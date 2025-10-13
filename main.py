from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import logging
import os
import traceback
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import re

from database import Base, engine, get_db
from models import UserType, User
from schemas import UserCreate, UserRead, Token
from crud import get_user_by_email, create_user
from auth import verify_password, get_password_hash, create_access_token

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
app = FastAPI(title="Auth API", version="1.0.0", debug=DEBUG)

# Monta a pasta 'static' para servir arquivos estáticos
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Páginas HTML
@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(STATIC_DIR / "login.html", media_type="text/html")

@app.get("/register", include_in_schema=False)
def register_page():
    return FileResponse(STATIC_DIR / "register.html", media_type="text/html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/", tags=["health"])
def root():
    return {"message": "API de autenticação funcionando!"}

# Regras de senha: 6-8 chars, 1 minúscula, 1 maiúscula, 1 número, 1 especial, sem espaços
PASSWORD_PATTERN = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{6,8}$')

def validate_password_backend(pw: str):
    if PASSWORD_PATTERN.match(pw):
        return
    # Detalhes por regra (útil para o retorno)
    fails = []
    if not (6 <= len(pw) <= 8): fails.append("6-8 caracteres")
    if not re.search(r'[a-z]', pw): fails.append("ao menos 1 minúscula")
    if not re.search(r'[A-Z]', pw): fails.append("ao menos 1 maiúscula")
    if not re.search(r'\d', pw):    fails.append("ao menos 1 número")
    if not re.search(r'[^A-Za-z0-9]', pw): fails.append("ao menos 1 especial")
    if re.search(r'\s', pw): fails.append("sem espaços")
    raise HTTPException(status_code=422, detail={"password_requirements": fails})

@app.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["users"])
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está cadastrado."
        )
    try:
        validate_password_backend(payload.password)
        if payload.password != payload.password_confirmation:
            raise HTTPException(status_code=422, detail="password_mismatch")
        hashed = get_password_hash(payload.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"password_error: {e}")
    user = create_user(
        db,
        email=payload.email,
        hashed_password=hashed,
        user_type=UserType(payload.user_type.value),
    )
    return user

@app.post("/auth/token", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

class UserOut(BaseModel):
    id: int
    email: str
    user_type: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

@app.get("/users", response_model=List[UserOut], tags=["users"])
def list_users(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).offset(offset).limit(limit).all()

@app.get("/users/{user_id}", response_model=UserOut, tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")
    return user

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    logging.exception("Unhandled error")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# if DEBUG:
#     @app.exception_handler(Exception)
#     async def dev_exception_handler(request: Request, exc: Exception):
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "detail": str(exc),
#                 "exception": exc.__class__.__name__,
#                 "traceback": traceback.format_exc(),
#                 "path": str(request.url),
#             },
#         )
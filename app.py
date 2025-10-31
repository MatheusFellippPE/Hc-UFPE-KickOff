from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from pathlib import Path

app = FastAPI(title="Demandas API")

DB_PATH = Path(__file__).parent / "demandas.db"

# Usuário "logado" (mock)
CURRENT_USER = {
    "name": "Usuário Exemplo",
    "title": "Analista",
    "photoUrl": "https://via.placeholder.com/48"
}

ALLOWED_STATUS = {"recebida", "em analise", "em andamento", "concluida"}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS demandas (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              titulo TEXT NOT NULL,
              descricao TEXT NOT NULL,
              status TEXT NOT NULL,
              userName TEXT NOT NULL,
              userTitle TEXT NOT NULL,
              userPhotoUrl TEXT,
              createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()

@app.on_event("startup")
def on_startup():
    init_db()

class DemandaCreate(BaseModel):
    titulo: str
    descricao: str
    status: str

@app.get("/api/me")
def me():
    return CURRENT_USER

@app.get("/api/demandas")
def listar_demandas():
    conn = get_db()
    try:
        cur = conn.execute(
            "SELECT * FROM demandas WHERE userName = ? ORDER BY createdAt DESC",
            (CURRENT_USER["name"],)
        )
        rows = [dict(r) for r in cur.fetchall()]
        return rows
    finally:
        conn.close()

@app.post("/api/demandas", status_code=201)
def criar_demanda(payload: DemandaCreate):
    titulo = (payload.titulo or "").strip()
    descricao = (payload.descricao or "").strip()
    status = (payload.status or "").strip().lower()

    if not titulo or not descricao or not status:
        raise HTTPException(status_code=400, detail="Título, descrição e status são obrigatórios.")
    if status not in ALLOWED_STATUS:
        raise HTTPException(status_code=400, detail="Status inválido.")

    conn = get_db()
    try:
        cur = conn.execute("""
            INSERT INTO demandas (titulo, descricao, status, userName, userTitle, userPhotoUrl)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, descricao, status, CURRENT_USER["name"], CURRENT_USER["title"], CURRENT_USER["photoUrl"]))
        conn.commit()
        return {"id": cur.lastrowid}
    finally:
        conn.close()

# Monta arquivos estáticos (servirá /demandas.html e /scripts/*)
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

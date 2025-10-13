from typing import Optional
from sqlalchemy.orm import Session
from models import User, UserType

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(
    db: Session,
    *,
    email: str,
    hashed_password: str,
    user_type: UserType,
) -> User:
    user = User(
        email=email,
        hashed_password=hashed_password,
        user_type=user_type,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
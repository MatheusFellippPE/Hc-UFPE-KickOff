import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum as SAEnum,
    Boolean,
    DateTime,
    func,
    Index,
)
from database import Base

class UserType(enum.Enum):
    aluno = "aluno"
    professor = "professor"
    pesquisador = "pesquisador"
    mentor = "mentor"
    outros = "outros"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(SAEnum(UserType, name="user_type_enum"), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

Index("ix_users_email_unique", User.email, unique=True)
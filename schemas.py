from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

class UserType(str, Enum):
    aluno = "aluno"
    professor = "professor"
    pesquisador = "pesquisador"
    mentor = "mentor"
    outros = "outros"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str
    user_type: UserType

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_confirmation:
            raise ValueError("password e password_confirmation não conferem")
        return self

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    user_type: UserType
    is_active: bool
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
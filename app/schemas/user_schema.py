# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    disabled: bool

class UserCreate(UserBase):
    password: str  # A senha é necessária apenas ao criar um usuário

class UserUpdate(UserBase):
    email: EmailStr = None  # Torna opcional no update
    full_name: str = None
    disabled: bool = None

class User(UserBase):
    id: int  # Adiciona o ID, que é esperado em operações de leitura

    class Config:
        orm_mode = True

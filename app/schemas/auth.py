# В этом файле нужно описать Pydantic-схемы для регистрации и токенов

from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    """Pydantic-схема для регистрации с проверкой длины пароля"""
    email: str
    password: str = Field(min_length=6, max_length=20)

class TokenResponse(BaseModel):
    """Pydantic-схема для access-токенов"""
    access_token: str
    token_type: str = Field(default_factory="bearer")
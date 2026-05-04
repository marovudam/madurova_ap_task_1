# В этом файле нужно описать публичную схему пользователя, которая используется в ответах

from pydantic import BaseModel

class UserPublic(BaseModel):
    """Публичная схема пользователя"""
    id: int
    email: str
    role: str
    model_config = {"from_attributes": True}
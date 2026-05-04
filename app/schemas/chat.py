# В этом файле нужно описать схему запроса к чату и схему ответа.

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ChatRequest(BaseModel):
    """Схема запроса"""
    prompt: str = Field(..., min_length=1, max_length=5000, description="Основной текст запроса")
    system: Optional[str] = Field(None, max_length=1000, description="Системная инструкция (необязательна))")
    max_history: int = Field(default=10, ge=0, le=100, description="Количество сообщений из истории")
    temperature: float = Field(default=1.0, ge=0.0, le=2.0, description="Креативность модели (0.0-2.0)")

class ChatResponse(BaseModel):
    """Схема ответа"""
    answer: str = Field(..., description="Ответ модели")

class ChatMessagePublic(BaseModel):
    """Публичная схемв сообщения"""
    id: int
    role: str
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChatHistoryResponse(BaseModel):
    """История сообщений"""
    items: List[ChatMessagePublic]
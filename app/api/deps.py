# В этом файле нужно реализовать dependency injection

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_token

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_repo(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    """Получение репозитория пользователя"""
    return UserRepository(session)

async def get_message_repo(session: AsyncSession = Depends(get_db_session)) -> ChatMessageRepository:
    """Получение репозитория для сообщений"""
    return ChatMessageRepository(session)

async def get_openrouter_client() -> OpenRouterClient:
    """Получение репозитория OpenRouter"""
    return OpenRouterClient()

async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    """Получение usecase-объекта для авторизации"""
    return AuthUseCase(user_repo)

async def get_chat_usecase(message_repo: ChatMessageRepository = Depends(get_message_repo),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client)) -> ChatUseCase:
    """Получение usecase-объекта для чата"""
    return ChatUseCase(message_repo, openrouter_client)

async def get_current_user_id(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))) -> int:
    """Получение текущего пользователя (user_id) из токена авторизации"""
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка авторизации: токен не расшифрован",
            headers={"WWW-Authenticate": "Bearer"})
    try:
        user_id = int(payload["sub"])
        return user_id
    except (KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Ошибка авторизации: user_id не получен",
            headers={"WWW-Authenticate": "Bearer"})
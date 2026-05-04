# В этом файле нужно собрать приложение FastAPI как единый объект и подключить всё, 
# что относится к инфраструктуре приложения. Нужно создать функцию create_app(), 
# внутри которой создаётся FastAPI(title=...), добавляется CORS (если он предусмотрен в конфиге), 
# подключаются роутеры из app/api/routes_auth.py и app/api/routes_chat.py. 
# Далее нужно обеспечить создание таблиц базы данных при старте приложения. 
# Для этого на событии startup нужно открыть соединение с engine и выполнить Base.metadata.create_all. 
# Также здесь нужно реализовать простой технический endpoint GET /health, который возвращает статус и окружение, 
# чтобы можно было быстро проверять, что сервер запущен. В этом файле не должно быть бизнес-логики и работы с репозиториями. 
# Здесь только сборка приложения и инфраструктура запуска.

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Соединение с базой данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    """Создание приложения FastAPI"""
    app = FastAPI(title=settings.APP_NAME,
        description="Защищённый API для взаимодействия с большой языковой моделью",
        lifespan=lifespan)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(chat_router, prefix="/chat", tags=["chat"])
    
    @app.get("/health", tags=["health"])
    async def health_check():
        """Проверка запуска окружения: статус и окружение"""
        return {"status": "ok", "env": settings.env}
    
    return app

app = create_app()
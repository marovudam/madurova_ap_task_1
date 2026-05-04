# В этом файле нужно создать асинхронный engine SQLAlchemy и фабрику сессий

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

SQLITE_PATH = "sqlite+aiosqlite:///" + settings.SQLITE_PATH

engine = create_async_engine(SQLITE_PATH, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
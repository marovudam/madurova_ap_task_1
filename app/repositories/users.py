# В этом файле нужно реализовать репозиторий пользователей

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User

class UserRepository:
    """Репозиторий пользователей"""
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_by_email(self, email: str):
        """Поиск пользователя по email"""
        query = select(User).where(User.email == email)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_id(self, id: str):
        """Поиск пользователя по id"""
        query = select(User).where(User.id == id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, role: str):
        """Регистрация пользователя"""
        user = User(email=email, password_hash=password_hash, role=role)
        self.__session.add(user)
        await self.__session.commit()
        await self.__session.refresh(user)
        return user

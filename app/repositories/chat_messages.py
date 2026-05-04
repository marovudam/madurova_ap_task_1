# В этом файле нужно реализовать репозиторий сообщений. 
# Репозиторий должен уметь добавлять сообщение (сохранение роли и контента), 
# получать последние N сообщений пользователя с сортировкой, а также удалять всю историю пользователя. 
# В этом файле нельзя обращаться к OpenRouter и нельзя формировать логику “какие сообщения включать в контекст”.
#  Репозиторий только читает и пишет данные.

from app.db.models import ChatMessage
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class ChatMessageRepository:
    """Репозиторий сообщений"""
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create(self, user_id, role, content):
        """Отправка сообщения"""
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self.__session.add(message)
        await self.__session.commit()
        await self.__session.refresh(message)
        return message

    async def get_last_messages(self, user_id: int, n: int = 10):
        """Получение истории сообщений"""
        query = select(ChatMessage).where(ChatMessage.user_id == user_id)\
            .order_by(ChatMessage.created_at.desc()).limit(n)
        result = await self.__session.execute(query)
        return list(result.scalars().all())
    
    async def delete_all(self, user_id):
        """Удаление истории переписки пользователя"""
        query = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self.__session.execute(query)
        await self.__session.commit()
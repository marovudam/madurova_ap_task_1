# В этом файле нужно реализовать бизнес-логику общения с LLM

from app.repositories.chat_messages import ChatMessageRepository
from app.schemas.chat import ChatRequest, ChatHistoryResponse, ChatMessagePublic
from app.services.openrouter_client import OpenRouterClient

class ChatUseCase:
    """Usecase для переписки и ее истории"""
    def __init__(self, message_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient):
        self.message_repo = message_repo
        self.openrouter_client = openrouter_client
    
    async def ask(self, user_id: int, request: ChatRequest) -> str:
        """Сохранение переписки с моделью"""
        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        history = await self.message_repo.get_last_messages(user_id=user_id,
            n=request.max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": request.prompt})
        await self.message_repo.create(user_id=user_id, role="user", content=request.prompt) 
        answer = await self.openrouter_client.chat_completion(messages=messages,
            temperature=request.temperature)
        # сохранение ответа модели
        await self.message_repo.create(user_id=user_id, role="assistant", content=answer)
        return answer
    
    async def get_history(self, user_id: int, limit: int = 100) -> ChatHistoryResponse:
        """Запрос истории сообщений"""
        messages = await self.message_repo.get_last_messages(user_id=user_id, n=limit)
        items = [ChatMessagePublic.model_validate(msg) for msg in messages]
        return ChatHistoryResponse(items=items)
    
    async def clear_history(self, user_id: int) -> None:
        """"Очистка истории"""
        await self.message_repo.delete_all(user_id=user_id)
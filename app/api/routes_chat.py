# В этом файле нужно реализовать HTTP-эндпоинты чата

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse
from app.usecases.chat import ChatUseCase

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    """Эндпоинт отправки сообщения"""
    try:
        answer = await chat_usecase.ask(user_id=user_id, request=request)
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_history(limit: int = 10, user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    """Эндпоинт получения истории"""
    return await chat_usecase.get_history(user_id=user_id, limit=limit)


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)):
    """Эндпоинт очистки истории"""
    await chat_usecase.clear_history(user_id=user_id)
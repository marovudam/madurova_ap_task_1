# В этом файле нужно реализовать HTTP-эндпоинты авторизации

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import NotAuthorizedError, NotFoundError, EmailConflictError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter()

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    """Эндпоинт регистрации нового пользователя"""
    try:
        return await auth_usecase.register(request)
    except EmailConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    """Эндпоинт входа в систему"""
    try:
        access_token = await auth_usecase.login(email=form_data.username,
            password=form_data.password)
        return TokenResponse(access_token=access_token, token_type="bearer")
    except NotAuthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e),
            headers={"WWW-Authenticate": "Bearer"})


@router.get("/me", response_model=UserPublic)
async def get_current(user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)):  
    """Эндпоинт получения текущего авторизированного пользователя"""
    try:
        return await auth_usecase.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
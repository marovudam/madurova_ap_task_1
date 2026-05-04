# В этом файле нужно реализовать бизнес-логику регистрации и логина

from app.core.errors import EmailConflictError, NotAuthorizedError, NotFoundError
from app.core.security import verify_password, hash_password, create_token
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.user import UserPublic

class AuthUseCase:
    """Usecase для регистрации и логина"""
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def register(self, request: RegisterRequest) -> UserPublic:
        """Регистрация пользователя"""
        user = await self.user_repo.get_by_email(request.email)
        if user:
            raise EmailConflictError(f"Пользователь с email {request.email} уже существует")
        password_hash = hash_password(request.password)
        user = await self.user_repo.create(request.email, password_hash, "user")
        return UserPublic.model_validate(user)
    
    async def login(self, email: str, password: str) -> str:
        """Авторизация пользователя"""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise NotAuthorizedError("Не удалось авторизоваться")
        access_token = create_token(str(user.id), user.role)
        
        return access_token
    
    async def get_profile(self, user_id: int) -> UserPublic:
        """Получение авторизированного пользователя, нужно для эндпойнта me"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден")
        return UserPublic.model_validate(user)
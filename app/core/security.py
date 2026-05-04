# В этом файле нужно реализовать всю криптографию и безопасность на уровне “утилит”.
# Здесь должны быть функции для хеширования пароля и проверки пароля через passlib.
# Также здесь должна быть функция генерации JWT access token, которая формирует payload 
# с sub (идентификатор пользователя), role (роль), exp (время истечения) и iat (время выдачи). 
# Также должна быть функция декодирования токена, которая валидирует подпись и срок действия и возвращает payload. 
# Этот файл не должен обращаться к базе данных и не должен знать, как устроены роуты. 
# Он предоставляет только функции для использования в usecase и dependency-слое.


from passlib.context import CryptContext
import time
import jwt
from app.core.config import settings
from typing import Any

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    """Функция хеширования пароля"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Функция проверки пароля"""
    return pwd_context.verify(password, hashed_password)


def create_token(sub: str, role: str) -> str:
    """Генерация access-токена"""
    payload = {
        "type": "access",
        "sub": sub,
        "role": role,
        "exp": int(time.time()) + 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "iat": int(time.time())
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict[str, Any]:
    """Декодирование access-токена"""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    return payload
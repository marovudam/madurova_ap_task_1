# В этом файле нужно описать собственные исключения приложения, которыми пользуются usecase и сервисы. 
# Должны быть базовая ошибка приложения и типовые наследники: конфликт (например, email уже существует), 
# неавторизован (неверный пароль), запрещено (нет прав), не найдено (объект в базе отсутствует), 
# ошибка внешнего сервиса (например, OpenRouter вернул ошибку). 
# Эти исключения нужны для того, чтобы бизнес-слой не зависел от FastAPI и не выбрасывал HTTPException.
# Usecase должен выбрасывать доменные ошибки, а роутер уже превращает их в HTTP-ответ.

class AppError(Exception):
    """Базовая ошибка приложения"""
    pass

class EmailConflictError(AppError):
    """Ошибка конфликта email"""
    def __init__(self, message):
        super().__init__("Пользователь с email уже зарегистрирован: " + message)


class NotAuthorizedError(AppError):
    """Ошибка: пользователь не авторизован"""
    def __init__(self, message):
        super().__init__("Пользователь не авторизован: " + message)


class ForbiddenError(AppError):
    """Ошибка: у пользователя нет прав"""
    def __init__(self, message):
        super().__init__("У пользователя нет прав для выполнения действия: " + message)


class NotFoundError(AppError):
    """Ошибка: объект не найден"""
    def __init__(self, message):
        super().__init__("Объект не найден: " + message)


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса"""
    def __init__(self, message):
        super().__init__("Внешний сервис вернул ошибку: " + message)
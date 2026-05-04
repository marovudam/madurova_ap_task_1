# В этом файле нужно объявить базовый класс SQLAlchemy для декларативных моделей. 
# Должен быть класс Base(DeclarativeBase). Это общий базовый класс, от которого наследуются ORM-модели. 
# Никакой дополнительной логики не требуется.

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Базовый класс для ORM-моделей"""
    pass
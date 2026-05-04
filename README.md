# Защищённый API для работы с большой языковой моделью

## Установка и запуск

Установка и запуск приложения производятся с помощью пакетного менеджера uv

Установка uv:
```pip install uv```

Создание и запуск виртуального окружения:

```
uv venv
source .venv/bin/activate # MacOS/Linux
.venv\Scripts\activate.bat # Windows
```

Запуск приложения:
```
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Интерфейс Swagger UI доступен по ссылке [http://localhost:8000/docs](http://localhost:8000/docs)

Статус сервиса можно проверить по ссылке [http://localhost:8000/health](http://localhost:8000/health)

## Пример работы

Регистрация пользователя с email madurova@email.com:

![регистрация madurova@email.com](img/registration.png)


Авторизация по паролю и получение токена:

![авторизация по паролю и получение токена](img/auth.png)

Авторизация с полученным токеном через интерфейс Swagger:

![авторизация с использованием токена](img/token_auth.png)

Авторизация с полученным токеном через интерфейс Swagger (результат):

![авторизация с использованием токена: результат](img/token_auth.png)

Запрос и ответ модели:

![запрос к модели и ответ](img/prompt_answer.png)

История запросов:

![история запроса](img/history.png)


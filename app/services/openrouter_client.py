# В этом файле нужно реализовать клиента для OpenRouter
import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
    """Клиент OpenRouter"""
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.__api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.site_url = settings.OPENROUTER_SITE_URL
        self.app_name = settings.OPENROUTER_APP_NAME
    
    async def chat_completion(self, messages: list[dict], temperature: float = 0.5) -> str:
        """Отправка и получение сообщений от модели"""
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/chat/completions", 
                headers=headers, json=payload, timeout=60.0)
            if response.status_code != 200:
                raise ExternalServiceError(f"Ошибка OpenRouter: {response.status_code} - {response.text}")
            data = response.json()
            return data["choices"][0]["message"]["content"]
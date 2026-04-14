import asyncio
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 5) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        
        if event.from_user.id in self.limit:
            return await event.answer('⚠️ Не так швидко! Зачекайте кілька секунд перед наступним запитом.')
        
        self.limit[event.from_user.id] = None
        return await handler(event, data)
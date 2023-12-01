from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from cachetools import TTLCache


class AntiFloodMiddleware(BaseMiddleware):

    # Usually set to int = 5
    def __init__(self, time_limit: int = 0) -> None:
        # Initialize a time-based cache with a maximum size of 10,000 and a specified time limit (ttl)
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Check if the chat ID is already present in the cache
        if event.chat.id in self.limit:
            # If present, return without further processing (anti-flood mechanism)
            return
        else:
            # If not present, add the chat ID to the cache with a value of None
            self.limit[event.chat.id] = None
        # Call the original event handler and return its result
        return await handler(event, data)

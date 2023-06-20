from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from python_aternos.ataccount import AternosAccount


class AternosAccountMiddleware(BaseMiddleware):
    def __init__(self, aternos: AternosAccount) -> None:
        self.aternos_account = aternos

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data['aternos_account'] = self.aternos_account
        return await handler(event, data)

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from data.config import ADMIN


class WhitelistMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.whitelist = ADMIN

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id not in self.whitelist:
            return await handler(event, data)
        return event.answer(_("You cannot use this bot, write to the bot administrator"))

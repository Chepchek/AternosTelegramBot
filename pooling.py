import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n, ConstI18nMiddleware

from data.config import TELEGRAM_TOKEN, LOCALE
from handlers import (
    start_router,
    server_manager_router,
)
from middlewares import AternosAccountMiddleware
from middlewares.whitelist import WhitelistMiddleware
from utils.aternos import aternos_login
from utils.misc.logging import set_logging_level


async def main():
    set_logging_level()

    bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')

    i18n = I18n(path="./locales/", default_locale=LOCALE, domain="messages")
    aternos_account = aternos_login()
    dp = Dispatcher(bot=bot)
    dp.message.middleware(AternosAccountMiddleware(aternos_account))
    dp.message.middleware(ConstI18nMiddleware(i18n=i18n, locale=LOCALE))
    dp.message.middleware(WhitelistMiddleware())
    dp.callback_query.middleware(AternosAccountMiddleware(aternos_account))
    dp.callback_query.middleware(ConstI18nMiddleware(i18n=i18n, locale=LOCALE))
    dp.callback_query.middleware(WhitelistMiddleware())

    for router in [start_router, server_manager_router]:
        dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

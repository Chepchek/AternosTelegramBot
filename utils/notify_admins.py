import logging

from aiogram import Dispatcher

from data.config import ADMINS, BOT_NOTIFY_STARTED

from l10n.strings import string


async def on_startup_notify(dp: Dispatcher):
    if BOT_NOTIFY_STARTED:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, string("bot_started"))

            except Exception as err:
                logging.exception(err)

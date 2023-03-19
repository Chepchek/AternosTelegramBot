from aiogram import types
from l10n.strings import string


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", string("cmd_start")),
            types.BotCommand("help", string("cmd_help")),
        ]
    )

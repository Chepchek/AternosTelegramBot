from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from l10n.strings import string
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(string("help"))

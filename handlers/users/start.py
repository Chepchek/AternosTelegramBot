from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS

from keyboards.inline.aternos import get_server_list_kb
from l10n.strings import string

from loader import dp


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer(
        f"{string('hello')}, {message.from_user.full_name}!",
        reply_markup=get_server_list_kb(),
    )

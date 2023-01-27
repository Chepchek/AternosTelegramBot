from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu import menu

from data.config import ADMINS

from loader import dp


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu)

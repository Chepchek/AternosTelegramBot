from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=15, keyboard=[
    [
        KeyboardButton("Список серверов 📄")
    ]
])
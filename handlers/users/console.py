import asyncio
import logging

from typing import Dict, Any, Tuple

import ujson as ujson
from aiogram import types
from aiogram.dispatcher import FSMContext
from python_aternos import AternosWss, Streams

from loader import dp


# The code for working with websockets from the python_aternos library is not very good)
# TODO: rewrite the connection via the websocket at a low level


@dp.callback_query_handler(text="OpenServerConsole", state="ServerDetail")
async def get_console(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = data["server"]
    # if server.status in ['offline', 'loading']:
    #     await call.answer("Сервер должен быть запущен!")
    #     return
    await call.message.answer("Консоль сервера")
    socket: AternosWss = server.wss()
    await socket.connect()
    while True:
        try:
            data = await socket.socket.recv()
            obj = ujson.loads(data)
            msgtype = Streams.none
            msg = None

            if obj['type'] == 'line':
                msgtype = Streams.console
                msg = obj['data'].strip('\r\n ')

            elif obj['type'] == 'heap':
                msgtype = Streams.ram
                msg = int(obj['data']['usage'])

            elif obj['type'] == 'tick':
                msgtype = Streams.tps
                ticks = 1000 / obj['data']['averageTickTime']
                msg = 20 if ticks > 20 else ticks

            elif obj['type'] == 'status':
                msgtype = Streams.status
                msg = ujson.loads(obj['message'])
            await call.message.answer(f"Received {msgtype}\nMessage: \n <b>{msg}</b>\n")
        except asyncio.CancelledError as e:
            logging.exception(e)
            pass
        await asyncio.sleep(1)

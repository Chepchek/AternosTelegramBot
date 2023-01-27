import pytz
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.aternos import get_server_list_kb, ServerCallback_data, get_server_panel, get_server_players

from data.config import ADMINS
from loader import dp, AternosClient


def get_text(server_id: str):
    server = AternosClient.get_server(servid=server_id)
    return ("Информация о сервере:\n\n"
            f"<b>IP:</b> {server.address}\n"
            f"<b>Status:</b> {server.status.upper()}\n"
            f"<b>Online:</b> {server.players_count}/{server.slots}\n"
            f"<b>Minecraft edition:</b> {'JAVA' if server.is_bedrock == 0 else 'BEDROCK'}\n"
            f"<b>Server version:</b> {server.software} | {server.version}\n"
            f"<b>Используется RAM:</b> {server.ram}\n\n\n"
            f"<b>Последнее обновление: {datetime.now(pytz.timezone('Europe/Moscow')).strftime('%y.%m.%d %H:%M:%S')}</b>"
            )


@dp.message_handler(text="Список серверов 📄", user_id=ADMINS, state="*")
async def server_list(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Список серверов 📄", reply_markup=get_server_list_kb())


@dp.callback_query_handler(ServerCallback_data.filter())
async def server_detail(call: types.CallbackQuery, callback_data: ServerCallback_data, state: FSMContext):
    server = AternosClient.get_server(callback_data['server_id'])
    await state.set_state("ServerDetail")
    await state.update_data(server_id=server.servid)
    await call.message.edit_text(get_text(server_id=server.servid),
                                 reply_markup=get_server_panel(server_id=server.servid))


@dp.callback_query_handler(text="StartServer", state="ServerDetail")
async def start_server(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = AternosClient.get_server(servid=data["server_id"])
    if server.status != "offline":
        await call.answer("Сервер уже запущен!", show_alert=True)
        return
    server.start()
    await call.answer("Запуск сервера", show_alert=True)
    await call.message.edit_text(get_text(server_id=server.servid),
                                 reply_markup=get_server_panel(server_id=server.servid))


@dp.callback_query_handler(text="RestartServer", state="ServerDetail")
async def restart_server(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = AternosClient.get_server(servid=data["server_id"])
    if server.status == "offline":
        await call.answer("Сначала запустите сервер!", show_alert=True)
        return
    server.restart()
    await call.answer("Перезапуск сервера", show_alert=True)
    await call.message.edit_text(get_text(server_id=server.servid),
                                 reply_markup=get_server_panel(server_id=server.servid))


@dp.callback_query_handler(text="CancelStart", state="ServerDetail")
async def cancel_start(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = AternosClient.get_server(servid=data["server_id"])
    if server.status != "loading":
        await call.answer("Сначала запуститe\остановвите сервер!", show_alert=True)
        return
    server.cancel()
    await call.answer("Выключение сервера", show_alert=True)
    await call.message.edit_text(get_text(server_id=server.servid),
                                 reply_markup=get_server_panel(server_id=server.servid))


@dp.callback_query_handler(text="ShutdownServer", state="ServerDetail")
async def restart_server(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = AternosClient.get_server(servid=data["server_id"])
    if server.status == "offline":
        await call.answer("Сначала запустите сервер!", show_alert=True)
        return
    server.stop()
    await call.answer("Выключение сервера", show_alert=True)
    await call.message.edit_text(get_text(server_id=server.servid),
                                 reply_markup=get_server_panel(server_id=server.servid))


@dp.callback_query_handler(text="RefreshServerInfo", state="ServerDetail")
async def refresh_server_info(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text(get_text(server_id=data['server_id']),
                                 reply_markup=get_server_panel(server_id=data['server_id']))


@dp.callback_query_handler(text="GetPlayerList", state="ServerDetail")
async def get_player_list(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup, online_info = get_server_players(server_id=data['server_id'])
    if markup:
        await call.message.edit_text(f"Список игроков, которые в данный момент играют на сервере <b>{online_info}</b>",
                                     reply_markup=markup)
    else:
        await call.answer("Список игроков пуст или недоступен!", show_alert=True)

from datetime import datetime

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.aternos import (
    get_server_list_kb,
    get_server_panel,
    get_server_players,
    ServerCallback_data,
)

from l10n.strings import string
from loader import AternosClient, dp


def get_text(server_id: str):
    server = AternosClient.get_server(servid=server_id)
    return (
        f"{string('server_info')}:\n\n"
        f"<b>IP:</b> {server.address}\n"
        f"<b>Status:</b> {server.status.upper()}\n"
        f"<b>Online:</b> {server.players_count}/{server.slots}\n"
        f"<b>Minecraft edition:</b> "
        f"{'JAVA' if server.is_bedrock == 0 else 'BEDROCK'}\n"
        f"<b>Server version:</b> {server.software} | {server.version}\n"
        f"<b>{string('used_ram')}:</b> {server.ram}\n\n"
        f"<b>{string('last_update')} (UTC): "
        f"{datetime.now(pytz.timezone('UTC')).strftime('%y.%m.%d %H:%M:%S')}"
        f"</b>"
    )


@dp.callback_query_handler(text="ServerList", state="ServerDetail")
async def server_list(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(
        string("server_list"), reply_markup=get_server_list_kb()
    )


@dp.callback_query_handler(ServerCallback_data.filter())
async def server_detail(
    call: types.CallbackQuery,
    callback_data: ServerCallback_data,
    state: FSMContext,
):
    server = AternosClient.get_server(callback_data["server_id"])
    await state.set_state("ServerDetail")
    await state.update_data(server=server)
    await call.message.edit_text(
        get_text(server_id=server.servid),
        reply_markup=get_server_panel(server_id=server.servid),
    )


@dp.callback_query_handler(text="StartServer", state="ServerDetail")
async def start_server(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = data["server"]
    if server.status != "offline":
        await call.answer(string("server_running"), show_alert=True)
        return
    server.start()
    await call.answer(string("start"), show_alert=True)
    await call.message.edit_text(
        get_text(server_id=server.servid),
        reply_markup=get_server_panel(server_id=server.servid),
    )


@dp.callback_query_handler(text="RestartServer", state="ServerDetail")
async def restart_server(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = data["server"]
    if server.status == "offline":
        await call.answer(string("start_first"), show_alert=True)
        return
    server.restart()
    await call.answer(string("restart"), show_alert=True)
    await call.message.edit_text(
        get_text(server_id=server.servid),
        reply_markup=get_server_panel(server_id=server.servid),
    )


@dp.callback_query_handler(text="CancelStart", state="ServerDetail")
async def cancel_start(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = data["server"]
    if server.status != "loading":
        await call.answer(string("start_stop_server"), show_alert=True)
        return
    server.cancel()
    await call.answer(string("cancel"), show_alert=True)
    await call.message.edit_text(
        get_text(server_id=server.servid),
        reply_markup=get_server_panel(server_id=server.servid),
    )


@dp.callback_query_handler(text="ShutdownServer", state="ServerDetail")
async def shutdown_server(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    server = data["server"]
    if server.status == "offline":
        await call.answer(string("start_first"), show_alert=True)
        return
    server.stop()
    await call.answer(string("shutdown"), show_alert=True)
    await call.message.edit_text(
        get_text(server_id=server.servid),
        reply_markup=get_server_panel(server_id=server.servid),
    )


@dp.callback_query_handler(text="RefreshServerInfo", state="ServerDetail")
async def refresh_server_info(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text(
        get_text(server_id=data["server"].servid),
        reply_markup=get_server_panel(server_id=data["server"].servid),
    )


@dp.callback_query_handler(text="GetPlayerList", state="ServerDetail")
async def get_player_list(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup, online_info = get_server_players(server=data["server"])
    if markup:
        await call.message.edit_text(
            f"{string('current_players')} <b>{online_info}</b>",
            reply_markup=markup,
        )
    else:
        await call.answer(string("current_players_error"), show_alert=True)


@dp.callback_query_handler(text="None")
async def get_player_info(call: types.CallbackQuery, state: FSMContext):
    await call.answer()


# @dp.callback_query_handler(text="OpenServerConsole", state="ServerDetail")
# async def get_console(call: types.CallbackQuery, state: FSMContext):
#     await call.message.answer(string("console"))
#     data = await state.get_data()
#     server = data["server"]
#     if server.status in ['offline', 'loading']:
#         await call.answer(string("server_must_be_running"))
#         return None
#     socket = server.wss()
#     await socket.connect()
#     await socket.command("/help")
#     while True:
#         @socket.wssreceiver(Streams.console, call)
#         async def console(msg: Dict[Any, Any], args: Tuple[str]) -> None:
#             logging.info(args[0], 'received', msg)
#             await call.message.answer(f"{args[0]} | {msg}")
#             print(msg)

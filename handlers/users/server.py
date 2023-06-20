from datetime import datetime, timedelta

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.utils.i18n import gettext as _
from python_aternos import AternosServer
from python_aternos.ataccount import AternosAccount

from keyboards.inline.aternos.server import get_server_list_kb, get_server_panel, get_server_players
from keyboards.inline.callback import (
    AternosServerCallbackData,
    GetAternosServerListCallbackData,
    AternosServerActionCallbackData
)
from states.server import ServerDetailState

server_manager_router = Router()


def server_info_text(server: AternosServer) -> str:
    return _(
        "<b>Server info:</b>\n\n"
        "<b>IP:</b> {address}\n"
        "<b>Status:</b> {status}\n"
        "<b>Countdown:</b> {countdown}\n"
        "<b>Online:</b> {players_count}/{slots}\n"
        "<b>Server version:</b> {software} | {version}\n"
        "<b>RAM:</b> {ram}\n\n<b>Last info update (server time): {time}</b>").format(
        address=server.address,
        countdown=timedelta(seconds=server.countdown) if server.countdown != -1 else "-",
        status=server.status.upper(),
        players_count=server.players_count,
        slots=server.slots,
        software=server.software,
        version=server.version,
        ram=server.ram,
        time=datetime.now().strftime('%y.%m.%d %H:%M:%S'))


@server_manager_router.callback_query(GetAternosServerListCallbackData.filter(), any_state)
async def server_list(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    await state.clear()
    await call.message.edit_text(_("List of servers"), reply_markup=get_server_list_kb(aternos_account))


@server_manager_router.callback_query(AternosServerCallbackData.filter(), any_state)
async def server_detail(call: types.CallbackQuery,
                        callback_data: AternosServerCallbackData,
                        state: FSMContext,
                        aternos_account: AternosAccount):
    server = aternos_account.get_server(callback_data.server_id)
    server.fetch()
    await state.set_state(ServerDetailState.server_detail)
    await state.update_data(server=callback_data.server_id)
    await call.message.edit_text(
        server_info_text(server),
        reply_markup=get_server_panel(
            server_id=server.servid,
            aternos_account=aternos_account
        )
    )


@server_manager_router.callback_query(AternosServerActionCallbackData.filter(F.action == "StartServer"),
                                      ServerDetailState.server_detail)
async def start_server(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    data = await state.get_data()
    server = aternos_account.get_server(servid=data["server"])
    server.fetch()
    if server.status != "offline":
        await call.answer(_("The server is already running!"), show_alert=True)
        return
    server.start()
    await call.answer(_("Starting the server"), show_alert=True)
    await call.message.edit_text(
        server_info_text(server),
        reply_markup=get_server_panel(
            server_id=server.servid,
            aternos_account=aternos_account
        )
    )


@server_manager_router.callback_query(AternosServerActionCallbackData.filter(F.action == "RestartServer"),
                                      ServerDetailState.server_detail)
async def restart_server(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    data = await state.get_data()
    server = aternos_account.get_server(servid=data["server"])
    server.fetch()
    if server.status == "offline":
        await call.answer(_("Start the server first!"), show_alert=True)
        return
    server.restart()
    await call.answer(_("Restarting the server"), show_alert=True)
    await call.message.edit_text(
        server_info_text(server),
        reply_markup=get_server_panel(
            server_id=server.servid,
            aternos_account=aternos_account
        )
    )


@server_manager_router.callback_query(AternosServerActionCallbackData.filter(F.action == "CancelStart"),
                                      ServerDetailState.server_detail)
async def cancel_start(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    data = await state.get_data()
    server = aternos_account.get_server(servid=data["server"])
    if server.status != "loading":
        await call.answer(_("First start/stop the server!"), show_alert=True)
        return
    server.cancel()
    await call.answer(_("Shutting down the server"), show_alert=True)
    await call.message.edit_text(
        server_info_text(server),
        reply_markup=get_server_panel(
            server_id=server.servid,
            aternos_account=aternos_account
        )
    )


@server_manager_router.callback_query(AternosServerActionCallbackData.filter(F.action == "ShutdownServer"),
                                      ServerDetailState.server_detail)
async def shutdown_server(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    data = await state.get_data()
    server = aternos_account.get_server(servid=data["server"])
    server.fetch()
    if server.status == "offline":
        await call.answer(_("Start the server first!"), show_alert=True)
        return
    server.stop()
    await call.answer(_("Shutting down the server"), show_alert=True)
    await call.message.edit_text(
        server_info_text(server),
        reply_markup=get_server_panel(
            server_id=server.servid,
            aternos_account=aternos_account
        )
    )


@server_manager_router.callback_query(AternosServerActionCallbackData.filter(F.action == "RefreshServerInfo"),
                                      ServerDetailState.server_detail)
async def refresh_server_info(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    data = await state.get_data()
    server = aternos_account.get_server(servid=data["server"])
    server.fetch()
    await call.message.edit_text(
        server_info_text(server),
        reply_markup=get_server_panel(
            server_id=data['server'],
            aternos_account=aternos_account
        )
    )


@server_manager_router.callback_query(AternosServerActionCallbackData.filter(F.action == "GetPlayerList"),
                                      ServerDetailState.server_detail)
async def get_player_list(call: types.CallbackQuery, state: FSMContext, aternos_account: AternosAccount):
    data = await state.get_data()
    server = aternos_account.get_server(servid=data["server"])
    server.fetch()
    markup, online_info = get_server_players(server=server)
    if markup:
        await call.message.edit_text(_("Server player list <b>{online_info}</b>").format(online_info=online_info),
                                     reply_markup=markup)
    else:
        await call.answer(_("Server player list empty or unavailable!"), show_alert=True)

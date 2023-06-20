from functools import lru_cache

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from python_aternos import AternosServer
from python_aternos.ataccount import AternosAccount

from keyboards.inline.callback import AternosServerCallbackData
from keyboards.inline.callback.server import GetAternosServerListCallbackData, AternosServerActionCallbackData


@lru_cache
def get_kb_server_list() -> InlineKeyboardMarkup:
    return InlineKeyboardBuilder().button(
        text=_("Server list"),
        callback_data=GetAternosServerListCallbackData(payload="GetServerList")
    ).adjust(1).as_markup()


def get_server_list_kb(aternos_account: AternosAccount) -> InlineKeyboardMarkup:
    server_list_kb = InlineKeyboardBuilder()
    for server in aternos_account.list_servers():
        server.fetch()
        server_list_kb.button(
            text=server.address,
            callback_data=AternosServerCallbackData(server_id=server.servid)
        )
    server_list_kb.adjust(1)
    return server_list_kb.as_markup()


def get_server_panel(aternos_account: AternosAccount, server_id: str) -> InlineKeyboardMarkup:
    server_panel_kb = InlineKeyboardBuilder()

    server = aternos_account.get_server(servid=server_id)

    server.fetch()

    if server.status != "offline":
        server_panel_kb.button(
            text=_("Shutdown server"),
            callback_data=AternosServerActionCallbackData(action="ShutdownServer")
        )
        server_panel_kb.button(
            text=_("Restart"),
            callback_data=AternosServerActionCallbackData(action="RestartServer")
        )
        server_panel_kb.button(
            text=_("Player list"),
            callback_data=AternosServerActionCallbackData(action="GetPlayerList")
        )

    elif server.status == "starting":
        server_panel_kb.button(
            text=_("Cancel start"),
            callback_data=AternosServerActionCallbackData(action="CancelStart")
        )

    else:
        server_panel_kb.button(
            text=_("Start server"),
            callback_data=AternosServerActionCallbackData(action="StartServer")
        )

    server_panel_kb.button(
        text=_("Update info"),
        callback_data=AternosServerActionCallbackData(action="RefreshServerInfo")
    )

    server_panel_kb.adjust(1)

    return server_panel_kb.as_markup()


def get_server_players(server: AternosServer):
    players_kb = InlineKeyboardBuilder()
    if not server.players_list:
        return None, None
    for player in server.players_list:
        players_kb.button(text=player, callback_data="None")
    players_kb.adjust(1)
    return players_kb.as_markup(), f"{server.players_count}/{server.slots}"

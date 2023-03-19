from typing import Tuple, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from l10n.strings import string

from loader import AternosClient
from python_aternos import AternosServer

ServerCallback_data = CallbackData("server", "server_id")


def get_server_list_kb() -> InlineKeyboardMarkup:
    server_list_kb = InlineKeyboardMarkup()
    for server in AternosClient.list_servers():
        server_list_kb.add(
            InlineKeyboardButton(
                text=server.address,
                callback_data=ServerCallback_data.new(server_id=server.servid),
            )
        )
    return server_list_kb


def get_server_panel(server_id: str) -> InlineKeyboardMarkup:
    server_panel_kb = InlineKeyboardMarkup()
    server = AternosClient.get_server(servid=server_id)
    if server.status != "offline":
        server_panel_kb.add(
            InlineKeyboardButton(
                text=string("shutdown"), callback_data="ShutdownServer"
            )
        )
        server_panel_kb.add(
            InlineKeyboardButton(
                text=string("restart"), callback_data="RestartServer"
            )
        )
        server_panel_kb.add(
            InlineKeyboardButton(
                text=string("player_list"), callback_data="GetPlayerList"
            )
        )
        # server_panel_kb.add(InlineKeyboardButton(text=string("console"),
        # callback_data="OpenServerConsole"))
    elif server.status == "starting":
        server_panel_kb.add(
            InlineKeyboardButton(
                text=string("cancel"), callback_data="CancelStart"
            )
        )
    else:
        server_panel_kb.add(
            InlineKeyboardButton(
                text=string("start"), callback_data="StartServer"
            )
        )
    server_panel_kb.add(
        InlineKeyboardButton(
            text=string("refresh"), callback_data="RefreshServerInfo"
        )
    )
    return server_panel_kb


def get_server_players(
    server: AternosServer,
) -> Union[Tuple[InlineKeyboardMarkup, str], Tuple[None, None]]:
    players_kb = InlineKeyboardMarkup()
    if not server.players_list:
        return None, None
    for player in server.players_list:
        players_kb.add(InlineKeyboardButton(text=player, callback_data="None"))
    return players_kb, f"{server.players_count}/{server.slots}"

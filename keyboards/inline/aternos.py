from typing import Union, Tuple

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from python_aternos import AternosServer

from loader import AternosClient

ServerCallback_data = CallbackData("server", "server_id")


def get_server_list_kb() -> InlineKeyboardMarkup:
    server_list_kb = InlineKeyboardMarkup()
    for server in AternosClient.list_servers():
        server_list_kb.add(InlineKeyboardButton(text=server.address,
                                                callback_data=ServerCallback_data.new(server_id=server.servid)
                                                )
                           )
    return server_list_kb


def get_server_panel(server_id: str) -> InlineKeyboardMarkup:
    server_panel_kb = InlineKeyboardMarkup()
    server = AternosClient.get_server(servid=server_id)
    if server.status != "offline":
        server_panel_kb.add(InlineKeyboardButton(text="Выключить сервер", callback_data="ShutdownServer"))
        server_panel_kb.add(InlineKeyboardButton(text="Перезапустить", callback_data="RestartServer"))
        server_panel_kb.add(InlineKeyboardButton(text="Просмотреть игроков", callback_data="GetPlayerList"))
        # server_panel_kb.add(InlineKeyboardButton(text="Открыть консоль", callback_data="OpenServerConsole"))
    elif server.status == "starting":
        server_panel_kb.add(InlineKeyboardButton(text="Остановить", callback_data="CancelStart"))
    else:
        server_panel_kb.add(InlineKeyboardButton(text="Запустить сервер", callback_data="StartServer"))
    server_panel_kb.add(InlineKeyboardButton(text="Обновить информацию", callback_data="RefreshServerInfo"))
    return server_panel_kb


def get_server_players(server: AternosServer) -> Union[tuple[InlineKeyboardMarkup, str], tuple[None, None]]:
    players_kb = InlineKeyboardMarkup()
    if not server.players_list:
        return None, None
    for player in server.players_list:
        players_kb.add(InlineKeyboardButton(text=player, callback_data="None"))
    return players_kb, f"{server.players_count}/{server.slots}"

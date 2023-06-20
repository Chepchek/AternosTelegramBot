from aiogram.filters.callback_data import CallbackData


class AternosServerCallbackData(CallbackData, prefix="AternosServer"):
    server_id: str


class GetAternosServerListCallbackData(CallbackData, prefix="GetAternosServerList"):
    payload: str


class AternosServerActionCallbackData(CallbackData, prefix="AternosServerActionCallbackData"):
    action: str

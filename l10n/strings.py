from data import config


L10N = {
    "start": {"russian": "Запустить сервер", "english": "Start"},
    "restart": {"russian": "Перезапустить", "english": "Restart"},
    "player_list": {
        "russian": "Просмотреть игроков",
        "english": "Player list",
    },
    "cancel": {"russian": "Остановить", "english": "Cancel start"},
    "shutdown": {"russian": "Выключить сервер", "english": "Shutdown"},
    "refresh": {"russian": "Обновить информацию", "english": "Refresh info"},
    "console": {"russian": "Открыть консоль", "english": "Open console"},
    "server_list": {
        "russian": "Список серверов 📄",
        "english": "Server list 📄",
    },
    "server_info": {
        "russian": "Информация о сервере",
        "english": "Server information",
    },
    "used_ram": {"russian": "Используется RAM", "english": "Used RAM"},
    "last_update": {
        "russian": "Последнее обновление",
        "english": "Last update",
    },
    "current_players": {
        "russian": "Список игроков, которые в данный момент играют на сервере",
        "english": "List of players currently playing on the server",
    },
    "current_players_error": {
        "russian": "Список игроков пуст или недоступен!",
        "english": "The list of players is empty or unavailable!",
    },
    "start_first": {
        "russian": "Сначала запустите сервер!",
        "english": "Start the server first!",
    },
    "start_stop_first": {
        "russian": "Сначала запуститe\остановвите сервер!",
        "english": "First start/stop the server!",
    },
    "server_running": {
        "russian": "Сервер уже запущен!",
        "english": "Server is already running!",
    },
    "server_must_be_running": {
        "russian": "Сервер должен быть запущен!",
        "english": "Server must be running!",
    },
    "help": {
        "russian": (
            "Список команд:\n"
            "/start - Начать диалог\n"
            "/help - Получить справку"
        ),
        "english": (
            "Command list:\n" "/start - Start a dialogue\n" "/help - Get help"
        ),
    },
    "hello": {"russian": "Привет", "english": "hello"},
    "bot_started": {"russian": "Бот Запущен", "english": "Bot started"},
    "cmd_start": {"russian": "Запустить бота", "english": "Run the bot"},
    "cmd_help": {"russian": "Вывести справку", "english": "Display help"},
}


def string(key: str) -> str:
    return L10N[key][config.BOT_LANG]

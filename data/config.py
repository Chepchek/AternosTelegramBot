from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Get a bot token
ADMINS = env.list("ADMINS")  # admins list
ATERNOS_LOGIN = env.str("ATERNOS_LOGIN", None)
ATERNOS_PASS = env.str("ATERNOS_PASS", None)
ATERNOS_PASS_HASH = env.str("ATERNOS_PASS_HASH", None)
ATERNOS_COOKIE = env.str("ATERNOS_COOKIE", None)


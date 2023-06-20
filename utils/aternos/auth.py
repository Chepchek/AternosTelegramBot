import logging
import os

from python_aternos import Client
from python_aternos.ataccount import AternosAccount

from data.config import ATERNOS_LOGIN, ATERNOS_PASS_HASH, ATERNOS_PASS


ATERNOS_SESSIONS_FILES: str = "./aternos_session"


def aternos_login() -> AternosAccount:
    client = Client()
    aternos = client.account

    if not os.path.exists(ATERNOS_SESSIONS_FILES):
        os.makedirs(ATERNOS_SESSIONS_FILES)

    client.sessions_dir = ATERNOS_SESSIONS_FILES

    if not ATERNOS_LOGIN:
        logging.error("Aternos login was not specified, authorization is not possible")
    elif not ATERNOS_PASS and not ATERNOS_PASS_HASH:
        logging.error("Aternos password and password hash was not specified, authorization is not possible")

    if ATERNOS_LOGIN and ATERNOS_PASS:
        client.login(ATERNOS_LOGIN, ATERNOS_PASS)
        logging.info("Successfully logged in according with LOGIN | PASS")
    elif ATERNOS_LOGIN and ATERNOS_PASS_HASH:
        client.login_hashed(ATERNOS_LOGIN, ATERNOS_PASS)
        logging.info("Successfully logged in according with LOGIN | PASS HASH")

    client.save_session()

    return aternos

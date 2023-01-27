import logging

from python_aternos import Client
from data import config


def get_aternos_auth() -> Client:
    try:
        return Client.restore_session()
    except Exception as e:
        logging.exception(e)
        if config.ATERNOS_PASS:
            logging.info("Successfully authenticated with Aternos login | password")
            return Client.from_credentials(username=config.ATERNOS_LOGIN, password=config.ATERNOS_PASS)
        elif config.ATERNOS_PASS_HASH:
            logging.info("Successfully authenticated with Aternos login | hash")
            return Client.from_hashed(username=config.ATERNOS_LOGIN, md5=config.ATERNOS_PASS_HASH)
        elif config.ATERNOS_COOKIE:
            logging.info("Successfully authenticated with Aternos cookie")
            return Client.from_session(session=config.ATERNOS_COOKIE)
        else:
            raise ValueError("Invalid reading data from .env file")

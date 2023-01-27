import logging
import os

from python_aternos import Client
from data import config

aternos_session = os.path.join(os.path.dirname(__file__), '../aternos_session')


def saved_sessions():
    sessions = list()
    for saved_session in os.listdir(aternos_session):
        sessions.append(os.path.join(aternos_session, saved_session))
    if len(sessions) > 1:
        logging.warning(f"You have more than one saved session, will be used {sessions[0]}")
    return sessions[0] if sessions else None


def get_aternos_auth() -> Client:
    try:
        session = Client.restore_session(file=saved_sessions())
        logging.info('Successfully restored session from aternos_session directory')
        return session
    except FileNotFoundError as e:
        logging.exception(e)
        if config.ATERNOS_PASS:
            logging.info("Successfully authenticated with Aternos login | password")
            session = Client.from_credentials(username=config.ATERNOS_LOGIN,
                                              password=config.ATERNOS_PASS,
                                              sessions_dir=aternos_session)
            return session
        elif config.ATERNOS_PASS_HASH:
            logging.info("Successfully authenticated with Aternos login | hash")
            session = Client.from_hashed(username=config.ATERNOS_LOGIN,
                                         md5=config.ATERNOS_PASS_HASH,
                                         sessions_dir=aternos_session)
            # session.save_session(file=aternos_session)
            return session
        elif config.ATERNOS_COOKIE:
            logging.info("Successfully authenticated with Aternos cookie")
            session = Client.from_session(session=config.ATERNOS_COOKIE)
            # session.save_session(file=aternos_session)
            return session
        else:
            raise ValueError("Invalid reading data from .env file")

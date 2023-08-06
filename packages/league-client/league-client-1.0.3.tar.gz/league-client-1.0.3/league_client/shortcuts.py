from league_connection import LeagueConnection

from league_process.process import open_riot_client

from .logger import logger
from .login import login as base_login
from .logout import logout
from .session import wait_session
from .username import check_username


def login(username,
          password,
          riot_exe,
          riot_lockfile,
          league_lockfile,
          ):
    while True:
        open_riot_client(riot_exe)
        riot_connection = LeagueConnection(riot_lockfile)
        res = base_login(riot_connection, username, password)
        if not res['ok']:
            return res
        league_connection = LeagueConnection(league_lockfile)
        res = wait_session(league_connection)
        if not res['ok']:
            return res
        res = check_username(league_connection, username)
        if not res['ok']:
            logger.info('Changing account...')
            logout(league_lockfile)
            continue
        return {'ok': True}

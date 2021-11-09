'''
    Error handling client decorators, to provide
    useful information sent back to the server or
    handle critical errors accordingly.

    Verified: 2020 December 30 & 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from client.state import ClientStatic
from shared.helper import Helper
from shared.state import Static
from shared.data import Data

import sys

if Static.EXE:
    from client.helper import ClientHelper

    import time


class ReconnectError(Exception):
    pass


class ClientError:

    if Static.EXE:
        __RECONNECT_TIMER = 10

    @staticmethod
    def general(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception as error:
                return Data.parse(Helper.join(
                    'Client Side Execution Failed',
                    f'{type(error).__name__}: {error}'
                ), status=Static.DANGER)

        return wrapper

    @staticmethod
    def critical(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except SystemExit:
                raise
            except ReconnectError:
                if Static.EXE:
                    ClientHelper.restart()
                else:
                    sys.exit()
            except TimeoutError:
                if Static.EXE:
                    time.sleep(ClientError.__RECONNECT_TIMER)
                    ClientHelper.restart()
                else:
                    sys.exit()
            except Exception:
                if Static.EXE and ClientStatic.STICKY:
                    time.sleep(ClientError.__RECONNECT_TIMER)
                    ClientHelper.restart()
                else:
                    sys.exit()

        return wrapper

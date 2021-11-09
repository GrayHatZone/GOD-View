'''
    A shared class among all modules to all
    have the same core identifying features
    when interacted with.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.helper import SafeIP
from server.state import Dynamic
from shared.error import Error


class Module:

    def __init__(self, conn, token, connect_ip):
        Dynamic.MODULES[token] = self
        self.__conn = conn
        self.__token = token
        self.__connect_ip = SafeIP(connect_ip)

    def __str__(self):
        return type(self).__name__

    @property
    def safe_connect_ip(self):
        return self.__connect_ip.safe

    @property
    def connect_ip(self):
        return self.__connect_ip.pure

    @property
    def token(self):
        return self.__token

    @property
    def conn(self):
        return self.__conn

    @Error.quiet
    def close(self):
        self.__conn.close()

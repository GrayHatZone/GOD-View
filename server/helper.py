'''
    General purpose methods that are
    commonly used throughout the program.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.state import ServerStatic

import time
import uuid


class SafeIP:

    def __init__(self, ip):
        self.__safe = ip.replace(':', '_')
        self.__pure = ip

    @property
    def pure(self):
        return self.__pure

    @property
    def safe(self):
        return self.__safe


class ServerHelper:

    @staticmethod
    def split(value, seperator=ServerStatic.SEPERATOR, strict=False):
        result = [el.strip() for el in value.split(seperator)]

        if strict:
            return list(filter(None, result))
        else:
            return result

    @staticmethod
    def keys(dictionary, keys):
        return (dictionary.get(key, False) for key in keys)

    @staticmethod
    def filename(ext):
        return time.strftime(f'%Y-%m-%d (%H-%M-%S).{ext}')

    @staticmethod
    def repeat(times, symbol=' '):
        return symbol * times

    @staticmethod
    def uuid():
        return str(uuid.uuid4())

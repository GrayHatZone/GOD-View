'''
    Error decorators to not disrupt the
    general flow of either client or server
    during runtime.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

import sys


class Error:

    @staticmethod
    def quiet(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception:
                pass

        return wrapper

    @staticmethod
    def quiet_thread(callback):
        def wrapper(*args, **kwargs):
            try:
                callback(*args, **kwargs)
            except Exception:
                sys.exit()

        return wrapper

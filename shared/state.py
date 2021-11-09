'''
    Global variables that will guide important parts
    of the execution behavior during runtime, for
    both the client & server.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10

    CONSTANT : GUI dependence is for
    INFO, SUCCESS, WARNING & DANGER.
'''

import platform
import sys
import os


class Static:

    IP           = '127.0.0.1'
    PORT         = 5658
    TIMEOUT      = 45
    LIVE_TIMEOUT = 15

    WINDOWS      = False
    LINUX        = False
    MAC          = False

    INFO         = 'INFO'
    SUCCESS      = 'SUCCESS'
    WARNING      = 'WARNING'
    DANGER       = 'DANGER'

    ENCODING     = 'utf-8'
    ERRORS       = 'replace'
    RAW          = 'raw:'

    SECRET       = '45799733-250a-4995-9d6c-998b1670929f'
    SALT         = '88fe3fdc-3009-4aad-a2c9-dd6e444c0986'

    INTERVAL     = '6dcd731d-3448-4b0c-8f11-2bee3accb024'
    ALIVE        = '46b700f2-1648-4935-9d2e-063d856609ae'

    DISCONNECT   = 'e97a46ad-b758-41c5-80e4-5473a169f6ea'
    UNINSTALL    = '22323c5d-1217-493d-90a6-bcbc84fcc3d5'
    RECONNECT    = '06a61bcc-b3ea-4a42-a543-73ea3a42a4fc'

    @classmethod
    def setup(cls):
        system = platform.system()

        if system == 'Windows':
            cls.WINDOWS = True
        elif system == 'Linux':
            cls.LINUX = True
        elif system == 'Darwin':
            cls.MAC = True
        else:
            raise OSError

        forward, backward = '/', '\\'
        filepath = sys.argv[0]

        if cls.WINDOWS:
            if forward in filepath:
                filepath = filepath.replace(forward, backward)
        else:
            if backward in filepath:
                filepath = filepath.replace(backward, forward)

        if os.path.isabs(filepath):
            cls.ROOT_DIR, cls.ROOT = os.path.split(filepath)
        else:
            cls.ROOT_DIR, cls.ROOT = os.path.split(
                os.path.abspath(filepath))

        cls.ROOT = os.path.join(cls.ROOT_DIR, cls.ROOT)
        cls.EXE = getattr(sys, 'frozen', False)

        if cls.EXE:
            cls.MEI = os.path.split(sys._MEIPASS)[1]

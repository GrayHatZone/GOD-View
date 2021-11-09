'''
    Variables that has important impact on during
    the execution during runtime. These should be
    set prior to building out the client.

    Verified: 2020 December 30 & 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from shared.state import Static


class ClientStatic:

    BUILD_NAME = 'Production Build'
    BUILD_VERSION = '1.0.0'
    # NOTE : Applies to pre-connect
    STICKY = True

    # NOTE : Don't change
    DEFAULT = 'Unkown'

    @classmethod
    def setup(cls):
        if Static.WINDOWS:
            # NOTE : Don't change
            cls.WEBCAM = {}

            cls.NAME = 'GOD-VIEW'
            cls.CODE_PAGE = '65001'

        # NOTE : Don't change
        if Static.TIMEOUT > 7.5:
            cls.TIMEOUT = Static.TIMEOUT - 2.5
        else:
            cls.TIMEOUT = Static.TIMEOUT

        # NOTE : Server IP
        Static.IP = Static.IP
        # NOTE : Server port
        Static.PORT = Static.PORT
        # NOTE : Server encryption secret
        Static.SECRET = Static.SECRET
        # NOTE : Server encryption salt
        Static.SALT = Static.SALT

'''
    A class used by all modules, for the simple
    reason that every module requires a token.
    it's easily extensible for future reference.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''


class Module:

    def __init__(self, token):
        self.__token = token

    @property
    def token(self):
        return self.__token

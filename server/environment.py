'''
    A utility class to manage the environment
    variables & interact with the database.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.database import Database
from server.settings import Settings
from server.error import ServerError
from server.console import Console
from shared.state import Static


class Environment:

    def __init__(self, ret):
        self.__ret = ret

        self.__db = Database()
        self.__db.create_table(Settings.TABLE_NAME,
                               **Settings.TABLE_KWARGS)
        self.__db.commit()

        self.__environment = self.__db.read(
            Settings.TABLE_NAME, fetch=1)

        if not self.__environment:
            self.__db.write(Settings.TABLE_NAME,
                            Settings.DEFAULT)
            self.__db.commit()
            self.__environment = (Settings.DEFAULT,)

    @ServerError.quiet
    def __del__(self):
        self.__db.close()

    def set(self, variable, value):
        lower_variable = variable.lower()

        if lower_variable in Settings.TABLE_KWARGS:
            upper_variable = variable.upper()
            old_value = getattr(Settings, upper_variable)

            if type(old_value) is int:
                lower_value = value.lower()

                if lower_value == 'true':
                    value = 1
                elif lower_value == 'false':
                    value = 0
                else:
                    raise ValueError('Bool Required')
            else:
                value = value.strip()

            self.__db.update(Settings.TABLE_NAME,
                             (lower_variable, '=', old_value),
                             **{lower_variable: value})
            self.__db.commit()
            setattr(Settings, upper_variable, value)

            return Console.printf('Environment variable set',
                                  Static.SUCCESS, ret=self.__ret)
        else:
            return Console.printf('Environment variable does not exist',
                                  Static.WARNING, ret=self.__ret)

    @staticmethod
    def list(ret):
        headers, values = ('Variable', 'Value'), []

        for key, value in zip(Settings.EVENIORMENT_VARIABLES,
                              Settings.environment()):
            values.append((key, (bool(value) if type(value)
                                 is int else value)))

        return Console.tabulate(values, headers, ret)

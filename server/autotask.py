'''
    A utility class to manage autotasks &
    interact with the database.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.state import ServerStatic
from server.database import Database
from server.error import ServerError
from server.console import Console
from shared.state import Static


class Autotask:

    TABLE_NAME = 'autotasks'
    TABLE_KWARGS = {
        'action': 'text'
    }

    __ARG_SEPERATOR = '>>'

    def __init__(self, ret):
        self.__ret = ret

        self.__db = Database()
        self.__db.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(
            Autotask.TABLE_NAME, Database.parse(Autotask.TABLE_KWARGS)))
        self.__db.commit()

        self.__autotask = self.__db.read(Autotask.TABLE_NAME)

    @ServerError.quiet
    def __del__(self):
        self.__db.close()

    @property
    def autotask(self):
        return self.__autotask

    def add(self, action):
        self.__db.write(Autotask.TABLE_NAME, (action.replace(
            Autotask.__ARG_SEPERATOR, ServerStatic.ARG_SEPARATOR),))
        self.__db.commit()

        return Console.printf('Autotask add complete',
                              Static.SUCCESS, ret=self.__ret)

    def remove(self, action):
        action = action.replace(Autotask.__ARG_SEPERATOR,
                                ServerStatic.ARG_SEPARATOR)

        if self.__action_exists(action):
            self.__db.delete(Autotask.TABLE_NAME,
                             ('action', '=', action))
            self.__db.commit()

            return Console.printf('Autotask remove complete',
                                  Static.SUCCESS, ret=self.__ret)
        else:
            return Console.printf('Autotask action does not exist',
                                  Static.WARNING, ret=self.__ret)

    def list(self):
        if self.autotask:
            return Console.tabulate(self.autotask,
                                    ('Action',), self.__ret)
        else:
            return Console.printf('No autoask actions exist',
                                  Static.INFO, ret=self.__ret)

    def __action_exists(self, compare_action):
        for action, in self.autotask:
            if compare_action == action:
                return True
        else:
            return False

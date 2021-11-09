'''
    A utility class to manage aliases &
    interact with the database.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.database import Database
from server.error import ServerError
from server.console import Console
from shared.state import Static


class Alias:

    __TABLE_NAME = 'aliases'
    __TABLE_KWARGS = {
        'key': 'text',
        'value': 'text'
    }

    def __init__(self, ret):
        self.__ret = ret

        self.__db = Database()
        self.__db.create_table(Alias.__TABLE_NAME,
                               **Alias.__TABLE_KWARGS)
        self.__db.commit()

        self.__alias = self.__db.read(Alias.__TABLE_NAME)

    @ServerError.quiet
    def __del__(self):
        self.__db.close()

    def add(self, key, value):
        if self.alias_exists(key):
            return Console.printf('Alias key already exists',
                                  Static.WARNING, ret=self.__ret)
        else:
            self.__db.write(Alias.__TABLE_NAME, (key, value))
            self.__db.commit()

            return Console.printf('Alias add complete',
                                  Static.SUCCESS, ret=self.__ret)

    def remove(self, key):
        if self.alias_exists(key):
            self.__db.delete(Alias.__TABLE_NAME, ('key', '=', key))
            self.__db.commit()

            return Console.printf('Alias remove complete',
                                  Static.SUCCESS, ret=self.__ret)
        else:
            return Console.printf('Alias key does not exist',
                                  Static.WARNING, ret=self.__ret)

    def update(self, key, new_key, new_value):
        if self.alias_exists(key):
            self.__db.execute('DELETE FROM {} WHERE key=? OR key=?'.format(
                Alias.__TABLE_NAME), (key, new_key))
            self.__db.write(Alias.__TABLE_NAME, (new_key, new_value))
            self.__db.commit()

            return Console.printf('Alias value update complete',
                                  Static.SUCCESS, ret=self.__ret)
        else:
            return Console.printf('Alias key does not exist',
                                  Static.WARNING, ret=self.__ret)

    def list(self):
        if self.__alias:
            return Console.tabulate(self.__alias,
                                    ('Key', 'Value'), self.__ret)
        else:
            return Console.printf('No aliases exists',
                                  Static.INFO, ret=self.__ret)

    def alias_exists(self, compare_key, ret_value=False):
        for key, value in self.__alias:
            if compare_key == key:
                if ret_value:
                    return value
                else:
                    return True
        else:
            return False

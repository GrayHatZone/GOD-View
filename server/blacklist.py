'''
    A utility class to manage blacklisted
    addresses & interact with the database.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.database import Database
from server.error import ServerError
from server.console import Console
from shared.state import Static

import ipaddress


class Blacklist:

    __TABLE_NAME = 'blacklist'
    __TABLE_KWARGS = {
        'address': 'text'
    }

    def __init__(self, ret):
        self.__ret = ret

        self.__db = Database()
        self.__db.create_table(Blacklist.__TABLE_NAME,
                               **Blacklist.__TABLE_KWARGS)
        self.__db.commit()

        self.__blacklist = [address[0] for address in
                            self.__db.read(Blacklist.__TABLE_NAME)]

    @ServerError.quiet
    def __del__(self):
        self.__db.close()

    @property
    def blacklist(self):
        return self.__blacklist

    def add(self, address):
        address = self.__verify_address(address)

        if self.__address_exists(address):
            return Console.printf('Address is already blacklisted',
                                  Static.WARNING, ret=self.__ret)
        else:
            self.__db.write(Blacklist.__TABLE_NAME, (address,))
            self.__db.commit()

            return Console.printf('Blacklist address added',
                                  Static.SUCCESS, ret=self.__ret)

    def remove(self, address):
        address = self.__verify_address(address)

        if self.__address_exists(address):
            self.__db.delete(Blacklist.__TABLE_NAME,
                             ('address', '=', address))
            self.__db.commit()

            return Console.printf('Blacklist address removed',
                                  Static.SUCCESS, ret=self.__ret)
        else:
            return Console.printf('Address is not blacklisted',
                                  Static.WARNING, ret=self.__ret)

    def update(self, address, new_address):
        address = self.__verify_address(address)
        new_address = self.__verify_address(new_address)

        if self.__address_exists(address):
            if self.__address_exists(new_address):
                return Console.printf('New address already exists',
                                      Static.WARNING, ret=self.__ret)
            else:
                self.__db.update(Blacklist.__TABLE_NAME,
                                 ('address', '=', address),
                                 address=new_address)
                self.__db.commit()
                return Console.printf('Blacklist address updated',
                                      Static.SUCCESS, ret=self.__ret)
        else:
            return Console.printf('Address is not blacklisted',
                                  Static.WARNING, ret=self.__ret)

    def list(self):
        if self.blacklist:
            headers, values = ('Address', 'IPV6', 'Link Local',
                               'Private', 'Loopback'), []

            for address in self.blacklist:
                address_obj = ipaddress.ip_address(address)

                values.append((str(address_obj),
                               str(address_obj.version == 6),
                               str(address_obj.is_link_local),
                               str(address_obj.is_private),
                               str(address_obj.is_loopback)))

            return Console.tabulate(values, headers, self.__ret)
        else:
            return Console.printf('No addresses blacklisted',
                                  Static.INFO, ret=self.__ret)

    def __address_exists(self, address):
        return address in self.blacklist

    def __verify_address(self, address):
        return str(ipaddress.ip_address(address))

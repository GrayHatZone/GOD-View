'''
    A intermediary class for general purpose
    flow control operations throughout the
    program.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * eel
'''

from server.state import ServerStatic, Dynamic
from server.console import Console

import socket
import time

if not ServerStatic.TERMINAL:
    import eel


class Controller:

    @staticmethod
    def message(ret_msg, *args, **kwargs):
        Dynamic.MESSAGES.append((ret_msg, args, kwargs))

        # NOTE : Calling this method with ret_msg
        # enabled at the same time twice will cause
        # erroneous output & should only be called
        # from the GUI, as it requires return data
        if ret_msg:
            try:
                while Dynamic.RESULT is None:
                    time.sleep(.1)
                else:
                    return Dynamic.RESULT
            finally:
                Dynamic.RESULT = None

    @staticmethod
    def exit_program():
        if Dynamic.CLIENTS:
            for unique_id in Dynamic.CLIENTS.copy():
                Controller.delete_client(unique_id, False)

        raise SystemExit

    @staticmethod
    def add_session(unique_id, allow_raise=True):
        try:
            assert unique_id in Dynamic.CLIENTS, 'Client Not Found'
            assert unique_id not in Dynamic.SESSION, \
                'Client Already In Session'

            Dynamic.SESSION.add(unique_id)

            if not ServerStatic.TERMINAL:
                if eel._websockets != []:
                    eel.sessionAddEel(unique_id)
        except Exception:
            if allow_raise:
                raise

    @staticmethod
    def remove_session(unique_id, allow_raise=True):
        try:
            Dynamic.SESSION.remove(unique_id)

            if not ServerStatic.TERMINAL:
                if eel._websockets != []:
                    eel.sessionRemoveEel(unique_id)
        except Exception:
            if allow_raise:
                raise

    @staticmethod
    def delete_client(unique_id, allow_raise=True):
        try:
            client = Dynamic.CLIENTS[unique_id]
            del Dynamic.CLIENTS[unique_id]

            try:
                client.socket.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass

            client.socket.close()
            Controller.remove_session(unique_id, False)

            if not ServerStatic.TERMINAL:
                if eel._websockets != []:
                    eel.clientRemoveEel(unique_id)

            Console.log('Disconnected Client [{} {} {}]\n'.format(
                client.connect_ip.pure, ServerStatic.SEPERATOR,
                unique_id), log_type=ServerStatic.ACTION)
        except Exception:
            if allow_raise:
                raise

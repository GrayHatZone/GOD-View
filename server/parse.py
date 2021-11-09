'''
    A core class handling the standard input loop,
    parsing the data & translating aliases. It
    also takes care of directing the execution
    of actions of the program.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * eel
'''

from server.state import ServerStatic, Dynamic
from server.controller import Controller
from server.settings import Settings
from server.console import Console
from shared.helper import Helper
from shared.state import Static
from server.alias import Alias
from shared.data import Data
import server.action

import traceback
import inspect

if not ServerStatic.TERMINAL:
    import eel


class Parse:

    @staticmethod
    def stdin():
        while True:
            result = Parse.parse_string(Parse.parse_alias(input()))
            message, lower = Data.lower(result)

            if Dynamic.SESSION:
                if lower in ServerStatic.UNIVERSAL \
                        or lower in ServerStatic.SESSION:
                    Parse.execute(lower, result, False)
                else:
                    if Settings.AUTO_SHELL:
                        Controller.message(False, result)
                    else:
                        Parse.__default_message(lower, message)
            elif lower in ServerStatic.UNIVERSAL:
                Parse.execute(lower, result, False)
            else:
                Parse.__default_message(lower, message)

    @staticmethod
    def parse_string(message):
        arguments = message.split(ServerStatic.ARG_SEPARATOR)
        arguments_dict = Data.message(arguments[0].strip())

        for argument in arguments[1:]:
            key_value_list = [el for el in argument.split() if el]
            key_value_list_len = len(key_value_list)

            if key_value_list_len == 0:
                break

            key, value = key_value_list[0], key_value_list[1:]

            if key_value_list_len == 1:
                arguments_dict[key] = True
            else:
                arguments_dict[key] = ' '.join(value)

        return arguments_dict

    @staticmethod
    def parse_alias(message):
        alias = Alias(True).alias_exists(message, True)

        if alias:
            return alias
        else:
            return message

    @staticmethod
    def execute(lower, request, gui_call, custom=None):
        try:
            if gui_call:
                lower = Data.lower(request, False)

                assert ((lower in ServerStatic.SESSION and Dynamic.SESSION)
                        or lower in ServerStatic.UNIVERSAL), \
                    'No Active Session / Request Type Not Found'

            method = getattr(server.action, lower)
            params = len(inspect.signature(method).parameters)

            if params == 0:
                return method()
            if params == 1:
                return method(request)
            if params == 2:
                return method(request, gui_call)
            else:
                return method(request, gui_call, custom)
        except SystemExit:
            raise
        except Exception:
            Console.log('Request Execution Failed\n',
                        Static.DANGER, ServerStatic.ACTION)
            Console.log(traceback.format_exc(),
                        log_type=ServerStatic.TRACEBACK)

    @staticmethod
    def __default_message(lower, message):
        if lower:
            Console.printf(Helper.join(
                f'"{message}" request type could not be found',
                'Use "help" request type for assistance'
            ), Static.WARNING)
        else:
            Console.printf(raw=True)

    if not ServerStatic.TERMINAL:
        @staticmethod
        @eel.expose
        def execute_eel(request):
            return Parse.execute(None, request, True)

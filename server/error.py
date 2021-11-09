'''
    Decorators that are used to manage errors
    during runtime. This includes logging the
    errors & providing information about the
    severity & the next step.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.controller import Controller
from server.state import ServerStatic
from server.console import Console
from shared.helper import Helper
from shared.state import Static

import traceback
import inspect
import sys


class ServerError:

    @staticmethod
    def general(callback):
        def wrapper(request=None, gui_call=None, custom=None):
            try:
                params = len(inspect.signature(callback).parameters)

                if params == 0:
                    return callback()
                if params == 1:
                    return callback(request)
                if params == 2:
                    return callback(request, gui_call)
                else:
                    return callback(request, gui_call, custom)
            except Exception as error:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)

                return Console.printf(Helper.join(
                    'Server Side Execution Failed',
                    f'{type(error).__name__}: {error}'
                ), Static.DANGER, ret=gui_call)

        return wrapper

    @staticmethod
    def quiet(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)

        return wrapper

    @staticmethod
    def quiet_thread(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)
                sys.exit()

        return wrapper

    @staticmethod
    def critical(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except KeyboardInterrupt:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)

                Console.printf(Helper.join(
                    'Keyboard Interrupt Noticed',
                    f'Exiting {ServerStatic.NAME}'
                ), Static.DANGER, False, newline=True)

                Controller.exit_program()
            except Exception as error:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)

                Console.printf(Helper.join(
                    '[STDIN] Internal Server Error',
                    f'{type(error).__name__}: {error}',
                    f'Exiting {ServerStatic.NAME}'
                ), Static.DANGER, False, newline=True)

                Controller.exit_program()

        return wrapper

    @staticmethod
    def thread(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception as error:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)

                Console.printf(Helper.join(
                    '[THREAD] Internal Server Error',
                    f'{type(error).__name__}: {error}',
                    f'{ServerStatic.NAME} Restart Recommended'
                ), Static.DANGER, newline=True)

        return wrapper

'''
    Handles everything related to the GUI,
    exposing the necessary functionality.
    Taking care of logging & middleware.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * eel
'''

from server.state import ServerStatic, Dynamic
from server.helper import ServerHelper
from server.settings import Settings
from server.error import ServerError
from server.console import Console
from shared.helper import Helper
from shared.state import Static

import traceback
import bottle
import eel


class Web:

    @staticmethod
    @eel.expose
    def clients_eel():
        return [[key, value.data] for key, value
                in Dynamic.CLIENTS.items()]

    @staticmethod
    @eel.expose
    def session_eel():
        return list(Dynamic.SESSION)

    @staticmethod
    @eel.expose
    def help_eel():
        return ServerStatic.GUI_HELP

    @staticmethod
    @eel.expose
    def host_eel():
        return ServerStatic.HOST


class Gui:

    @staticmethod
    @ServerError.thread
    def start():
        eel.init(ServerStatic.GUI_DIR)

        if ServerStatic.WEB_GUI:
            Gui.__execute_start(False)
        else:
            try:
                Gui.__execute_start('chrome')
            except EnvironmentError:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)

                Console.printf(Helper.join(
                    'Chrome browser is not installed',
                    'Converting to web GUI instance'
                ), Static.INFO, newline=True)

                ServerStatic.WEB_GUI = True
                Gui.__execute_start(False)

    @staticmethod
    def __execute_start(mode):
        eel.start(ServerStatic.GUI_PAGE,
                  mode=mode,
                  host=Static.IP,
                  port=ServerStatic.GUI_PORT,
                  app=Gui.__load_middleware(),
                  size=ServerStatic.WINDOW_SIZE,
                  close_callback=lambda *_: None)

    @staticmethod
    def __load_middleware():
        bottle_instance = bottle.default_app()
        bottle_instance.install(Middleware.verify)
        bottle_instance.install(bottle.auth_basic(Middleware.login))

        # CONSTANT : logout path is GUI dependant
        @bottle_instance.route('/logout')
        def _(): bottle.abort(401, 'Access denied')

        return bottle_instance


class Middleware:

    __IP_PROXY = ('REMOTE_ADDR',
                  'HTTP_X_FORWARDED_FOR')

    @staticmethod
    def verify(callback):
        def wrapper(*args, **kwargs):
            if Settings.GUI_WHITELIST:
                normal, proxy = ServerHelper.keys(bottle.request.environ,
                                                  Middleware.__IP_PROXY)
                gui_whitelist = Settings.GUI_WHITELIST.split(',')

                if normal in gui_whitelist or proxy in gui_whitelist:
                    return callback(*args, **kwargs)
                else:
                    Console.log('Blocked: {} [{}/{}]\n'.format(
                        bottle.request.url, normal, proxy
                    ), Static.DANGER, ServerStatic.HTTP)

                    bottle.abort(401, 'Access denied')
            else:
                return callback(*args, **kwargs)

        return wrapper

    @staticmethod
    def login(username, password):
        if (username == Settings.GUI_USERNAME and
                password == Settings.GUI_PASSWORD):
            Middleware.__resource(True)
            return True
        else:
            Middleware.__resource(False)
            return False

    @staticmethod
    def __resource(success):
        Console.log('Resource Request: {} [{}/{}]\n'.format(
            bottle.request.url, *ServerHelper.keys(bottle.request.environ,
                                                   Middleware.__IP_PROXY)
        ), Static.SUCCESS if success else Static.DANGER, ServerStatic.HTTP)

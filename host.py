# Lines: ~3700 (+ 386 Shared) + 2730 (GUI)
from server.state import ServerStatic
from shared.state import Static

Static.setup()
ServerStatic.setup()

from server.settings import Settings
Settings.set_environment()

from server.socket import ServerSocket
from server.error import ServerError
from server.console import Console
from server.parse import Parse


class Server:

    def __init__(self):
        Console.init()

    @ServerError.critical
    def run(self):
        ServerSocket().threads()
        Parse.stdin()


if __name__ == '__main__':
    Server().run()

# Lines: ~1885 (+ 386 Shared)
from client.state import ClientStatic
from shared.state import Static

try:
    Static.setup()
    ClientStatic.setup()
except OSError:
    import sys
    sys.exit()

from client.socket import ClientSocket
from client.error import ClientError
from shared.helper import Helper


class Client:

    def __init__(self):
        Helper.clear_pyinstaller_temp()

    @ClientError.critical
    def run(self):
        ClientSocket().connect()


if __name__ == '__main__':
    Client().run()

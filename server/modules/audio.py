'''
    Handles the audio stream module connection.
    Setting up the output stream & making sure
    it's cleaned up from memory & data structures.
    Independent of failure or success.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * pyaudio
'''

from server.modules.module import Module
from shared.helper import Helper
from server.state import Dynamic
from shared.error import Error
from shared.data import Data

import pyaudio


class Audio(Module):

    def __init__(self, conn, token, connect_ip):
        super().__init__(conn, token, connect_ip)
        self.__audio = pyaudio.PyAudio()

    @Error.quiet_thread
    def __recv(self, channels, rate):
        try:
            try:
                stream = self.__audio.open(format=pyaudio.paInt16,
                                           channels=channels, rate=rate,
                                           frames_per_buffer=Data.BUFFER_SIZE,
                                           output=True)

                try:
                    with self.conn as sock:
                        while True:
                            stream.write(Data.recv(sock, True, False))
                            Data.send(sock)
                finally:
                    stream.stop_stream()
                    stream.close()
            finally:
                self.__audio.terminate()
        finally:
            del Dynamic.MODULES[self.token]

    def live(self, *args):
        Helper.thread(self.__recv, *args)

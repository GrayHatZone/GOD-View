'''
    Handles the webcam stream module connection.
    Displaying the images using the opencv-python
    library & allowing some interactions with
    the window.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * opencv-python
        * numpy
'''

from server.state import ServerStatic, Dynamic
from server.modules.module import Module
from shared.helper import Helper
from shared.error import Error
from shared.data import Data

import numpy
import time
import cv2


class Webcam(Module):

    def __init__(self, conn, token, connect_ip):
        super().__init__(conn, token, connect_ip)
        self.__fps = False
        self.__flip = 0

    @Error.quiet_thread
    def __recv(self):
        try:
            with self.conn as sock:
                title = '{} {} {}'.format(
                    self.connect_ip, ServerStatic.SEPERATOR, self.token)

                while True:
                    if self.__fps:
                        timer = time.time()

                    frame = Data.recv(sock, True, False)
                    frame = numpy.frombuffer(frame, numpy.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    frame = cv2.flip(frame, self.__flip)

                    if self.__fps:
                        cv2.putText(frame, f'{1 / (time.time() - timer):.2f}',
                                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (128, 0, 0), 2)

                    cv2.imshow(title, frame)

                    key = cv2.waitKey(25) & 0xFF

                    if key == ord('q'):
                        raise SystemExit

                    if key == ord('f'):
                        self.__fps = not self.__fps

                    if key == ord('t'):
                        self.__flip = int(not self.__flip)

                    Data.send(sock)
        finally:
            del Dynamic.MODULES[self.token]

    def live(self):
        Helper.thread(self.__recv)

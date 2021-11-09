'''
    Handles the desktop stream module connection.
    Displaying the images using the opencv-python
    library & allowing some interactions with
    the window.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * opencv-python
'''

from server.state import ServerStatic, Dynamic
from server.modules.module import Module
from shared.helper import Helper
from shared.error import Error
from shared.data import Data

import numpy
import time
import cv2


class Desktop(Module):

    def __init__(self, conn, token, connect_ip):
        super().__init__(conn, token, connect_ip)
        self.__fps = True

    @Error.quiet_thread
    def __recv(self):
        try:
            with self.conn as sock:
                title = '{} {} {}'.format(
                    self.connect_ip, ServerStatic.SEPERATOR, self.token)
                cv2.namedWindow(title, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(title, *ServerStatic.WINDOW_SIZE)

                while True:
                    if self.__fps:
                        timer = time.time()

                    frame = Data.recv(sock, True, False)
                    frame = numpy.frombuffer(frame, numpy.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)

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

                    Data.send(sock)
        finally:
            del Dynamic.MODULES[self.token]

    def live(self):
        Helper.thread(self.__recv)

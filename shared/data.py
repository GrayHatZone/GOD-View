'''
    A shared resource that takes care of sending
    & receiving data from a connection. Handling
    the security, but also the packaging of data.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * cryptography
'''

from shared.state import Static

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import time
import json
import zlib


class Data:

    BUFFER_SIZE = 81920

    __SECRET = Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=Static.SALT.encode(Static.ENCODING),
        iterations=100000, backend=default_backend()
    ).derive(Static.SECRET.encode(Static.ENCODING))))
    __COMPRESSION_LEVEL = 6
    __HEADER_SIZE = 10

    @staticmethod
    def send(conn, request='', serialize=True):
        if serialize:
            request = Data.__serialize(request)

        request = Data.__compress(request)
        request = Data.__encrypt(request)

        conn.sendall('{:<{}}'.format(
            len(request), Data.__HEADER_SIZE
        ).encode(Static.ENCODING) + request)

    @staticmethod
    def recv(conn, server_sided=False, deserialize=True):
        mode = [True, 0, ''.encode(Static.ENCODING)]

        if server_sided:
            timer = time.time()

        while True:
            data = conn.recv(Data.BUFFER_SIZE)

            if mode[0]:
                mode[:2] = False, int(data[:Data.__HEADER_SIZE])

            mode[2] += data

            if len(mode[2]) - Data.__HEADER_SIZE == mode[1]:
                response = mode[2][Data.__HEADER_SIZE:]
                response = Data.__decrypt(response)
                response = Data.__decompress(response)

                if deserialize:
                    response = Data.__deserialize(response)

                return response

            if server_sided:
                if time.time() - timer > Static.TIMEOUT:
                    raise TimeoutError('Client Response Timeout')

    @staticmethod
    def parse(message, **kwargs):
        headers = {
            'status': None,
            'raw': False,
            'end': False
        }

        for header in headers:
            if header in kwargs:
                headers.update({header: kwargs[header]})
                del kwargs[header]

        return {
            'message': message,
            'headers': headers,
            **kwargs
        }

    @staticmethod
    def lower(request, include_original=True):
        message = request['message']

        if include_original:
            return (message, message.lower())
        else:
            return message.lower()

    @staticmethod
    def message(data=''):
        return {'message': data}

    @staticmethod
    def b64encode(data):
        return base64.b64encode(data).decode(Static.ENCODING)

    @staticmethod
    def b64decode(data):
        return base64.b64decode(data.encode(Static.ENCODING))

    @staticmethod
    def __serialize(data):
        return json.dumps(data).encode(Static.ENCODING)

    @staticmethod
    def __deserialize(data):
        return json.loads(data.decode(Static.ENCODING))

    @staticmethod
    def __compress(data):
        return zlib.compress(data, Data.__COMPRESSION_LEVEL)

    @staticmethod
    def __decompress(data):
        return zlib.decompress(data)

    @staticmethod
    def __encrypt(data):
        return Data.__SECRET.encrypt(data)

    @staticmethod
    def __decrypt(data):
        return Data.__SECRET.decrypt(data)

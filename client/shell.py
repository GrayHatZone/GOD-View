'''
    Handles the running of commands in
    the terminal. Timeouts, encoding &
    returning the correct data.

    Verified: 2021 February 6
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * psutil
'''

from client.state import ClientStatic
from client.error import ClientError
from shared.state import Static
from shared.error import Error
from shared.data import Data

import subprocess
import threading
import psutil
import os


class Shell:

    @staticmethod
    @ClientError.general
    def run(data, disable_stderr=False):
        if Static.WINDOWS:
            data = f'chcp {ClientStatic.CODE_PAGE} > nul && {data}'

        process_timer = threading.Timer(ClientStatic.TIMEOUT,
                                        Shell.__timeout)
        process_timer.start()

        process = subprocess.run(data, shell=True,
                                 encoding=Static.ENCODING,
                                 errors=Static.ERRORS,
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        if process_timer.is_alive():
            process_timer.cancel()

            if disable_stderr:
                if process.returncode == 0:
                    return process.stdout.strip('\r\n')
                else:
                    return ClientStatic.DEFAULT
            else:
                return Data.parse(''.join((
                    process.stdout,
                    process.stderr
                )).strip('\r\n'), raw=True)
        else:
            raise TimeoutError('Timeout Awaiting Shell Response')

    @staticmethod
    @Error.quiet
    def __timeout():
        # NOTE : Works well, only lists the
        # cmd.exe & the subprocess, for example
        # vim.exe. Does not disturb the other
        # threads the client is running
        for child in psutil.Process(
                os.getpid()).children(True):
            child.kill()

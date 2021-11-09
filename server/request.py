'''
    Handles the requests made to clients, including
    interval, autotasks, terminal & GUI. These are
    correctly interpreted to specific formats &
    is the foundation of the program.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * eel
'''

from server.state import ServerStatic, Dynamic
from server.controller import Controller
from server.helper import ServerHelper
from server.settings import Settings
from server.console import Console
from shared.helper import Helper
from shared.state import Static
from shared.data import Data

import threading
import traceback
import queue
import os

if not ServerStatic.TERMINAL:
    import eel


class Request:

    __LOADING_AMID_LENGTH = len(ServerStatic.LOADING_AMID)
    __AUTOTASK_FN = 'autotasks.txt'
    __LOCK = threading.Lock()

    def __init__(self, message, loading=ServerStatic.LOADING,
                 ret=False, callback=None, args=(), custom=None):
        self.__queue = queue.Queue()

        self.__message = message
        self.__loading = loading
        self.__callback = callback
        self.__args = args

        if custom is None:
            self.__clients = [(unique_id, Dynamic.CLIENTS[unique_id])
                              for unique_id in Dynamic.SESSION]
            self.__autotask = False
            self.__interval = False
            self.__ret = ret

            if not self.__ret:
                self.__first_stdout = True
        else:
            self.__clients = [(unique_id, Dynamic.CLIENTS[unique_id])
                              for unique_id in custom[0]]
            self.__autotask = custom[1]
            self.__interval = not self.__autotask
            self.__ret = False

        if self.__ret:
            self.__responses = []
            self.__html = False

    def send(self):
        if any((self.__ret, self.__autotask, self.__interval)):
            self.__employ_workers()
            self.__create_jobs()

            if self.__ret:
                if self.__html:
                    return dict(html=True,
                                message=Helper.join(
                                    *self.__responses))
                else:
                    return Helper.join(*self.__responses)
        else:
            with Console.LOCK:
                Console.printf(self.__loading, raw=True,
                               loading=True, lock=False)

                self.__employ_workers()
                self.__create_jobs()

                Console.printf(raw=True, lock=False)

    def __employ_workers(self):
        for _ in self.__clients:
            Helper.thread(self.__worker)

    def __create_jobs(self):
        for client in self.__clients:
            self.__queue.put(client)

        self.__queue.join()

    def __worker(self):
        try:
            unique_id, client = self.__queue.get()
            response = self.__execute_request(unique_id, client)

            if self.__ret:
                self.__responses.append(
                    self.__main_response(unique_id, client, response))
            elif self.__autotask:
                dirpath = os.path.join(ServerStatic.ARCHIVE_DIR,
                                       client.connect_ip.safe)

                if not os.path.isdir(dirpath):
                    os.makedirs(dirpath, exist_ok=True)

                Helper.write_file(
                    os.path.join(dirpath, Request.__AUTOTASK_FN),
                    'AUTOTASK ACTION: [ {} {} ]\n{}\n'.format(
                        self.__message['message'], ServerStatic.LOADING_AMID,
                        self.__main_response(unique_id, client, response)))
            elif self.__interval:
                if not ServerStatic.TERMINAL:
                    if eel._websockets != []:
                        if Settings.GUI_UPDATE:
                            response.update(dict(unique_id=unique_id))
                            eel.activityUpdateEel(response)
            else:
                with Request.__LOCK:
                    if self.__first_stdout:
                        self.__first_stdout = False
                        Console.printf(ServerHelper.repeat(
                            len(self.__loading)), raw=True,
                            loading=True, lock=False)
                    else:
                        Console.printf(ServerHelper.repeat(
                            Request.__LOADING_AMID_LENGTH),
                            raw=True, loading=True, lock=False)

                    self.__main_response(unique_id, client, response)
                    Console.printf(ServerStatic.LOADING_AMID,
                                   raw=True, loading=True,
                                   newline=True, lock=False)

            if self.__callback:
                if 'custom' in response:
                    self.__callback(client.connect_ip, unique_id,
                                    response['custom'], *self.__args)
        except Exception:
            Console.log(traceback.format_exc(),
                        log_type=ServerStatic.TRACEBACK)
        finally:
            self.__queue.task_done()

    def __main_response(self, unique_id, client, response):
        prefix = 'Response: {} {} {}'.format(client.connect_ip.pure,
                                             ServerStatic.SEPERATOR,
                                             unique_id)
        message = response['message']
        table = type(message) is list

        try:
            if message:
                if table:
                    table_response = Console.tabulate(
                        *message, self.__ret, self.__autotask, f'{prefix}\n')

                    if self.__ret:
                        if not self.__html:
                            self.__html = True

                    return table_response
                else:
                    return Console.printf(
                        f'{prefix}\n{message}', **response['headers'],
                        ret=self.__ret or self.__autotask, lock=False)
            else:
                return Console.printf(
                    f'{prefix}\nEmpty Response\n', Static.INFO, False,
                    ret=self.__ret or self.__autotask, lock=False)
        except Exception:
            Console.log('Response Handling Error\n',
                        Static.DANGER, ServerStatic.ACTION)
            Console.log(traceback.format_exc(),
                        log_type=ServerStatic.TRACEBACK)

            return Console.printf(
                f'{prefix}\nResponse Handling Error', Static.DANGER,
                False, ret=self.__ret or self.__autotask, lock=False)

    def __execute_request(self, unique_id, client):
        try:
            Data.send(client.socket, self.__message)
            response = Data.recv(client.socket, True)

            return response
        except Exception:
            Console.log('Request Execution Errror\n',
                        Static.DANGER, ServerStatic.ACTION)
            Console.log(traceback.format_exc(),
                        log_type=ServerStatic.TRACEBACK)

            try:
                Controller.delete_client(unique_id)
            except Exception:
                Console.log(traceback.format_exc(),
                            log_type=ServerStatic.TRACEBACK)
            finally:
                return Data.parse(Helper.join(
                    'Timeout / error emerged awaiting client response',
                    'Client disconnected & removed from active session'
                ), status=Static.DANGER)

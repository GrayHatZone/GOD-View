'''
    A vital class taking care of the logging
    & formatting the data, this will then be
    written to standard output or returned.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
    * Third Party Modules
        * colorama
'''

from server.state import ServerStatic, Dynamic
from server.helper import ServerHelper
from server.settings import Settings
from shared.helper import Helper
from shared.state import Static

import threading
import os

import colorama
colorama.init()


class Color:

    @staticmethod
    def green(message):
        return colorama.Fore.LIGHTGREEN_EX \
               + message + colorama.Style.RESET_ALL

    @staticmethod
    def red(message):
        return colorama.Fore.LIGHTRED_EX \
               + message + colorama.Style.RESET_ALL

    @staticmethod
    def yellow(message):
        return colorama.Fore.LIGHTYELLOW_EX \
               + message + colorama.Style.RESET_ALL

    @staticmethod
    def blue(message):
        return colorama.Fore.LIGHTBLUE_EX \
               + message + colorama.Style.RESET_ALL

    @staticmethod
    def cyan(message):
        return colorama.Fore.LIGHTCYAN_EX \
               + message + colorama.Style.RESET_ALL

    @staticmethod
    def magenta(message):
        return colorama.Fore.LIGHTMAGENTA_EX \
                + message + colorama.Style.RESET_ALL

    @staticmethod
    def white(message):
        return colorama.Fore.LIGHTWHITE_EX \
               + message + colorama.Style.RESET_ALL


class Console:

    LOCK = threading.Lock()

    __LOGS = {
        ServerStatic.TRACEBACK: 'traceback.txt',
        ServerStatic.CONSOLE: 'console.txt',
        ServerStatic.ACTION: 'action.txt',
        ServerStatic.HTTP: 'http.txt'
    }

    __STATUS = {
        Static.SUCCESS: ('[+]', '!', Color.green),
        Static.DANGER: ('[-]', '.', Color.red),
        Static.WARNING: ('[!]', '.', Color.yellow),
        Static.INFO: ('[*]', '.', Color.blue)
    }

    __END_PREFIX = (Color.red('[Server]'),
                    Color.red('[Session]'))

    __END_SUFFIX = ' {}{}'.format(
        Color.yellow(ServerStatic.NAME),
        Color.red('>'))

    __DEFAULT_STATUS = 'RAW'
    __TABLE_SEPERATOR = '-'
    __TABLE_MARGIN = 2

    @staticmethod
    def printf(message='', status=None, end=True, raw=False,
               ret=False, loading=False, newline=False, lock=True):
        if raw:
            if message:
                if not loading:
                    Console.log(message + '\n')

                if ret:
                    result = message + '\n'
                else:
                    result = Color.cyan(message)
            else:
                result = ''
        else:
            result = Console.__message(message, status, ret)

        if ret:
            return result
        else:
            if lock:
                with Console.LOCK:
                    print(Console.__newline(newline) + result,
                          end=Console.__end(message, end, raw, loading))
            else:
                print(Console.__newline(newline) + result,
                      end=Console.__end(message, end, raw, loading))

    @staticmethod
    def __message(message, status, ret, void=False):
        pure_status, color_status = Console.__status(status)

        if Settings.CONSOLE_LOG or ret:
            pure = ''

        if not (ret or void):
            color = ''

        for line in message.split('\n'):
            if line:
                if Settings.CONSOLE_LOG or ret:
                    pure += '{} {}\n'.format(
                        pure_status[0],
                        line + pure_status[1])

                if not (ret or void):
                    color += '{} {}\n'.format(
                        color_status[0],
                        Color.white(line + pure_status[1]))

        if Settings.CONSOLE_LOG:
            Console.log(pure, status)

        if not void:
            if ret:
                return pure
            else:
                return color

    @staticmethod
    def __end(message, end, raw, loading):
        if loading:
            return '\r'
        elif end:
            if message == '':
                result = ''
            elif raw:
                result = '\n\n'
            else:
                result = '\n'

            if Dynamic.SESSION:
                result += Console.__END_PREFIX[1]
            else:
                result += Console.__END_PREFIX[0]

            return result + Console.__END_SUFFIX
        elif raw:
            return '\n'
        else:
            return ''

    @staticmethod
    def __status(status):
        status = Console.__STATUS[status]
        return (status[:2], (status[2](status[0]), status[1]))

    @staticmethod
    def __newline(check):
        if check:
            return '\n'
        else:
            return ''

    @staticmethod
    def tabulate(data, headers, ret=False, text=False, prefix=''):
        lengths = Console.__max_length(data, headers)

        if Settings.CONSOLE_LOG or text:
            text_table = ''

        if ret:
            html_headers = ''
            html_rows = ''
        elif not text:
            stdout_result = ''

        for index, column in enumerate(headers):
            table_header = (
                str(column)
                + ServerHelper.repeat(lengths[index] - len(str(column)))
                + ServerHelper.repeat(Console.__TABLE_MARGIN))

            if Settings.CONSOLE_LOG or text:
                text_table += table_header

            if ret:
                html_headers += f'<th>{table_header}</th>'
            elif not text:
                stdout_result += Color.cyan(table_header)

        if Settings.CONSOLE_LOG or text:
            text_table += '\n'

        if not (ret or text):
            stdout_result += '\n'

        for length in lengths:
            table_seperator = (
                ServerHelper.repeat(length, Console.__TABLE_SEPERATOR)
                + ServerHelper.repeat(Console.__TABLE_MARGIN))

            if Settings.CONSOLE_LOG or text:
                text_table += table_seperator

            if not (ret or text):
                stdout_result += Color.white(table_seperator)

        if Settings.CONSOLE_LOG or text:
            text_table += '\n'

        if not (ret or text):
            stdout_result += '\n'

        for row in data:
            if ret:
                html_row = ''

            for index, column in enumerate(row):
                table_row = (
                    str(column)
                    + ServerHelper.repeat(lengths[index] - len(str(column)))
                    + ServerHelper.repeat(Console.__TABLE_MARGIN))

                if Settings.CONSOLE_LOG or text:
                    text_table += table_row

                if ret:
                    html_row += f'<td>{table_row}</td>'
                elif not text:
                    stdout_result += Color.cyan(table_row)

            if Settings.CONSOLE_LOG or text:
                text_table += '\n'

            if ret:
                html_rows += f'<tr>{html_row}<tr>'
            elif not text:
                stdout_result += '\n'

        if Settings.CONSOLE_LOG:
            Console.log(prefix + text_table)

        if text:
            return prefix + text_table
        elif ret:
            table = (f'<table><thead><tr>{html_headers}'
                     f'</tr></thead><tbody>{html_rows}'
                     '</tbody></table>')

            if prefix:
                return prefix + table
            else:
                return dict(html=True, message=table)
        else:
            if prefix:
                print(Color.magenta(prefix) + stdout_result, end='')
            else:
                with Console.LOCK:
                    print(stdout_result)
                    Console.printf(raw=True, lock=False)

    @staticmethod
    def __max_length(data, headers):
        result = [[len(header)] for header in headers]

        for item in data:
            for index, sub_item in enumerate(item):
                result[index].append(len(str(sub_item)))

        return [max(length) for length in result]

    @staticmethod
    def log(message, status=__DEFAULT_STATUS, log_type=ServerStatic.CONSOLE):
        if getattr(Settings, log_type):
            if not os.path.isdir(ServerStatic.LOGS_DIR):
                os.makedirs(ServerStatic.LOGS_DIR, exist_ok=True)

            Helper.write_file(os.path.join(
                ServerStatic.LOGS_DIR,
                Console.__LOGS[log_type]
            ), '{} {} {}\n{}\n'.format(
                Helper.timestamp(),
                ServerStatic.SEPERATOR,
                status, message))

    @staticmethod
    def alert(message, status):
        Console.__message(message, status, False, True)
        return dict(alert=True, message=message, type=status)

    @staticmethod
    def init():
        print(Color.green(r'''
 $$$$$$\   $$$$$$\  $$$$$$$\         $$\    $$\ $$$$$$\ $$$$$$$$\ $$\      $$\
$$  __$$\ $$  __$$\ $$  __$$\        $$ |   $$ |\_$$  _|$$  _____|$$ | $\  $$ |
$$ /  \__|$$ /  $$ |$$ |  $$ |       $$ |   $$ |  $$ |  $$ |      $$ |$$$\ $$ |
$$ |$$$$\ $$ |  $$ |$$ |  $$ |$$$$$$\\$$\  $$  |  $$ |  $$$$$\    $$ $$ $$\$$ |
$$ |\_$$ |$$ |  $$ |$$ |  $$ |\______|\$$\$$  /   $$ |  $$  __|   $$$$  _$$$$ |
$$ |  $$ |$$ |  $$ |$$ |  $$ |         \$$$  /    $$ |  $$ |      $$$  / \$$$ |
\$$$$$$  | $$$$$$  |$$$$$$$  |          \$  /   $$$$$$\ $$$$$$$$\ $$  /   \$$ |
 \______/  \______/ \_______/            \_/    \______|\________|\__/     \__|
 ''') + Color.red(r'''
          _       __
         | |     / /____ _ ____   _____ __ ___
 ______  | | /| / // __ `// __ \ / ___// // _ \
/_____/  | |/ |/ // /_/ // / / /(__  )/ //  __/
         |__/|__/ \__,_//_/ /_//____//_/ \___/
'''))

        Console.printf(ServerStatic.LOADING_AMID,
                       raw=True, loading=True, lock=False)
        Helper.clear_pyinstaller_temp()

        if not ServerStatic.TERMINAL:
            Console.printf(Helper.join(
                f'HTTP & WS Host Address: {ServerStatic.GUI_HOST}',
                f'TCP Host Address: {ServerStatic.HOST}'
            ), Static.INFO, lock=False)
        else:
            Console.printf(f'TCP Host Address: {ServerStatic.HOST}',
                           Static.INFO, lock=False)

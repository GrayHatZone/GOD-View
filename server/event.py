'''
    A vital class supporting the help command
    but also the GUI request buttons, that are
    required to execute requests.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.state import ServerStatic


class Event:

    def __init__(self, command, available, namespace, args=()):
        self.__command = command.capitalize()
        self.__available = available.capitalize()
        self.__namespace = namespace.capitalize()
        self.__args = args

    def __call__(self):
        getattr(ServerStatic,
                self.__available.upper()).append(
                    self.__command.lower())

        self.__args_str = ''.join([
            self.__required(required, (
                ServerStatic.ARG_SEPARATOR
                + name + self.__response(response, name)))
            for name, required, response in self.__args])

        ServerStatic.HELP.append((self.__available,
                                  self.__namespace,
                                  self.__command,
                                  self.__args_str))

        if not ServerStatic.TERMINAL:
            namespace = ServerStatic.GUI_HELP.get(
                self.__namespace, False)
            namespace_obj = [self.__available,
                             self.__command,
                             self.__args_str,
                             self.__args]

            if namespace:
                namespace.append(namespace_obj)
            else:
                ServerStatic.GUI_HELP[
                    self.__namespace] = [namespace_obj]

    def __response(self, response, name):
        if response:
            return f' [{name}]'
        else:
            return ''

    def __required(self, required, arg):
        if required:
            return f'{arg} '
        else:
            return f'({arg}) '

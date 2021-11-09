'''
    An important class that allows settings
    in the program & will keep the database
    updated.

    Verified: 2021 February 8
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.database import Database


class Settings:

    TABLE_NAME = 'environment'
    TABLE_KWARGS = {
        'email_alert': 'integer',
        'email_sender': 'text',
        'email_password': 'text',
        'email_receivers': 'text',
        'terminal_alert': 'integer',
        'auto_shell': 'integer',
        'gui_username': 'text',
        'gui_password': 'text',
        'gui_whitelist': 'text',
        'gui_alert': 'integer',
        'gui_update': 'integer',
        'connect_sticky': 'integer',
        'connect_refresh': 'integer',
        'http_log': 'integer',
        'action_log': 'integer',
        'console_log': 'integer',
        'traceback_log': 'integer'
    }

    EVENIORMENT_VARIABLES = ('EMAIL_ALERT',
                             'EMAIL_SENDER',
                             'EMAIL_PASSWORD',
                             'EMAIL_RECEIVERS',
                             'TERMINAL_ALERT',
                             'AUTO_SHELL',
                             'GUI_USERNAME',
                             'GUI_PASSWORD',
                             'GUI_WHITELIST',
                             'GUI_ALERT',
                             'GUI_UPDATE',
                             'CONNECT_STICKY',
                             'CONNECT_REFRESH',
                             'HTTP_LOG',
                             'ACTION_LOG',
                             'CONSOLE_LOG',
                             'TRACEBACK_LOG')

    DEFAULT = (int(),
               str(),
               str(),
               str(),
               int(True),
               int(True),
               'god',
               'view',
               str(),
               int(),
               int(True),
               int(),
               int(),
               int(True),
               int(True),
               int(True),
               int(True))

    @classmethod
    def set_environment(cls):
        db = Database()
        db.create_table(cls.TABLE_NAME,
                        **cls.TABLE_KWARGS)
        db.commit()

        values = db.read(cls.TABLE_NAME)

        if not values:
            db.write(cls.TABLE_NAME, cls.DEFAULT)
            db.commit()
            values.append(cls.DEFAULT)

        for key, value in zip((
                cls.EVENIORMENT_VARIABLES), values[0]):
            setattr(cls, key, value)

    @classmethod
    def environment(cls):
        return (cls.EMAIL_ALERT,
                cls.EMAIL_SENDER,
                cls.EMAIL_PASSWORD,
                cls.EMAIL_RECEIVERS,
                cls.TERMINAL_ALERT,
                cls.AUTO_SHELL,
                cls.GUI_USERNAME,
                cls.GUI_PASSWORD,
                cls.GUI_WHITELIST,
                cls.GUI_ALERT,
                cls.GUI_UPDATE,
                cls.CONNECT_STICKY,
                cls.CONNECT_REFRESH,
                cls.HTTP_LOG,
                cls.ACTION_LOG,
                cls.CONSOLE_LOG,
                cls.TRACEBACK_LOG)

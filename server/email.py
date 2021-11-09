'''
    To open an secure SMTP connection to the
    Gmail server, format & finally send out
    the email.

    Verified: 2021 February 7
    * Follows PEP8
    * Tested Platforms
        * Windows 10
'''

from server.state import ServerStatic
from server.error import ServerError

import smtplib
import email


class Email:

    __SMTP_SERVER = ('smtp.gmail.com', 465)
    __EMAIL_CSS = ('font-family: Arial, Helvetica, sans-serif;'
                   'background-color: rgb(31, 93, 117);'
                   'color: rgb(255, 255, 255);'
                   'font-size: 0.75rem;'
                   'font-weight: 100;'
                   'padding: 2rem;')

    def __init__(self, sender, password, recievers):
        self.__sender = sender
        self.__password = password
        self.__recievers = recievers

    @ServerError.quiet
    def send(self, subject, title, body):
        with smtplib.SMTP_SSL(*Email.__SMTP_SERVER) as smtp:
            smtp.login(self.__sender, self.__password)
            smtp.send_message(self.__email(subject, title, body))

        return True

    def __email(self, subject, title, body):
        message = email.message.EmailMessage()
        message['Subject'] = subject
        message['From'] = self.__sender
        message['To'] = self.__recievers
        message.set_content('''
            <div style="{}">
                {} {} {}
                <hr />
                {}
            </div>
        '''.format(Email.__EMAIL_CSS,
                   ServerStatic.NAME,
                   ServerStatic.SEPERATOR,
                   title, body), subtype='html')

        return message

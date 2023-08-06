from collections import namedtuple as _namedtuple
import smtplib as _smtplib

import configparser as _configparser
import ssl as _ssl
import json as _json


class EmailConst(object):
    def __init__(self, Subject, To, From, Content):
        """Generate email and send content using smtplib"""

        self.Subject = Subject
        self.To = To
        self.From = From
        self.Content = Content

    def __dict__(self) -> dict:
        return {
            "Subject": self.Subject,
             "To": self.To,
             "From": self.From,
             "Content": self.Content
        }

    def __str__(self) -> str:
        m = self.__dict__()
        return str(_namedtuple(
            "EmailConst", ["Subject", "To", "From", "Content"])(
                m.get("Subject"), m.get("To"), m.get("From"), m.get("Subject"
                )
            )
        )

    @property
    def mail(self) -> str:
        if (type(self.To) == type([]) and len(self.To) >= 2):
            to_string = str(", ".join(self.To))
        else:
            to_string = self.To
        
        return f"""\
From: {self.From}
To: {to_string}
Subject: {self.Subject}

{self.Content}"""

    def SendMail(self, Login: tuple, Content: dict = None, Mailing: tuple = ("localhost", 587)) -> bool:
        '''Send mail via mailing server, use (smtp.gmail.com, 587) for gmail hosting.
           
           NOTE: starting May 30, 2022, Google will no longer support the use of third-party apps or devices
           and the smtp.gmail.com server will be broken
        '''
 
        username, passwd = Login[0], Login[1]
        mail_server, mail_port = Mailing[0], Mailing[1]
        mail_sent = False

        if (Content is None):
            Content = self.__dict__()

        context = _ssl.create_default_context()
        with _smtplib.SMTP(mail_server, mail_port) as smtplib_server:
            smtplib_server.ehlo()
            smtplib_server.starttls(context=context)
            smtplib_server.ehlo()

            smtplib_server.login(username, passwd)
            smtplib_server.sendmail(username, Content.get("To"), self.mail)
            mail_sent = True
        return mail_sent


class LoadMail(EmailConst):
    def __init__(self, config: str, filetype: str = "ini"):
        '''Load and send mail from either a .ini file or json object'''
        filetype_opts = ["json", "ini"]
        self.configs = {"Subject": "", "To": "", "From": "", "Content": ""}
        self.config = config
        self.filetype = filetype
        
        if (str.lower(self.filetype) not in filetype_opts):
            raise ValueError(
                f"Invalid configuration type, supported types are {filetype_opts}"
            )

        # exchange for match statement in newer versions
        if (filetype == "ini"):
            configure = _configparser.ConfigParser()
            configure.read(self.config)

            #set default section
            configure = configure["mailing"]
            for mail, key in zip(["subject", "to", "from", "content"], self.configs.keys()):
                self.configs.update({key: configure[mail]})

        elif (filetype == "json"):
            with open(config, "r") as configure:
                configure = _json.load(configure)["mailing"]
                self.configs.update(
                    {
                        "Subject": configure["subject"],
                        "To": configure["to"],
                        "From": configure["from"],
                        "Content": configure["content"]
                    }
                )

        super().__init__(
            self.configs["Subject"],
            self.configs["To"],
            self.configs["From"],
            self.configs["Content"]
        )

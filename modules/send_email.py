import jinja2
import yaml
import os
import smtplib
import sys
"""
send_email.py

This module is intended to be a generic way to send emails.

The following global variables will be set by the subloader, taken from
the module_info table.
    module_id                      # ID of this module.                     default: 1
    name                           # the name of this module                default: send_sms
    description                    # a description of its function  
    provider                       # provider                               default: mailtrap.io
    smtp_server                    # SMTP server to send emails via         default: live.smtp.mailtrap.io
    port                           # SMTP port                              default: 587
    username`                      # SMTP username                          default: api
    password                       # SMTP password
    tls                            # Use TLS?                               default: true
"""

CONFIG_DIR = os.path.join(
    os.path.dirname(__file__),
    "send_email"
)

TEMPLATE_FILE = os.path.join(
    CONFIG_DIR,
    "template.html"
)
class EmailSender:

    @staticmethod
    def load_sender_config():
        """
        sender config:
        `send_email:
          username:
          password:
          port:
          smtp_server:
        """
        with open(CONFIG_FILE, "r") as _o:
            return yaml.load(_o, Loader = yaml.Loader)

    def __init__(self):
        # self.config = self.load_sender_config()
        # for k, v in self.config['send_email'].items():
        #     setattr(self, k, v)
        self.port = port
        self.username = username
        self.smtp = smtplib.SMTP(smtp_server,
                            port)
        self.login()

    def login(self):
        self.smtp.connect(smtp_server, self.port)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(self.username, password)
        self.smtp.ehlo()
        print(f"Logged in with user {self.username}")

    def send(self,
             to = "James Mattison <james.mattison7@gmail.com>",
             from_ = "Magic Elves <api@slovendor.com>",
             msg = "Test message"):

        o = """
        Subject: Testing emails
        To: {to}
        From: {from_}
        """
        receiver = to
        sender = from_
        blob = self.smtp.sendmail(sender, receiver, o)
        print(blob)

class PortalTemplate:

    def __init__(self):
        self.template_file = f"{CONFIG_DIR}/template.html"
        self.template = self._load_template()

    def _load_template(self):
        with open(self.template_file, "r") as _o:
            blob = _o.read()
        temp = jinja2.Template(blob)
        return temp

    def render(self, **kwargs):
        loader = jinja2.FileSystemLoader(searchpath = "send_email/")
        env = jinja2.Environment(loader = loader)
        f = env.get_template("template.html")
        rendered = f.render(**kwargs)
        return rendered

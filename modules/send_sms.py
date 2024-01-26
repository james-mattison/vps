from .subloader import Subloader
import sys
sys.path.insert(0, "..")
from lib.db import DB

from twilio.rest import Client

if not Subloader.module_enabled("send_sms"):
    raise Exception(f"Module send_sms is not enabled!")

class MessageSender:

    def __init__(self):
        self.db = DB("additional_info")
        self.sid, self.secret = self.get_creds()

    def get_creds(self):
        twilio_sid = self.db.select_where("module_info", info_key="twilio_sid")['info_value']
        twilio_secret = self.db.select_where("module_info", info_key="twilio_secret")['info_value']

        return twilio_sid, twilio_secret

    def send_message(self, to, from_, message):
        client = Client(self.sid, self.secret)
        m = client.messages.create(
            body = message,
            to = to,
            from_ = from_
        )
        print(m.sid)


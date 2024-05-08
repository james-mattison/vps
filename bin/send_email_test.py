import mailtrap as mt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("to", action = "store")
parser.add_argument("msg", action = "store")

args = parser.parse_args()


mail = mt.Mail(
    sender=mt.Address(email="api@slovendor.com", name="VPS Management Agent"),
    to=[mt.Address(email=args.to)],
    subject="Vendor Product Systems Information",
    text=args.msg,
    category="Integration Test",
)

client = mt.MailtrapClient(
    token = "e0685efa3d208635ed1b0c7d3ba0490c"
    )

client.send(mail)

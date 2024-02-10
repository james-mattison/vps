print("send_sms")
import sinch

def send_msg():
    c = sinch.Client(
        key_id = "88af58e9-ab0a-4939-8b0b-e843ce619783",
        key_secret = "EUUgEcU23cTyKWML8dX1TDedsw",
        project_id = "6984d913-fe68-4184-a0a4-a7b449420566")

    r = c.sms.batches.send(
        body = "test",
        to = ["+18185125437"],
        from_ = "+18054296325",
        delivery_report = "none"
    )

    print(r)
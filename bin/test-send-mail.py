import mailtrap as mt

mail = mt.Mail(
    sender=mt.Address(email="api@slovendor.com", name="Alert for You"),
    to=[mt.Address(email="james.mattison7@gmail.com")],
    subject="Another Goatse'd Test",
    text="Congrats for sending the Goat Man with the mailtrap!",
    category="Integration Test",
)

client = mt.MailtrapClient(
    token = "e0685efa3d208635ed1b0c7d3ba0490c"
    )

client.send(mail)
es
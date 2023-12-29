from os import environ

from flask_mail import Mail, Message


class EmailSender:
    def __init__(self, app):
        self.sender = environ.get("MAIL_USERNAME")
        app.config["MAIL_SERVER"] = environ.get("MAIL_SERVER")
        app.config["MAIL_PORT"] = int(environ.get("MAIL_PORT"))
        app.config["MAIL_USERNAME"] = environ.get("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = environ.get("MAIL_PASSWORD")
        app.config["MAIL_USE_TLS"] = environ.get("MAIL_USE_TLS") == "True"
        app.config["MAIL_USE_SSL"] = environ.get("MAIL_USE_SSL") == "True"
        self.mail = Mail(app)

    def send(self, recipient: str, subject: str, body: str):
        message = Message(
            sender=self.sender, recipients=[recipient], subject=subject, body=body
        )
        self.mail.send(message)

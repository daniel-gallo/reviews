class FakeEmailSender:
    def __init__(self):
        self.sent_messages = []

    def send(self, recipient: str, subject: str, body: str):
        self.sent_messages.append(
            {"recipient": recipient, "subject": subject, "body": body}
        )

        print(
            f"""
            To: {recipient}
            Subject: {subject}
            Body: {body}
            """
        )

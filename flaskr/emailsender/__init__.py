from .real import EmailSender
from .fake import FakeEmailSender

__all__ = ["EmailSender", "FakeEmailSender"]

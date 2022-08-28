import os
from typing import Optional

import requests
import ujson


class Mailer:
    # The mailer service to use. Should be the module name of an API wrapper
    # class that responds to `.send_mail`.
    MAILER_SERVICE = os.getenv("MAILER_SERVICE", "mailgun")

    @classmethod
    def send_mail(cls, **args) -> bool:
        """Send an email using the configured mailer service."""
        if cls.MAILER_SERVICE == "mailgun":
            return Mailgun.send_mail(**args)
        elif cls.MAILER_SERVICE == "sendgrid":
            return Sendgrid.send_mail(**args)


class Sendgrid:
    BASE_URL = os.getenv("SENDGRID_BASE_URL", "https://api.sendgrid.com")
    VERSION = os.getenv("SENDGRID_VERSION", "v3")
    AUTH_KEY = os.environ["SENDGRID_API_KEY"]
    DEFAULT_SENDER = os.environ["DEFAULT_SENDER"]

    @classmethod
    def send_mail(
        cls,
        recipient: str,
        subject: str,
        body: str,
        sender: Optional[str] = None,
    ) -> bool:
        url = f"{cls.BASE_URL}/{cls.VERSION}/mail/send"
        headers = {
            "Authorization": f"Bearer {cls.AUTH_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": sender or cls.DEFAULT_SENDER},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}],
        }
        resp = requests.post(url, headers=headers, data=ujson.dumps(data))
        return resp.status_code == requests.codes.accepted


class Mailgun:
    BASE_URL = os.getenv("MAILGUN_BASE_URL", "https://api.mailgun.net")
    VERSION = os.getenv("MAILGUN_VERSION", "v3")
    DOMAIN = os.environ["MAILGUN_DOMAIN"]
    AUTH_KEY = os.environ["MAILGUN_API_KEY"]
    DEFAULT_SENDER = os.environ["DEFAULT_SENDER"]

    @classmethod
    def send_mail(
        cls,
        recipient: str,
        subject: str,
        body: str,
        sender: Optional[str] = None,
    ) -> bool:
        url = f"{cls.BASE_URL}/{cls.VERSION}/{cls.DOMAIN}/messages"
        data = {
            "from": sender or cls.DEFAULT_SENDER,
            "to": recipient,
            "subject": subject,
            "text": body,
        }
        resp = requests.post(url, auth=("api", cls.AUTH_KEY), data=data)
        return resp.status_code == requests.codes.ok

import os
from typing import Optional

import requests


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
    ):
        url = f"{cls.BASE_URL}/{cls.VERSION}/{cls.DOMAIN}/messages"
        data = {
            "from": sender or cls.DEFAULT_SENDER,
            "to": recipient,
            "subject": subject,
            "text": body,
        }
        resp = requests.post(url, auth=("api", cls.AUTH_KEY), data=data)
        return resp.status_code == requests.codes.ok


mailer = Mailgun

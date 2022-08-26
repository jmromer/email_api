import os
from typing import Optional

import requests
import ujson


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
    ):
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


mailer = Sendgrid

import os

from bs4 import BeautifulSoup
from email_validator import EmailNotValidError, validate_email
from fastapi import FastAPI
from pydantic import BaseModel


class Email(BaseModel):
    to_email: str  # TODO: rename to `to`
    to_name: str
    from_email: str  # TODO: rename to `from`
    from_name: str
    subject: str
    body: str


# The mailer service to use. Should be the module name of an API wrapper class
# that responds to `.send_mail`.
MAILER_SERVICE = os.getenv("MAILER_SERVICE", "mailgun")

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.post("/email")
async def send_email(email: Email):
    try:
        # minimally validate email addresses
        from_validated = validate_email(email.from_email, check_deliverability=False)
        to_validated = validate_email(email.to_email, check_deliverability=False)
    except EmailNotValidError as e:
        return {"status": "error", "message": str(e)}

    # send an email using the configured mailer service
    mailer = getattr(__import__("lib"), MAILER_SERVICE).mailer
    if mailer.send_mail(
        sender=f"{email.from_name} <{from_validated.email}>",
        recipient=f"{email.to_name} <{to_validated.email}>",
        subject=email.subject,
        body=BeautifulSoup(email.body, features="html.parser").get_text("\n"),
    ):
        return {"status": "success", "message": "message send enqueued"}
    else:
        return {"status": "error", "message": "message send failed"}

from bs4 import BeautifulSoup
from email_validator import EmailNotValidError, validate_email
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from lib.mailer import Mailer


class Email(BaseModel):
    to_email: str = Field(str, alias="to")
    to_name: str
    from_email: str = Field(str, alias="from")
    from_name: str
    subject: str
    body: str


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
        raise HTTPException(status_code=422, detail=str(e))

    success = Mailer.send_mail(
        sender=f"{email.from_name} <{from_validated.email}>",
        recipient=f"{email.to_name} <{to_validated.email}>",
        subject=email.subject,
        body=BeautifulSoup(email.body, features="html.parser").get_text("\n"),
    )

    if not success:
        raise HTTPException(status_code=422, detail="message send failed")

    return {"status": "success", "message": "message send enqueued"}

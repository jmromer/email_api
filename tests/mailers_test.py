import pytest
import requests

from lib.mailers import Mailgun, Sendgrid


@pytest.mark.vcr
def test_mailgun_send_mail_success():
    assert Mailgun.send_mail(
        recipient="Jake Romer <jake@conclave.digital>",
        subject="A question?",
        body="Is this your email address?",
    )


@pytest.mark.vcr
def test_sendgrid_send_mail_success():
    assert Sendgrid.send_mail(
        recipient="jake@conclave.digital",
        subject="A question?",
        body="Is this your email address?",
    )

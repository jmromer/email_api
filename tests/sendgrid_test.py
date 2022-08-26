import pytest
import requests
from lib.sendgrid import Sendgrid


@pytest.mark.vcr
def test_sendgrid_send_mail_success():
    assert Sendgrid.send_mail(
        recipient="jake@conclave.digital",
        subject="A question?",
        body="Is this your email address?",
    )

import pytest
import requests

from lib.mailgun import Mailgun


@pytest.mark.vcr
def test_mailgun_send_mail_success():
    assert Mailgun.send_mail(
        recipient="Jake Romer <jake@conclave.digital>",
        subject="A question?",
        body="Is this your email address?",
    )

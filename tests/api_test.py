import pytest
from httpx import AsyncClient

import lib
from lib.api import app


@pytest.mark.anyio
async def test_healthcheck():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_send_email(mocker):
    message = {
        "to_email": "fake@example.com",
        "to_name": "Mr. Fake",
        "from_email": "no-reply@fake.com",
        "from_name": "Ms. Fake",
        "subject": "A message from The Fake Family",
        "body": "<h1>Your Bill</h1><p>$10</p>",
    }
    mocker.patch("lib.mailgun.mailer")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/email", json=message)

    assert response.status_code == 200
    lib.mailgun.mailer.send_mail.assert_called_once_with(
        sender="Ms. Fake <no-reply@fake.com>",
        recipient="Mr. Fake <fake@example.com>",
        subject="A message from The Fake Family",
        body="Your Bill\n$10",
    )

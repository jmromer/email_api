import os

import pytest
from httpx import AsyncClient

import email_api
from email_api.api import app
from email_api.mailers import UnrecognizedMailer


@pytest.mark.anyio
async def test_healthcheck():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_send_email_success(mocker):
    mocker.patch("email_api.mailers.Mailgun")
    message = {
        "to": "fake@example.com",
        "to_name": "Mr. Fake",
        "from": "no-reply@fake.com",
        "from_name": "Ms. Fake",
        "subject": "A message from The Fake Family",
        "body": "<h1>Your Bill</h1><p>$10</p>",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/email", json=message)

    assert response.status_code == 200
    email_api.mailers.Mailgun.send_mail.assert_called_once_with(
        sender="Ms. Fake <no-reply@fake.com>",
        recipient="Mr. Fake <fake@example.com>",
        subject="A message from The Fake Family",
        body="Your Bill\n$10",
    )


@pytest.mark.anyio
async def test_send_email_success_with_sendgrid(mocker, monkeypatch):
    monkeypatch.setenv("MAILER_SERVICE", "Sendgrid")
    mocker.patch("email_api.mailers.Sendgrid")
    message = {
        "to": "fake@example.com",
        "to_name": "Mr. Fake",
        "from": "no-reply@fake.com",
        "from_name": "Ms. Fake",
        "subject": "A message from The Fake Family",
        "body": "<h1>Your Bill</h1><p>$10</p>",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/email", json=message)

    assert response.status_code == 200
    email_api.mailers.Sendgrid.send_mail.assert_called_once_with(
        sender="Ms. Fake <no-reply@fake.com>",
        recipient="Mr. Fake <fake@example.com>",
        subject="A message from The Fake Family",
        body="Your Bill\n$10",
    )


@pytest.mark.anyio
async def test_send_email_failre_with_invalid_mailer(mocker, monkeypatch):
    monkeypatch.setenv("MAILER_SERVICE", "Mailchimps")
    message = {
        "to": "fake@example.com",
        "to_name": "Mr. Fake",
        "from": "no-reply@fake.com",
        "from_name": "Ms. Fake",
        "subject": "A message from The Fake Family",
        "body": "<h1>Your Bill</h1><p>$10</p>",
    }

    with pytest.raises(UnrecognizedMailer):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/email", json=message)


@pytest.mark.anyio
async def test_send_email_invalid_request(mocker):
    message = {
        "to": "",
        "to_name": "Mr. Fake",
        "from": "no-reply@fake.com",
        "from_name": "Ms. Fake",
        "subject": "A message from The Fake Family",
        "body": "<h1>Your Bill</h1><p>$10</p>",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/email", json=message)

    assert response.status_code == 422
    assert "email address is not valid" in response.json().get("detail")

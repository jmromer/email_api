import os


def test():
    os.system("poetry run pytest")


def start():
    os.system("poetry run uvicorn email_api.api:app")

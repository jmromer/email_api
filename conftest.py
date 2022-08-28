import pytest
from dotenv import load_dotenv

load_dotenv(".env.test")


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["Authorization"]}

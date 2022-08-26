import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["Authorization"]}

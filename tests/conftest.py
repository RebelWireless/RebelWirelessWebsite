import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def mock_discord():
    with patch("app.utils.discord.send_signup_to_discord") as signup_mock, \
         patch("app.utils.discord.send_contact_to_discord") as contact_mock:
        yield signup_mock, contact_mock

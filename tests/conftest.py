import pytest
from fastapi.testclient import TestClient

import app.services.notification_service as notification_service
from app.config import Config
from app.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_bot(mocker):
    mock = mocker.AsyncMock()
    mocker.patch.object(notification_service, 'bot', mock)
    return mock


@pytest.fixture
def mock_config(mocker):
    mocker.patch.object(Config, 'GROUP_IDS',)
    mocker.patch.object(Config, 'BOT_TOKEN',)

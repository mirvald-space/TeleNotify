from unittest.mock import AsyncMock

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_send_notification_success(client, mocker):
    mock_bot = AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"message": "Test notification"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=-4221944088, text="Test notification")


def test_send_notification_empty_message(client):
    response = client.post("/send_notification", json={"message": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message cannot be empty"}


def test_send_notification_missing_message(client):
    response = client.post("/send_notification", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_send_notification_failure(client, mocker):
    mock_bot = AsyncMock()
    mock_bot.send_message.side_effect = Exception("Failed to send message")
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"message": "Test notification"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Failed to send notification to some groups"}

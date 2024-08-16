import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_send_notification_success(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"message": "Test notification"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_send_notification_with_slack_params(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification", json={
        "channel": "#test-channel",
        "username": "test-bot",
        "text": "Test notification with Slack params",
        "icon_emoji": ":test:",
        "link_names": True,
        "mrkdwn": True
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once()


def test_send_notification_empty_message(client):
    response = client.post("/send_notification", json={"message": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message cannot be empty"}


def test_send_notification_missing_message_and_text(client):
    response = client.post("/send_notification", json={
        "channel": "#test-channel",
        "username": "test-bot"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_failure(client, mocker):
    mock_bot = mocker.AsyncMock()
    mock_bot.send_message.side_effect = Exception("Failed to send message")
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"message": "Test notification"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Failed to send notification to some groups"}

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_send_notification_with_text_query(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification?text=Test notification using query")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=mocker.ANY, text="Test notification using query")


@pytest.mark.asyncio
async def test_send_notification_with_text_body(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"text": "Test notification using body"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=mocker.ANY, text="Test notification using body")


@pytest.mark.asyncio
async def test_send_notification_with_message_body(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification", json={"message": "Test notification using message field"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=mocker.ANY, text="Test notification using message field")


@pytest.mark.asyncio
async def test_send_notification_text_priority(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification", json={
        "text": "Priority text",
        "message": "Secondary message"
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=mocker.ANY, text="Priority text")


@pytest.mark.asyncio
async def test_send_notification_with_slack_params(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification", json={
        "text": "Test notification with Slack params",
        "channel": "#test-channel",
        "username": "test-bot",
        "icon_emoji": ":test:",
        "link_names": True,
        "mrkdwn": True
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=mocker.ANY, text="Test notification with Slack params")


def test_send_notification_empty_message(client):
    response = client.post("/send_notification", json={"text": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


def test_send_notification_missing_text(client):
    response = client.post("/send_notification", json={
        "channel": "#test-channel",
        "username": "test-bot"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_failure(client, mocker):
    mock_bot = mocker.AsyncMock()
    mock_bot.send_message.side_effect = Exception("Failed to send message")
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"text": "Test notification"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Failed to send notification to some groups"}


@pytest.mark.asyncio
async def test_send_notification_empty_query(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification?text=")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_query_priority(client, mocker):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification?text=Query text", json={"text": "Body text"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    mock_bot.send_message.assert_called_once_with(
        chat_id=mocker.ANY, text="Query text")

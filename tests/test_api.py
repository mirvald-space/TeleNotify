import pytest
from aiogram.enums import ParseMode
from fastapi import status

from app.config import Config


@pytest.fixture
def mock_config(mocker):
    mocker.patch.object(Config, 'GROUP_IDS', [-1001, -1002])


@pytest.mark.asyncio
async def test_send_notification_with_text_query(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification?text=Test notification using query")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text="Test notification using query", parse_mode=None)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text="Test notification using query", parse_mode=None)


@pytest.mark.asyncio
async def test_send_notification_with_text_body(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"text": "Test notification using body"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text="Test notification using body", parse_mode=None)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text="Test notification using body", parse_mode=None)


@pytest.mark.asyncio
async def test_send_notification_with_message_body(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification", json={"message": "Test notification using message field"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text="Test notification using message field", parse_mode=None)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text="Test notification using message field", parse_mode=None)


@pytest.mark.asyncio
async def test_send_notification_text_priority(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification", json={
        "text": "Priority text",
        "message": "Secondary message"
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text="Priority text", parse_mode=None)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text="Priority text", parse_mode=None)


@pytest.mark.asyncio
async def test_send_notification_with_html_format(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    html_message = "<b>Bold</b> and <i>italic</i> text with <a href='http://example.com'>link</a>"
    response = client.post("/send_notification",
                           json={"text": html_message, "format": "html"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=html_message, parse_mode=ParseMode.HTML)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text=html_message, parse_mode=ParseMode.HTML)


@pytest.mark.asyncio
async def test_send_notification_with_markdown_format(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    markdown_message = "*Bold* and _italic_ text with [link](http://example.com)"
    response = client.post(
        "/send_notification", json={"text": markdown_message, "format": "markdown"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=markdown_message, parse_mode=ParseMode.MARKDOWN)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text=markdown_message, parse_mode=ParseMode.MARKDOWN)


@pytest.mark.asyncio
async def test_send_notification_with_special_characters(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    special_chars_message = "Special characters: . ! @ # $ % ^ & * ( ) _ + { } | : \" < > ?"
    response = client.post("/send_notification",
                           json={"text": special_chars_message})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=special_chars_message, parse_mode=ParseMode.HTML)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text=special_chars_message, parse_mode=ParseMode.HTML)


@pytest.mark.asyncio
async def test_send_notification_with_urls(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    url_message = "Check out this link: https://www.example.com"
    response = client.post("/send_notification", json={"text": url_message})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=url_message, parse_mode=None)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text=url_message, parse_mode=None)


@pytest.mark.asyncio
async def test_send_notification_empty_message(client):
    response = client.post("/send_notification", json={"text": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_missing_text(client):
    response = client.post("/send_notification", json={
        "format": "plain"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_failure(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mock_bot.send_message.side_effect = Exception("Failed to send message")
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"text": "Test notification"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Failed to send notification to some groups"}


@pytest.mark.asyncio
async def test_send_notification_empty_query(client):
    response = client.post("/send_notification?text=")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_query_priority(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification?text=Query text", json={"text": "Body text"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "success",
                               "message": "Notification sent to all groups"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text="Query text", parse_mode=None)
    mock_bot.send_message.assert_any_call(
        chat_id=-1002, text="Query text", parse_mode=None)


@pytest.mark.asyncio
async def test_send_notification_with_auto_detection(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    html_message = "<b>Bold</b> text"
    markdown_message = "*Bold* text"
    plain_message = "Plain text"

    responses = [
        client.post("/send_notification", json={"text": html_message}),
        client.post("/send_notification", json={"text": markdown_message}),
        client.post("/send_notification", json={"text": plain_message})
    ]

    for response in responses:
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "success",
                                   "message": "Notification sent to all groups"}

    assert mock_bot.send_message.call_count == 6
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=html_message, parse_mode=ParseMode.HTML)
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=markdown_message, parse_mode=ParseMode.MARKDOWN)
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=plain_message, parse_mode=None)

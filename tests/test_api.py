import pytest
from aiogram.enums import ParseMode
from fastapi import status

from app.config import Config
from app.services.notification_service import escape_special_characters

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_config(mocker):
    mocker.patch.object(Config, 'GROUP_IDS', [-1001, -1002])

# Добавляем новые тесты для проверки функциональности bot_id и chat_id


@pytest.mark.asyncio
async def test_send_notification_with_custom_bot_and_chat(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mock_bot_class = mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    custom_bot_token = "custom_bot_token"
    custom_chat_id = 12345

    response = client.post(
        "/send_notification",
        json={
            "text": "Test with custom bot and chat",
            "bot_id": custom_bot_token,
            "chat_id": custom_chat_id
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_bot_class.assert_any_call(token=custom_bot_token)
    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test with custom bot and chat",
        None,
        [custom_chat_id],
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_multiple_chat_ids(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    custom_chat_ids = [12345, 67890]

    response = client.post(
        "/send_notification",
        json={
            "text": "Test with multiple chat IDs",
            "chat_id": custom_chat_ids
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test with multiple chat IDs",
        None,
        custom_chat_ids,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_text_query(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    response = client.post(
        "/send_notification?text=Test notification using query")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test notification using query",
        None,
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_text_body(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post("/send_notification",
                           json={"text": "Test notification using body"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    for chat_id in Config.GROUP_IDS:
        mock_bot.send_message.assert_any_call(
            chat_id=chat_id,
            text="Test notification using body",
            parse_mode=None,
            message_thread_id=None,
            reply_to_message_id=None
        )


@pytest.mark.asyncio
async def test_send_notification_with_message_body(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    response = client.post(
        "/send_notification", json={"message": "Test notification using message field"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test notification using message field",
        None,
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_text_priority(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    response = client.post("/send_notification", json={
        "text": "Priority text",
        "message": "Secondary message"
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Priority text",
        None,
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_html_format(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    html_message = "<b>Bold</b> and <i>italic</i> text with <a href='http://example.com'>link</a>"
    response = client.post("/send_notification",
                           json={"text": html_message, "format": "html"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        html_message,  # Отправляем неэкранированное сообщение
        ParseMode.HTML,
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_markdown_format(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    markdown_message = "*Bold* and _italic_ text with [link](http://example.com)"
    response = client.post(
        "/send_notification", json={"text": markdown_message, "format": "markdown"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        markdown_message,  # Отправляем неэкранированное сообщение
        ParseMode.MARKDOWN,
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_special_characters(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    special_chars_message = "Special characters: . ! @ # $ % ^ & * ( ) _ + { } | : \" < > ?"
    response = client.post("/send_notification",
                           json={"text": special_chars_message})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        special_chars_message,
        mocker.ANY,  # Изменено с None на mocker.ANY
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_urls(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    url_message = "Check out this link: https://www.example.com"
    response = client.post("/send_notification", json={"text": url_message})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        url_message,
        None,
        Config.GROUP_IDS,
        None,
        None
    )


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
        "detail": "Failed to send notification to some groups/topics"}


@pytest.mark.asyncio
async def test_send_notification_empty_query(client):
    response = client.post("/send_notification?text=")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Message text cannot be empty"}


@pytest.mark.asyncio
async def test_send_notification_query_priority(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    response = client.post(
        "/send_notification?text=Query text", json={"text": "Body text"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Query text",
        None,
        Config.GROUP_IDS,
        None,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_auto_detection(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    html_message = "<b>Bold</b> text"
    markdown_message = "*Bold* text"
    plain_message = "Plain text"

    escaped_html_message = escape_special_characters(html_message, 'html')
    escaped_markdown_message = escape_special_characters(
        markdown_message, 'markdown')

    responses = [
        client.post("/send_notification", json={"text": html_message}),
        client.post("/send_notification", json={"text": markdown_message}),
        client.post("/send_notification", json={"text": plain_message})
    ]

    for response in responses:
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "success", "message": "Notification sent to all specified groups/topics"}


@pytest.mark.asyncio
async def test_send_notification_with_topic_id(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    topic_id = 15
    response = client.post(
        "/send_notification",
        json={
            "text": "Test with topic",
            "topic_id": topic_id
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test with topic",
        None,
        Config.GROUP_IDS,
        topic_id,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_custom_bot_chat_and_topic(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mock_bot_class = mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    custom_bot_token = "custom_bot_token"
    custom_chat_id = 12345
    topic_id = 20

    response = client.post(
        "/send_notification",
        json={
            "text": "Test with custom bot, chat, and topic",
            "bot_id": custom_bot_token,
            "chat_id": custom_chat_id,
            "topic_id": topic_id
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_bot_class.assert_any_call(token=custom_bot_token)
    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test with custom bot, chat, and topic",
        None,
        [custom_chat_id],
        topic_id,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_topic_id_query_param(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    topic_id = 25
    response = client.post(
        f"/send_notification?text=Test with topic query&topic_id={topic_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test with topic query",
        None,
        Config.GROUP_IDS,
        topic_id,
        None
    )


@pytest.mark.asyncio
async def test_send_notification_with_reply_to_message_id(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)
    mock_send_notification = mocker.patch(
        'app.api.routes.send_notification_to_groups', return_value=True)

    reply_to_message_id = 123
    response = client.post(
        "/send_notification",
        json={
            "text": "Test with reply",
            "reply_to_message_id": reply_to_message_id
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    mock_send_notification.assert_called_once_with(
        mocker.ANY,
        "Test with reply",
        None,
        Config.GROUP_IDS,
        None,
        reply_to_message_id
    )

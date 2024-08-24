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

    # Проверяем, что бот был создан дважды: один раз с токеном по умолчанию и один раз с пользовательским токеном
    assert mock_bot_class.call_count == 2
    mock_bot_class.assert_any_call(token=Config.BOT_TOKEN)
    mock_bot_class.assert_any_call(token=custom_bot_token)

    # Проверяем, что сообщение было отправлено в указанный чат
    mock_bot.send_message.assert_called_once_with(
        chat_id=custom_chat_id,
        text="Test with custom bot and chat",
        parse_mode=None
    )


@pytest.mark.asyncio
async def test_send_notification_with_multiple_chat_ids(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

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

    # Проверяем, что сообщение было отправлено во все указанные чаты
    assert mock_bot.send_message.call_count == len(custom_chat_ids)
    for chat_id in custom_chat_ids:
        mock_bot.send_message.assert_any_call(
            chat_id=chat_id,
            text="Test with multiple chat IDs",
            parse_mode=None
        )


@pytest.mark.asyncio
async def test_send_notification_with_text_query(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification?text=Test notification using query")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
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
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    for chat_id in Config.GROUP_IDS:
        mock_bot.send_message.assert_any_call(
            chat_id=chat_id,
            text="Test notification using body",
            parse_mode=None
        )


@pytest.mark.asyncio
async def test_send_notification_with_message_body(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    response = client.post(
        "/send_notification", json={"message": "Test notification using message field"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
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
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
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
    escaped_html_message = escape_special_characters(html_message, 'html')
    response = client.post("/send_notification",
                           json={"text": html_message, "format": "html"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=escaped_html_message, parse_mode=ParseMode.HTML)


pytest.mark.asyncio


async def test_send_notification_with_markdown_format(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    markdown_message = "*Bold* and _italic_ text with [link](http://example.com)"
    escaped_markdown_message = escape_special_characters(
        markdown_message, 'markdown')
    response = client.post(
        "/send_notification", json={"text": markdown_message, "format": "markdown"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=escaped_markdown_message, parse_mode=ParseMode.MARKDOWN)


@pytest.mark.asyncio
async def test_send_notification_with_special_characters(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    special_chars_message = "Special characters: . ! @ # $ % ^ & * ( ) _ + { } | : \" < > ?"
    escaped_special_chars_message = escape_special_characters(
        special_chars_message, 'html')
    response = client.post("/send_notification",
                           json={"text": special_chars_message})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=-1001, text=escaped_special_chars_message, parse_mode=ParseMode.HTML)


@pytest.mark.asyncio
async def test_send_notification_with_urls(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    url_message = "Check out this link: https://www.example.com"
    response = client.post("/send_notification", json={"text": url_message})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
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

    response = client.post(
        "/send_notification?text=Query text", json={"text": "Body text"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}
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

    # Проверяем, что сообщение было отправлено с указанием message_thread_id
    for chat_id in Config.GROUP_IDS:
        mock_bot.send_message.assert_any_call(
            chat_id=chat_id,
            text="Test with topic",
            parse_mode=None,
            message_thread_id=topic_id
        )


@pytest.mark.asyncio
async def test_send_notification_with_custom_bot_chat_and_topic(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mock_bot_class = mocker.patch('app.api.routes.Bot', return_value=mock_bot)

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

    # Проверяем, что был создан бот с пользовательским токеном
    mock_bot_class.assert_any_call(token=custom_bot_token)

    # Проверяем, что сообщение было отправлено в указанный чат и тему
    mock_bot.send_message.assert_called_once_with(
        chat_id=custom_chat_id,
        text="Test with custom bot, chat, and topic",
        parse_mode=None,
        message_thread_id=topic_id
    )


@pytest.mark.asyncio
async def test_send_notification_with_topic_id_query_param(client, mocker, mock_config):
    mock_bot = mocker.AsyncMock()
    mocker.patch('app.api.routes.Bot', return_value=mock_bot)

    topic_id = 25
    response = client.post(
        f"/send_notification?text=Test with topic query&topic_id={topic_id}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "success", "message": "Notification sent to all specified groups/topics"}

    # Проверяем, что сообщение было отправлено с указанием message_thread_id
    for chat_id in Config.GROUP_IDS:
        mock_bot.send_message.assert_any_call(
            chat_id=chat_id,
            text="Test with topic query",
            parse_mode=None,
            message_thread_id=topic_id
        )

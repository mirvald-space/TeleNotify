from unittest.mock import AsyncMock

import pytest
from aiogram import types

from app.bot.handlers import echo_message


@pytest.mark.asyncio
async def test_echo_message():
    # Create a mock Message object
    message = AsyncMock(spec=types.Message)
    message.text = "Hello, bot!"
    message.answer = AsyncMock()

    # Call the echo_message handler
    await echo_message(message)

    # Check that the bot tried to send a response
    message.answer.assert_called_once_with("I received your message!")

from unittest.mock import AsyncMock

import pytest
from aiogram import types

from app.bot.handlers import echo_message


@pytest.mark.asyncio
async def test_echo_message():
    message = AsyncMock(spec=types.Message)
    message.text = "Hello, bot!"
    message.answer = AsyncMock()

    await echo_message(message)

    message.answer.assert_called_once_with("I received your message!")

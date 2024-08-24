import logging
import re
from typing import List

from aiogram import Bot
from aiogram.enums import ParseMode

from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def escape_special_characters(text: str, format: str) -> str:
    if format == 'html':
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    elif format == 'markdown':
        special_chars = '_*[]()~`>#+-=|{}.!'
        return ''.join('\\' + char if char in special_chars else char for char in text)
    else:
        return text


async def send_notification_to_groups(bot: Bot, message: str, parse_mode: ParseMode, chat_ids: List[int]) -> bool:
    logger.info(f"Sending notification: message='{
                message}', parse_mode={parse_mode}, chat_ids={chat_ids}")
    all_success = True

    # Определяем формат на основе parse_mode
    format = 'html' if parse_mode == ParseMode.HTML else 'markdown' if parse_mode == ParseMode.MARKDOWN else 'plain'
    logger.info(f"Using format: {format}")

    # Экранируем специальные символы
    escaped_message = escape_special_characters(message, format)
    logger.info(f"Escaped message: '{escaped_message}'")

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=escaped_message, parse_mode=parse_mode)
            logger.info(f"Message successfully sent to the chat {chat_id}")
        except Exception as e:
            logger.error(f"Error sending a message to a chat {chat_id}: {e}")
            all_success = False
    return all_success

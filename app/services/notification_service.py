import logging
import re

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


async def send_notification_to_groups(bot: Bot, message: str, parse_mode: ParseMode) -> bool:
    logger.info(f"Attempting to send message: {message}")
    all_success = True

    for group_id in Config.GROUP_IDS:
        try:
            await bot.send_message(chat_id=group_id, text=message, parse_mode=parse_mode)
            logger.info(f"Successfully sent message to group {group_id}")
        except Exception as e:
            logger.error(f"Error sending message to group {group_id}: {e}")
            all_success = False
    return all_success

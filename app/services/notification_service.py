import logging
import re
from typing import List, Optional

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


async def send_notification_to_groups(
    bot: Bot,
    message: str,
    parse_mode: Optional[ParseMode],
    chat_ids: List[int],
    topic_id: Optional[int] = None,
    reply_to_message_id: Optional[int] = None
) -> bool:
    logger.info(f"Sending notification: message='{message}', parse_mode={parse_mode}, chat_ids={
                chat_ids}, topic_id={topic_id}, reply_to_message_id={reply_to_message_id}")
    all_success = True

    format = 'html' if parse_mode == ParseMode.HTML else 'markdown' if parse_mode == ParseMode.MARKDOWN else 'plain'
    escaped_message = escape_special_characters(message, format)

    for chat_id in chat_ids:
        try:
            sent_message = await bot.send_message(
                chat_id=chat_id,
                text=escaped_message,
                parse_mode=parse_mode,
                message_thread_id=topic_id,
                reply_to_message_id=reply_to_message_id
            )
            logger.info(f"Message successfully sent to chat {chat_id}, topic {
                        topic_id}, message_id: {sent_message.message_id}")
        except Exception as e:
            logger.error(f"Error sending message to chat {
                         chat_id}, topic {topic_id}: {e}")
            all_success = False
    return all_success

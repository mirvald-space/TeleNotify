import logging
import re
from typing import List, Optional, Union

from aiogram import Bot
from aiogram.enums import ParseMode
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.config import Config
from app.services.notification_service import send_notification_to_groups

logger = logging.getLogger(__name__)


router = APIRouter()


class NotificationMessage(BaseModel):
    text: Optional[str] = Field(None, description="Main message content")
    message: Optional[str] = Field(
        None, description="Alternative to 'text' for backwards compatibility")
    format: Optional[str] = Field(
        None, description="Message format: 'plain', 'html', or 'markdown'. If not provided, it will be auto-detected.")
    bot_id: Optional[str] = Field(
        None, description="Optional bot token to use for sending the message")
    chat_id: Optional[Union[int, List[int]]] = Field(
        None, description="Optional chat ID or list of chat IDs to send the message to")
    topic_id: Optional[int] = Field(
        None, description="Optional topic ID for sending to a specific group topic")


def detect_format(text: str) -> str:
    if re.search(r'<[^>]+>', text):
        return 'html'
    elif re.search(r'\*.*\*|_.*_|\[.*\]\(.*\)', text):
        return 'markdown'
    return 'plain'


async def get_bot():
    bot = Bot(token=Config.BOT_TOKEN)
    try:
        yield bot
    finally:
        await bot.session.close()


@router.post("/send_notification")
async def send_notification(
    notification: Optional[NotificationMessage] = None,
    text: Optional[str] = Query(None),
    bot_id: Optional[str] = Query(None),
    chat_id: Optional[Union[int, List[int]]] = Query(None),
    topic_id: Optional[int] = Query(None),
    bot: Bot = Depends(get_bot)
):
    message_text = text or (notification.text if notification else None) or (
        notification.message if notification else None)
    if not message_text:
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")

    used_bot_id = bot_id or (
        notification.bot_id if notification else None) or Config.BOT_TOKEN
    used_chat_id = chat_id or (
        notification.chat_id if notification else None) or Config.GROUP_IDS
    used_topic_id = topic_id or (
        notification.topic_id if notification else None)

    message_format = (
        notification.format if notification else None) or detect_format(message_text)

    if message_format == 'html':
        parse_mode = ParseMode.HTML
    elif message_format == 'markdown':
        parse_mode = ParseMode.MARKDOWN
    else:
        parse_mode = None

    if used_bot_id != Config.BOT_TOKEN:
        custom_bot = Bot(token=used_bot_id)
    else:
        custom_bot = bot

    try:
        if isinstance(used_chat_id, int):
            used_chat_id = [used_chat_id]
        elif used_chat_id is None:
            used_chat_id = Config.GROUP_IDS

        success = await send_notification_to_groups(custom_bot, message_text, parse_mode, used_chat_id, used_topic_id)

        if success:
            return {"status": "success", "message": "Notification sent to all specified groups/topics"}
        else:
            raise HTTPException(
                status_code=500, detail="Failed to send notification to some groups/topics")
    finally:
        if used_bot_id != Config.BOT_TOKEN:
            await custom_bot.session.close()

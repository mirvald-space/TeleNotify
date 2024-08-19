import re
from typing import Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.config import Config
from app.services.notification_service import send_notification_to_groups

router = APIRouter()


class NotificationMessage(BaseModel):
    text: Optional[str] = Field(None, description="Main message content")
    message: Optional[str] = Field(
        None, description="Alternative to 'text' for backwards compatibility")
    format: Optional[str] = Field(
        None, description="Message format: 'plain', 'html', or 'markdown'. If not provided, it will be auto-detected.")


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
    text: Optional[str] = None,
    bot: Bot = Depends(get_bot)
):
    message_text = text or (notification.text if notification else None) or (
        notification.message if notification else None)

    if not message_text:
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")

    message_format = notification.format if notification and notification.format else detect_format(
        message_text)

    if message_format == 'html':
        parse_mode = ParseMode.HTML
    elif message_format == 'markdown':
        parse_mode = ParseMode.MARKDOWN
    else:
        parse_mode = None

    success = await send_notification_to_groups(bot, message_text, parse_mode)

    if success:
        return {"status": "success", "message": "Notification sent to all groups"}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to send notification to some groups")

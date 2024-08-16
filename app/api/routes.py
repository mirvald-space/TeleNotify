from typing import Optional

from aiogram import Bot
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.config import Config
from app.services.notification_service import send_notification_to_groups

router = APIRouter()


class NotificationMessage(BaseModel):
    text: Optional[str] = Field(None, description="Main message content")
    message: Optional[str] = Field(
        None, description="Alternative to 'text' for backwards compatibility")
    channel: Optional[str] = Field(
        None, description="Slack channel (ignored for Telegram)")
    username: Optional[str] = Field(
        None, description="Slack username (ignored for Telegram)")
    icon_emoji: Optional[str] = Field(
        None, description="Slack icon emoji (ignored for Telegram)")
    link_names: Optional[bool] = Field(
        None, description="Slack link names option (ignored for Telegram)")
    mrkdwn: Optional[bool] = Field(
        None, description="Slack Markdown option (ignored for Telegram)")


async def get_bot():
    bot = Bot(token=Config.BOT_TOKEN)
    try:
        yield bot
    finally:
        await bot.session.close()


@router.post("/send_notification")
async def send_notification(
    notification: Optional[NotificationMessage] = None,
    text: Optional[str] = Query(
        None, description="Message text (can be provided as query parameter)"),
    bot: Bot = Depends(get_bot)
):
    message_text = text or (notification.text if notification else None) or (
        notification.message if notification else None)

    if not message_text:
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")

    success = await send_notification_to_groups(bot, message_text)

    if success:
        return {"status": "success", "message": "Notification sent to all groups"}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to send notification to some groups")

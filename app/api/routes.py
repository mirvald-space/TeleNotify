from aiogram import Bot
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.config import Config
from app.services.notification_service import send_notification_to_groups

router = APIRouter()


class NotificationMessage(BaseModel):
    message: str


async def get_bot():
    bot = Bot(token=Config.BOT_TOKEN)
    try:
        yield bot
    finally:
        await bot.session.close()


@router.post("/send_notification")
async def send_notification(notification: NotificationMessage, bot: Bot = Depends(get_bot)):
    if not notification.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    success = await send_notification_to_groups(bot, notification.message)

    if success:
        return {"status": "success", "message": "Notification sent to all groups"}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to send notification to some groups")

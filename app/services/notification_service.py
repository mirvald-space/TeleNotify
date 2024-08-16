import logging

from aiogram import Bot

from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_notification_to_groups(bot: Bot, message: str) -> bool:
    logger.info(f"Attempting to send message: {message}")
    all_success = True
    for group_id in Config.GROUP_IDS:
        try:
            await bot.send_message(chat_id=group_id, text=message)
            logger.info(f"Successfully sent message to group {group_id}")
        except Exception as e:
            logger.error(f"Error sending message to group {group_id}: {e}")
            all_success = False
    return all_success

import logging

from aiogram import Bot
from aiogram.types import Chat

from app.config import Config

logger = logging.getLogger(__name__)


async def log_available_chats(bot: Bot):
    available_chats = []
    try:
        for group_id in Config.GROUP_IDS:
            try:
                chat = await bot.get_chat(chat_id=group_id)
                if isinstance(chat, Chat):
                    available_chats.append({
                        'id': chat.id,
                        'type': chat.type,
                        'title': chat.title
                    })
            except Exception as e:
                logger.error(f"Error fetching chat info for ID {
                             group_id}: {e}")

        logger.info(f"Available chats for bot {bot.id}:")
        for chat in available_chats:
            logger.info(f"Chat ID: {chat['id']}, Type: {
                        chat['type']}, Title: {chat['title']}")
    except Exception as e:
        logger.error(f"Error while fetching available chats: {e}")

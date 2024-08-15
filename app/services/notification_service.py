from aiogram import Bot

from app.config import Config


async def send_notification_to_groups(bot: Bot, message: str) -> bool:
    all_success = True
    for group_id in Config.GROUP_IDS:
        try:
            await bot.send_message(chat_id=group_id, text=message)
        except Exception as e:
            print(f"Error sending message to group {group_id}: {e}")
            all_success = False
    return all_success

import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from fastapi import Depends, FastAPI

from app.api.routes import router as api_router
from app.bot.handlers import register_handlers
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_PATH = f"/bot/{Config.BOT_TOKEN}"
WEBHOOK_URL = Config.WEBHOOK_URL + WEBHOOK_PATH


async def get_bot():
    bot = Bot(token=Config.BOT_TOKEN)
    try:
        yield bot
    finally:
        await bot.session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    dp = Dispatcher()
    register_handlers(dp)

    async with Bot(token=Config.BOT_TOKEN) as bot:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook set to URL: {WEBHOOK_URL}")

    yield

    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: WebhookInfo, bot: Bot = Depends(get_bot)):
    dp = Dispatcher()
    register_handlers(dp)
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    return await webhook_handler.handle(request)

if __name__ == "__main__":
    logger.info("Starting bot...")
    uvicorn.run(app, host=Config.WEBAPP_HOST, port=Config.WEBAPP_PORT)

import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from fastapi import Depends, FastAPI, Request

# Импортируйте корневой роутер
from app.api.routes import router as api_router
from app.api.routes import router as root_router
from app.bot.handlers import register_handlers
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_PATH = f"/bot/{Config.BOT_TOKEN}"
WEBHOOK_URL = Config.WEBHOOK_URL + WEBHOOK_PATH

dp = Dispatcher()  # Create Dispatcher once
register_handlers(dp)  # Register handlers once
webhook_handler = SimpleRequestHandler(
    dispatcher=dp, bot=None)  # Initialize handler without bot


async def get_bot():
    bot = Bot(token=Config.BOT_TOKEN)
    try:
        yield bot
    finally:
        await bot.session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with Bot(token=Config.BOT_TOKEN) as bot:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook set to URL: {WEBHOOK_URL}")

    # Set the bot instance in webhook handler
    webhook_handler.bot = bot

    yield

    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(api_router)
app.include_router(root_router)  # Подключите корневой роутер


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request, bot: Bot = Depends(get_bot)):
    # Set bot instance in webhook handler
    webhook_handler.bot = bot
    return await webhook_handler.handle(request)

if __name__ == "__main__":
    logger.info("Starting bot...")
    uvicorn.run(app, host=Config.WEBAPP_HOST, port=Config.WEBAPP_PORT)

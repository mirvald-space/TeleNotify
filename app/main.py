import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import WebhookInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from fastapi import FastAPI

from app.api.routes import router as api_router
from app.bot.handlers import register_handlers
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

WEBHOOK_PATH = f"/bot/{Config.BOT_TOKEN}"
WEBHOOK_URL = Config.WEBHOOK_URL + WEBHOOK_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"Webhook set to URL: {WEBHOOK_URL}")

    yield

    logger.info("Shutting down bot...")
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

register_handlers(dp)

app.include_router(api_router)

webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: WebhookInfo):
    return await webhook_handler.handle(request)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting bot...")
    uvicorn.run(app, host=Config.WEBAPP_HOST, port=Config.WEBAPP_PORT)

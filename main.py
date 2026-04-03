import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import db
from handlers import router

# Load environment variables
load_dotenv()

async def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logging.error("TELEGRAM_BOT_TOKEN is not set in .env")
        sys.exit(1)

    # Initialize SQLite Database
    db.init_db()
    logging.info("Database initialized.")

    # Initialize Bot and Dispatcher
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    # Register handlers
    dp.include_router(router)

    # Start polling
    logging.info("Starting bot polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

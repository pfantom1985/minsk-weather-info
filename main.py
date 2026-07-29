import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)

async def main():
    async with Bot(token=TOKEN) as bot:
        print("Start bot...")
        await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")

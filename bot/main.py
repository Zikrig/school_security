import asyncio
import logging
from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
from bot.handlers import start, materials, admin

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(materials.router)
dp.include_router(start.router)
dp.include_router(admin.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
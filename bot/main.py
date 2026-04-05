import logging
import sys

from vkbottle.bot import Bot

from bot.config import VK_GROUP_TOKEN
from bot.handlers import admin, materials, start

logging.basicConfig(level=logging.INFO)


def main() -> None:
    if not VK_GROUP_TOKEN:
        logging.error("Задайте VK_GROUP_TOKEN в окружении или .env")
        sys.exit(1)

    bot = Bot(VK_GROUP_TOKEN)
    start.setup(bot)
    materials.setup(bot)
    admin.setup(bot)
    bot.run_forever()


if __name__ == "__main__":
    main()

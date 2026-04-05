from vkbottle.bot import Bot, Message

from bot.keyboards.main_menu import get_main_keyboard

_START_TEXTS = ("/start", "start", "Начать", "начать")


def setup(bot: Bot) -> None:
    @bot.on.message(text=list(_START_TEXTS))
    async def cmd_start(message: Message):
        await message.answer(
            "Добро пожаловать! Я бот информационной безопасности.\n\n"
            "Выберите нужный раздел:",
            keyboard=get_main_keyboard(),
        )

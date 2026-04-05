from vkbottle.bot import Bot, Message

from bot.keyboards.main_menu import get_main_keyboard
from bot.state_helpers import clear_peer_state

_START_TEXTS = ("/start", "start", "Начать", "начать")


def setup(bot: Bot) -> None:
    @bot.on.message(text=list(_START_TEXTS))
    async def cmd_start(message: Message):
        await clear_peer_state(bot.state_dispenser, message.peer_id)
        await message.answer(
            "Добро пожаловать! Я бот информационной безопасности.\n\n"
            "Выберите нужный раздел:",
            keyboard=get_main_keyboard(),
        )

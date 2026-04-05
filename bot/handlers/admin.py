from vkbottle.bot import Bot, Message

from bot.config import ADMIN_IDS
from bot.data.materials import KEYWORDS
from bot.keyboards.main_menu import get_admin_keyboard, get_main_keyboard
from bot.state_helpers import clear_peer_state


def setup(bot: Bot) -> None:
    @bot.on.message(text="/admin")
    async def cmd_admin(message: Message):
        if message.from_id not in ADMIN_IDS:
            await message.answer("У вас нет доступа к панели администратора.")
            return
        await message.answer("Панель администратора", keyboard=get_admin_keyboard())

    @bot.on.message(text="🔑 Список ключевых слов")
    async def show_keywords(message: Message):
        if message.from_id not in ADMIN_IDS:
            return
        lines = ["Список ключевых слов:\n"]
        for keyword, data in KEYWORDS.items():
            lines.append(f"• {keyword} → {data['category']}: {data['subtopic']}")
        await message.answer("\n".join(lines))

    @bot.on.message(text="📊 Статистика")
    async def show_stats(message: Message):
        if message.from_id not in ADMIN_IDS:
            return
        await message.answer("Статистика в этой версии бота не собирается.")

    @bot.on.message(text="⬅️ На главную")
    async def back_to_main(message: Message):
        if message.from_id not in ADMIN_IDS:
            return
        await clear_peer_state(bot.state_dispenser, message.peer_id)
        await message.answer("Главное меню:", keyboard=get_main_keyboard())

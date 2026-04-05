from vkbottle import BaseStateGroup, GroupEventType
from vkbottle.bot import Bot, Message, MessageEvent
from vkbottle.dispatch.rules.base import PayloadContainsRule

from bot.data.materials import KEYWORDS, MATERIALS
from bot.keyboards.category_menu import get_category_keyboard
from bot.keyboards.main_menu import get_back_keyboard, get_main_keyboard


class SearchState(BaseStateGroup):
    WAITING_KEYWORD = "waiting_keyword"


def _footer() -> str:
    return "\n\nЕдиный номер экстренных служб 112\nПолиция 02, 102"


def _intro_block(material: dict) -> str:
    return f"{material['title']}\n\n{material['content'].strip()}"


def _full_material_text(material: dict) -> str:
    return _intro_block(material) + _footer()


def setup(bot: Bot) -> None:
    @bot.on.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        PayloadContainsRule({"cmd": "sub"}),
    )
    async def handle_subtopic(event: MessageEvent):
        pl = event.payload or {}
        category = pl.get("c")
        subtopic = pl.get("s")
        if not isinstance(category, str) or not isinstance(subtopic, str):
            await event.send_empty_answer()
            return
        if category not in MATERIALS:
            await event.show_snackbar("Раздел не найден")
            return
        if subtopic not in MATERIALS[category]["subtopics"]:
            await event.show_snackbar("Подтема не найдена")
            return
        material = MATERIALS[category]["subtopics"][subtopic]
        text = _full_material_text(material)
        await event.edit_message(
            message=text,
            keyboard=get_category_keyboard(category),
        )
        await event.send_empty_answer()

    @bot.on.message(text="👶 Памятка для детей")
    async def children_materials(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        material = MATERIALS["children"]
        await message.answer(
            f"{_intro_block(material)}\n\nВыберите подтему:",
            keyboard=get_category_keyboard("children"),
        )

    @bot.on.message(text="👨‍💼 Памятка для взрослых")
    async def adults_materials(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        material = MATERIALS["adults"]
        await message.answer(
            f"{_intro_block(material)}\n\nВыберите подтему:",
            keyboard=get_category_keyboard("adults"),
        )

    @bot.on.message(text="👵 Памятка для пенсионеров")
    async def pensioners_materials(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        material = MATERIALS["pensioners"]
        await message.answer(
            f"{_intro_block(material)}\n\nВыберите подтему:",
            keyboard=get_category_keyboard("pensioners"),
        )

    @bot.on.message(text="🔍 Поиск по ключевым словам")
    async def search_info(message: Message):
        await bot.state_dispenser.set(message.peer_id, SearchState.WAITING_KEYWORD)
        await message.answer(
            "Введите ключевое слово для поиска информации (например: банк, мэш, пенсия):",
            keyboard=get_back_keyboard(),
        )

    @bot.on.message(text="⬅️ Назад к категориям")
    async def back_to_categories(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer("Главное меню:", keyboard=get_main_keyboard())

    @bot.on.message(text="🏠 На главную")
    async def back_to_main_menu(message: Message):
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer("Главное меню:", keyboard=get_main_keyboard())

    @bot.on.message(state=SearchState.WAITING_KEYWORD)
    async def handle_search(message: Message):
        raw = message.text or ""
        user_text = raw.lower()
        found = False
        for keyword, data in KEYWORDS.items():
            if keyword in user_text:
                category = data["category"]
                subtopic = data["subtopic"]
                material = MATERIALS[category]["subtopics"][subtopic]
                await message.answer(
                    f"Найдено по запросу «{raw}»:\n\n{_full_material_text(material)}",
                    keyboard=get_back_keyboard(),
                )
                found = True
                break
        if not found:
            await message.answer(
                "По вашему запросу ничего не найдено. Попробуйте другие ключевые слова.",
                keyboard=get_back_keyboard(),
            )
        await bot.state_dispenser.delete(message.peer_id)

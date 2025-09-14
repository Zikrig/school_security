from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.data.materials import MATERIALS, KEYWORDS
from bot.keyboards.main_menu import get_main_keyboard, get_back_keyboard
from bot.keyboards.category_menu import get_category_keyboard

router = Router()

class SearchState(StatesGroup):
    waiting_for_keyword = State()

    
@router.callback_query(F.data.startswith("sub_"))
async def handle_subtopic(callback: CallbackQuery):
    data_parts = callback.data.split("_")
    await callback.answer(f"DEBUG: data_parts={data_parts}")
    if len(data_parts) != 3:
        await callback.answer("Ошибка запроса (len!=3)")
        return
    
    category = data_parts[1]
    subtopic = data_parts[2]
    await callback.answer(f"DEBUG: category={category}, subtopic={subtopic}")
    
    if category not in MATERIALS:
        await callback.answer(f"DEBUG: category '{category}' not in MATERIALS")
        await callback.answer("Раздел не найден (category)")
        return
    if subtopic not in MATERIALS[category]["subtopics"]:
        await callback.answer(f"DEBUG: subtopic '{subtopic}' not in MATERIALS[{category}]['subtopics']")
        await callback.answer("Раздел не найден (subtopic)")
        return
    
    material = MATERIALS[category]["subtopics"][subtopic]
    
    await callback.message.edit_text(
        f"<b>{material['title']}</b>\n\n{material['content']}\n\n"
        f"Единый номер экстренных служб 112\nПолиция 02, 102",
        parse_mode="HTML",
        reply_markup=get_category_keyboard(category)
    )
    await callback.answer()
    
    
@router.message(F.text == "👶 Памятка для детей")
async def children_materials(message: Message):
    material = MATERIALS["children"]
    await message.answer(
        f"<b>{material['title']}</b>\n\n{material['content']}\n\nВыберите подтему:",
        parse_mode="HTML",
        reply_markup=get_category_keyboard("children")
    )

@router.message(F.text == "👨‍💼 Памятка для взрослых")
async def adults_materials(message: Message):
    material = MATERIALS["adults"]
    await message.answer(
        f"<b>{material['title']}</b>\n\n{material['content']}\n\nВыберите подтему:",
        parse_mode="HTML",
        reply_markup=get_category_keyboard("adults")
    )

@router.message(F.text == "👵 Памятка для пенсионеров")
async def pensioners_materials(message: Message):
    material = MATERIALS["pensioners"]
    await message.answer(
        f"<b>{material['title']}</b>\n\n{material['content']}\n\nВыберите подтему:",
        parse_mode="HTML",
        reply_markup=get_category_keyboard("pensioners")
    )

@router.message(F.text == "🔍 Поиск по ключевым словам")
async def search_info(message: Message, state: FSMContext):
    await message.answer(
        "Введите ключевое слово для поиска информации (например: банк, мэш, пенсия):",
        reply_markup=get_back_keyboard()
    )
    await state.set_state(SearchState.waiting_for_keyword)

@router.message(SearchState.waiting_for_keyword)
async def handle_search(message: Message, state: FSMContext):
    user_text = message.text.lower()
    
    # Поиск по ключевым словам
    found = False
    for keyword, data in KEYWORDS.items():
        if keyword in user_text:
            category = data["category"]
            subtopic = data["subtopic"]
            material = MATERIALS[category]["subtopics"][subtopic]
            
            await message.answer(
                f"<b>Найдено по запросу '{user_text}':</b>\n\n"
                f"<b>{material['title']}</b>\n\n{material['content']}\n\n"
                f"Единый номер экстренных служб 112\nПолиция 02, 102",
                parse_mode="HTML",
                reply_markup=get_back_keyboard()
            )
            found = True
            break
    
    if not found:
        await message.answer(
            "По вашему запросу ничего не найдено. Попробуйте другие ключевые слова.",
            reply_markup=get_back_keyboard()
        )
    
    await state.clear()
    


    
@router.message(F.text == "⬅️ Назад к категориям")
async def back_to_categories(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🏠 На главную")
async def back_to_main_menu(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )


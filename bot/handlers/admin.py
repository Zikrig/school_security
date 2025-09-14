from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import ADMIN_IDS
from bot.data.materials import KEYWORDS
from bot.keyboards.main_menu import get_admin_keyboard, get_main_keyboard

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет доступа к панели администратора.")
        return
    
    await message.answer(
        "Панель администратора",
        reply_markup=get_admin_keyboard()
    )

@router.message(F.text == "🔑 Список ключевых слов")
async def show_keywords(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    keywords_text = "Список ключевых слов:\n\n"
    for keyword, data in KEYWORDS.items():
        keywords_text += f"• {keyword} → {data['category']}: {data['subtopic']}\n"
    
    await message.answer(keywords_text)

@router.message(F.text == "⬅️ На главную")
async def back_to_main(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )
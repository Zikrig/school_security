from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards.main_menu import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! Я бот информационной безопасности.\n\n"
        "Выберите нужный раздел:",
        reply_markup=get_main_keyboard()
    )
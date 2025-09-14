from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.data.materials import MATERIALS

def get_category_keyboard(category):
    keyboard = []
    for key, value in MATERIALS[category]["subtopics"].items():
        keyboard.append([InlineKeyboardButton(
            text=value["title"], 
            callback_data=f"sub_{category}_{key}"
        )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
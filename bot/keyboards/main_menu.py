from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👶 Памятка для детей")],
            [KeyboardButton(text="👨‍💼 Памятка для взрослых")],
            [KeyboardButton(text="👵 Памятка для пенсионеров")],
            [KeyboardButton(text="🔍 Поиск по ключевым словам")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_back_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Назад к категориям")],
            [KeyboardButton(text="🏠 На главную")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🔑 Список ключевых слов")],
            [KeyboardButton(text="⬅️ На главную")]
        ],
        resize_keyboard=True
    )
    return keyboard
from vkbottle import Callback, Keyboard

from bot.data.materials import MATERIALS

# VK: у inline-клавиатуры ограничение на число рядов (≈6); много рядов по 1 кнопке даёт 911.
# Подпись callback-кнопки — не длиннее 40 символов.
_MAX_LABEL = 40
_BUTTONS_PER_ROW = 2


def _callback_label(title: str) -> str:
    t = title.strip()
    if len(t) <= _MAX_LABEL:
        return t
    return t[: _MAX_LABEL - 1] + "…"


def get_category_keyboard(category: str) -> str:
    items = list(MATERIALS[category]["subtopics"].items())
    kb = Keyboard(one_time=False, inline=True)
    for i in range(0, len(items), _BUTTONS_PER_ROW):
        key1, val1 = items[i]
        kb.add(
            Callback(
                _callback_label(val1["title"]),
                payload={"cmd": "sub", "c": category, "s": key1},
            )
        )
        if i + 1 < len(items):
            key2, val2 = items[i + 1]
            kb.add(
                Callback(
                    _callback_label(val2["title"]),
                    payload={"cmd": "sub", "c": category, "s": key2},
                )
            )
        if i + _BUTTONS_PER_ROW < len(items):
            kb.row()
    return kb.get_json()

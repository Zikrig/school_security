from vkbottle import Callback, Keyboard

from bot.data.materials import MATERIALS


def get_category_keyboard(category: str) -> str:
    kb = Keyboard(one_time=False, inline=True)
    first = True
    for key, value in MATERIALS[category]["subtopics"].items():
        if not first:
            kb.row()
        first = False
        kb.add(
            Callback(
                value["title"],
                payload={"cmd": "sub", "c": category, "s": key},
            )
        )
    return kb.get_json()

from vkbottle import Keyboard, Text


def get_main_keyboard() -> str:
    return (
        Keyboard(one_time=False)
        .add(Text("👶 Памятка для детей"))
        .row()
        .add(Text("👨‍💼 Памятка для взрослых"))
        .row()
        .add(Text("👵 Памятка для пенсионеров"))
        .row()
        .add(Text("🔍 Поиск по ключевым словам"))
        .get_json()
    )


def get_back_keyboard() -> str:
    return (
        Keyboard(one_time=False)
        .add(Text("⬅️ Назад к категориям"))
        .row()
        .add(Text("🏠 На главную"))
        .get_json()
    )


def get_admin_keyboard() -> str:
    return (
        Keyboard(one_time=False)
        .add(Text("📊 Статистика"))
        .row()
        .add(Text("🔑 Список ключевых слов"))
        .row()
        .add(Text("⬅️ На главную"))
        .get_json()
    )

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from bot.data.materials import MATERIALS

_STATS_PATH = Path(__file__).resolve().parent / "data" / "stats.json"
_lock = asyncio.Lock()


def _default_stats() -> dict[str, Any]:
    return {
        "starts": 0,
        "unique_user_ids": [],
        "category_opens": {"children": 0, "adults": 0, "pensioners": 0},
        "subtopic_opens": {},
        "search_sessions": 0,
        "search_queries": 0,
        "search_hits": 0,
        "search_misses": 0,
        "admin_panel_opens": 0,
    }


def _normalize(raw: dict[str, Any]) -> dict[str, Any]:
    d = _default_stats()
    if not isinstance(raw, dict):
        return d
    d["starts"] = int(raw.get("starts", d["starts"]))
    d["search_sessions"] = int(raw.get("search_sessions", d["search_sessions"]))
    d["search_queries"] = int(raw.get("search_queries", d["search_queries"]))
    d["search_hits"] = int(raw.get("search_hits", d["search_hits"]))
    d["search_misses"] = int(raw.get("search_misses", d["search_misses"]))
    d["admin_panel_opens"] = int(raw.get("admin_panel_opens", d["admin_panel_opens"]))
    co = raw.get("category_opens", {})
    if isinstance(co, dict):
        for k in d["category_opens"]:
            if k in co:
                d["category_opens"][k] = int(co[k])
    so = raw.get("subtopic_opens", {})
    if isinstance(so, dict):
        d["subtopic_opens"] = {str(k): int(v) for k, v in so.items()}
    uid = raw.get("unique_user_ids", [])
    if isinstance(uid, list):
        out: list[int] = []
        for x in uid:
            try:
                out.append(int(x))
            except (TypeError, ValueError):
                pass
        d["unique_user_ids"] = sorted(set(out))
    return d


def _read() -> dict[str, Any]:
    if not _STATS_PATH.exists():
        return _default_stats()
    try:
        with open(_STATS_PATH, encoding="utf-8") as f:
            raw = json.load(f)
        return _normalize(raw) if isinstance(raw, dict) else _default_stats()
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return _default_stats()


def _write(data: dict[str, Any]) -> None:
    _STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = _STATS_PATH.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(_STATS_PATH)


def _touch_user(data: dict[str, Any], user_id: int) -> None:
    u = set(data["unique_user_ids"])
    if user_id not in u:
        u.add(user_id)
        data["unique_user_ids"] = sorted(u)


def _subtopic_key(category: str, subtopic: str) -> str:
    return f"{category}:{subtopic}"


async def record_start(user_id: int) -> None:
    async with _lock:
        data = _read()
        data["starts"] += 1
        _touch_user(data, user_id)
        _write(data)


async def record_category_open(user_id: int, category: str) -> None:
    if category not in ("children", "adults", "pensioners"):
        return
    async with _lock:
        data = _read()
        _touch_user(data, user_id)
        data["category_opens"][category] += 1
        _write(data)


async def record_subtopic_open(user_id: int, category: str, subtopic: str) -> None:
    async with _lock:
        data = _read()
        _touch_user(data, user_id)
        key = _subtopic_key(category, subtopic)
        data["subtopic_opens"][key] = data["subtopic_opens"].get(key, 0) + 1
        _write(data)


async def record_search_session(user_id: int) -> None:
    async with _lock:
        data = _read()
        _touch_user(data, user_id)
        data["search_sessions"] += 1
        _write(data)


async def record_search_query(user_id: int, hit: bool) -> None:
    async with _lock:
        data = _read()
        _touch_user(data, user_id)
        data["search_queries"] += 1
        if hit:
            data["search_hits"] += 1
        else:
            data["search_misses"] += 1
        _write(data)


async def record_admin_panel(user_id: int) -> None:
    async with _lock:
        data = _read()
        _touch_user(data, user_id)
        data["admin_panel_opens"] += 1
        _write(data)


def _subtopic_title(key: str) -> str:
    if ":" not in key:
        return key
    category, sub = key.split(":", 1)
    try:
        return MATERIALS[category]["subtopics"][sub]["title"]
    except KeyError:
        return key


def format_stats_report(data: dict[str, Any]) -> str:
    cats = data["category_opens"]
    top = sorted(data["subtopic_opens"].items(), key=lambda x: -x[1])[:15]
    top_lines = (
        "\n".join(f"  • {_subtopic_title(k)} — {v}" for k, v in top) if top else "  (пока нет)"
    )

    return (
        "📊 Статистика бота\n\n"
        f"Уникальных пользователей: {len(data['unique_user_ids'])}\n"
        f"Запусков (/start и аналоги): {data['starts']}\n\n"
        "Открытия разделов:\n"
        f"  • Дети: {cats['children']}\n"
        f"  • Взрослые: {cats['adults']}\n"
        f"  • Пенсионеры: {cats['pensioners']}\n\n"
        f"Нажатий «Поиск»: {data['search_sessions']}\n"
        f"Поисковых запросов: {data['search_queries']}\n"
        f"  с результатом: {data['search_hits']}\n"
        f"  без результата: {data['search_misses']}\n\n"
        f"Входов в админ-панель: {data['admin_panel_opens']}\n\n"
        "Топ подтем (callback):\n"
        f"{top_lines}"
    )


async def load_stats() -> dict[str, Any]:
    async with _lock:
        return _read()


import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlencode
from urllib.request import urlopen

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
START = datetime(2026, 11, 20, 19, 0, tzinfo=ZoneInfo("Europe/Riga"))
MARKER = "OSU TEAM | BOHPTS"


def api(method, data):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if data:
        url += "?" + urlencode(data)

    with urlopen(url, timeout=30) as response:
        result = json.load(response)

    if not result["ok"]:
        raise RuntimeError(result)
    return result["result"]


now = datetime.now(ZoneInfo("Europe/Riga"))
remaining = max(0, int((START - now).total_seconds()))

days, rest = divmod(remaining, 86400)
hours, rest = divmod(rest, 3600)
minutes, seconds = divmod(rest, 60)

if remaining > 0:
    message = (
        f"⚔️ {MARKER} ⚔️\n\n"
        "🔥 ДО ОТКРЫТИЯ СЕРВЕРА\n\n"
        f"⏳ {days:02d} д. {hours:02d} ч. "
        f"{minutes:02d} мин. {seconds:02d} сек.\n\n"
        "📅 20 ноября 2026\n"
        "🕖 19:00 по Риге\n\n"
        "🌐 https://bohpts.com/ru/\n\n"
        "🔄 Обновление каждый час"
    )
else:
    message = (
        f"⚔️ {MARKER} ⚔️\n\n"
        "🔥 СЕРВЕР ОТКРЫТ!\n\n"
        "⚔️ OSU TEAM, В БОЙ!\n\n"
        "🌐 https://bohpts.com/ru/"
    )

chat = api("getChat", {"chat_id": CHAT_ID})
pinned = chat.get("pinned_message", {})

if (
    pinned.get("from", {}).get("is_bot")
    and MARKER in pinned.get("text", "")
):
    if pinned["text"] != message:
        api("editMessageText", {
            "chat_id": CHAT_ID,
            "message_id": pinned["message_id"],
            "text": message,
            "disable_web_page_preview": "true"
        })
else:
    sent = api("sendMessage", {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": "true"
    })

    api("pinChatMessage", {
        "chat_id": CHAT_ID,
        "message_id": sent["message_id"],
        "disable_notification": "true"
    })

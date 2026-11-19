
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlencode
from urllib.request import urlopen

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

ZONE = ZoneInfo("Europe/Riga")
START = datetime(2026, 11, 20, 19, 0, tzinfo=ZONE)

def telegram(method, params):
    url = (
        f"https://api.telegram.org/bot{TOKEN}/{method}?"
        + urlencode(params)
    )
    with urlopen(url, timeout=30) as response:
        return response.read()

now = datetime.now(ZONE)
remaining = max(0, int((START - now).total_seconds()))

days, remainder = divmod(remaining, 86400)
hours, remainder = divmod(remainder, 3600)
minutes, seconds = divmod(remainder, 60)

if remaining:
    message = (
        "⚔️ OSU TEAM | BOHPTS ⚔️\n\n"
        "🔥 ДО СТАРТА СЕРВЕРА:\n\n"
        f"⏳ {days:02d} д. {hours:02d} ч. "
        f"{minutes:02d} мин. {seconds:02d} сек.\n\n"
        "📅 20.11.2026 — 19:00 (Рига)\n"
        "🌐 https://bohpts.com/ru/"
    )
else:
    message = "🔥 СЕРВЕР ОТКРЫТ!\n⚔️ OSU TEAM, В БОЙ!"

telegram("sendMessage", {
    "chat_id": CHAT_ID,
    "text": message
})

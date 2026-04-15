import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv("MAX_TOKEN", "")
BASE_URL = os.getenv("BASE_URL", "https://platform-api.max.ru")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

CHILDREN_CHANNEL_URL = os.getenv("CHILDREN_CHANNEL_URL", "")
LINGERIE_CHANNEL_URL = os.getenv("LINGERIE_CHANNEL_URL", "")

ADDRESSES_TEXT = (
    "📍 Наши магазины\n\n"
    "🏬 г. Энгельс\n"
    "📌 ул. М. Горького, д. 37\n\n"
    "🏬 г. Энгельс\n"
    "📌 пр-т Ф. Энгельса, д. 11\n\n"
    "🏬 г. Энгельс\n"
    "📌 пр-т Ф. Энгельса, д. 37"
)

if not MAX_TOKEN:
    print("WARNING: MAX_TOKEN is empty")
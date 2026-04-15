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
    "📌 пр-т Ф. Энгельса, д. 37\n\n"
    "Нажмите кнопку ниже, чтобы открыть магазин на карте 👇"
)

STORE_1_MAP_URL = "https://yandex.ru/maps/?text=Энгельс%20ул.%20М.%20Горького%2037"
STORE_2_MAP_URL = "https://yandex.ru/maps/?text=Энгельс%20пр-т%20Ф.%20Энгельса%2011"
STORE_3_MAP_URL = "https://yandex.ru/maps/?text=Энгельс%20пр-т%20Ф.%20Энгельса%2037"
if not MAX_TOKEN:
    print("WARNING: MAX_TOKEN is empty")
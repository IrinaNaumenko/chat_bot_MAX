import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv("MAX_TOKEN", "")
BASE_URL = os.getenv("BASE_URL", "https://platform-api.max.ru")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

CHILDREN_CHANNEL_URL = os.getenv("CHILDREN_CHANNEL_URL", "")
LINGERIE_CHANNEL_URL = os.getenv("LINGERIE_CHANNEL_URL", "")

ADDRESSES_TEXT = os.getenv(
    "ADDRESSES_TEXT",
    "📍 Наши адреса\n\n— Адрес 1\n— Адрес 2"
)

if not MAX_TOKEN:
    print("WARNING: MAX_TOKEN is empty")
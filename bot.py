import json
import requests

from config import (
    MAX_TOKEN,
    BASE_URL,
    ADDRESSES_TEXT,
    CHILDREN_CHANNEL_URL,
    LINGERIE_CHANNEL_URL,
)

HEADERS = {
    "Authorization": MAX_TOKEN,
    "Content-Type": "application/json; charset=utf-8",
}


def build_main_buttons():
    return [
        [
            {
                "type": "link",
                "text": "👶 Детская одежда",
                "url": CHILDREN_CHANNEL_URL,
            }
        ],
        [
            {
                "type": "link",
                "text": "👙 Нижнее бельё",
                "url": LINGERIE_CHANNEL_URL,
            }
        ],
        [
            {
                "type": "message",
                "text": "🛍 Каталог",
                "payload": "каталог",
            }
        ],
        [
            {
                "type": "message",
                "text": "📍 Адрес",
                "payload": "адрес",
            }
        ],
    ]


def build_catalog_buttons():
    return [
        [{"type": "message", "text": "👗 Платья", "payload": "платье"}],
        [{"type": "message", "text": "👖 Джинсы", "payload": "джинсы"}],
        [{"type": "message", "text": "🧥 Верхняя одежда", "payload": "верхняя"}],
        [{"type": "message", "text": "👕 Футболки", "payload": "футболка"}],
        [{"type": "message", "text": "👚 Блузы", "payload": "блуза"}],
        [{"type": "message", "text": "👗 Юбки", "payload": "юбка"}],
        [{"type": "message", "text": "👜 Аксессуары", "payload": "аксессуары"}],
        [{"type": "message", "text": "✨ Новинки", "payload": "новинка"}],
        [{"type": "message", "text": "🔥 Распродажа", "payload": "распродажа"}],
        [{"type": "message", "text": "🔙 Назад", "payload": "назад"}],
    ]


def send_message(chat_id, text, buttons=None):
    payload = {
        "text": text
    }

    if buttons:
        payload["attachments"] = [
            {
                "type": "inline_keyboard",
                "payload": {
                    "buttons": buttons
                }
            }
        ]

    response = requests.post(
        f"{BASE_URL}/messages",
        params={"chat_id": chat_id},
        headers=HEADERS,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )

    print("SEND:", response.status_code, response.text)
    response.raise_for_status()


CATEGORY_MAP = {
    "платье": ("👗 Платья", "платье"),
    "джинсы": ("👖 Джинсы", "джинсы"),
    "верхняя": ("🧥 Верхняя одежда", "верхняя"),
    "футболка": ("👕 Футболки", "футболка"),
    "блуза": ("👚 Блузы", "блуза"),
    "юбка": ("👗 Юбки", "юбка"),
    "аксессуары": ("👜 Аксессуары", "аксессуары"),
    "новинка": ("✨ Новинки", "новинка"),
    "распродажа": ("🔥 Распродажа", "распродажа"),
}


def handle_start(chat_id):
    send_message(
        chat_id,
        "Добро пожаловать 🤍\n\nПосмотри, что есть:",
        buttons=build_main_buttons(),
    )


def handle_catalog(chat_id):
    send_message(
        chat_id,
        "🛍 Каталог\n\nВыбери категорию:",
        buttons=build_catalog_buttons(),
    )
from config import (
    MAX_TOKEN,
    BASE_URL,
    ADDRESSES_TEXT,
    CHILDREN_CHANNEL_URL,
    LINGERIE_CHANNEL_URL,
    STORE_1_MAP_URL,
    STORE_2_MAP_URL,
    STORE_3_MAP_URL,
)
def build_address_buttons():
    return [
        [
            {
                "type": "link",
                "text": "🗺 М. Горького, 37",
                "url": STORE_1_MAP_URL,
            }
        ],
        [
            {
                "type": "link",
                "text": "🗺 Ф. Энгельса, 11",
                "url": STORE_2_MAP_URL,
            }
        ],
        [
            {
                "type": "link",
                "text": "🗺 Ф. Энгельса, 37",
                "url": STORE_3_MAP_URL,
            }
        ],
        [
            {
                "type": "message",
                "text": "🔙 Назад",
                "payload": "назад",
            }
        ],
    ]

def send_catalog_tag(chat_id, title, tag):
    text = (
        f"{title}\n\n"
        f"Мы уже всё подобрали за тебя 🤍\n"
        f"Открой канал и ищи по тегу: #{tag}"
    )
    send_message(chat_id, text, buttons=build_catalog_buttons())


def handle_text(chat_id, text):
    text = (text or "").strip().lower()
    print("TEXT:", text)

    if text in ["/start", "start", "меню", "назад"]:
        handle_start(chat_id)
        return

    if "каталог" in text:
        handle_catalog(chat_id)
        return

    if "адрес" in text:
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_address_buttons())
        return

    for key, (title, tag) in CATEGORY_MAP.items():
        if key in text:
            send_catalog_tag(chat_id, title, tag)
            return

    handle_start(chat_id)


def handle_callback(chat_id, payload):
    payload = (payload or "").strip().lower()

    if payload == "каталог":
        handle_catalog(chat_id)
        return

    if payload == "адрес":
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_address_buttons())
        return

    if payload == "назад":
        handle_start(chat_id)
        return

    if payload in CATEGORY_MAP:
        title, tag = CATEGORY_MAP[payload]
        send_catalog_tag(chat_id, title, tag)
        return

    handle_start(chat_id)


def process_update(update):
    update_type = update.get("update_type")
    print("UPDATE:", update_type, update)

    if update_type == "bot_started":
        chat_id = update.get("chat_id")
        if chat_id:
            handle_start(chat_id)
        return

    if update_type == "message_callback":
        callback = update.get("callback", {})
        payload = callback.get("payload", "")
        chat_id = update.get("chat_id")

        if not chat_id:
            chat_id = update.get("message", {}).get("recipient", {}).get("chat_id")

        if chat_id:
            handle_callback(chat_id, payload)
        return

    if update_type == "message_created":
        message = update.get("message", {})
        chat_id = message.get("recipient", {}).get("chat_id")
        text = message.get("body", {}).get("text", "")

        if chat_id:
            handle_text(chat_id, text)
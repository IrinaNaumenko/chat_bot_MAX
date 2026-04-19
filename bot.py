import json
import requests

from config import (
    MAX_TOKEN,
    BASE_URL,
    ADDRESSES_TEXT,
    CHILDREN_CHANNEL_URL,
    LINGERIE_CHANNEL_URL,
    MANAGER_URL,
    OWNER_URL,
    CATALOG,
    STORE_1_MAP_URL,
    STORE_2_MAP_URL,
     STORE_3_MAP_URL,
)
from fashion_fortune import get_daily_fortune

session = requests.Session()
session.headers.update({
    "Authorization": MAX_TOKEN,
    "Content-Type": "application/json; charset=utf-8",
})


def build_main_buttons():
    buttons = [
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
                "text": "🔮 Модная гадалка",
                "payload": "гадалка",
            }
        ],
        [
            {
                "type": "message",
                "text": "📍 Адрес",
                "payload": "адрес",
            }
        ],
        [
            {
                "type": "message",
                "text": "📝 Жалобы и предложения",
                "payload": "feedback",
            }
        ],
    ]

    if MANAGER_URL:
        buttons.insert(
            3,
            [
                {
                    "type": "link",
                    "text": "💬 Уточнить наличие",
                    "url": MANAGER_URL,
                }
            ],
        )

    return buttons


def build_catalog_buttons():
    buttons = []

    for payload, item in CATALOG.items():
        buttons.append([
            {
                "type": "message",
                "text": item["title"],
                "payload": payload,
            }
        ])

    buttons.append([
        {
            "type": "message",
            "text": "🔙 Назад",
            "payload": "назад",
        }
    ])

    return buttons


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


def build_category_buttons(channel_url):
    buttons = [
        [
            {
                "type": "link",
                "text": "🛍 Открыть канал",
                "url": channel_url,
            }
        ],
        [
            {
                "type": "message",
                "text": "🔙 Назад",
                "payload": "каталог",
            }
        ],
    ]

    if MANAGER_URL:
        buttons.insert(
            1,
            [
                {
                    "type": "link",
                    "text": "💬 Уточнить наличие",
                    "url": MANAGER_URL,
                }
            ],
        )

    return buttons


def build_fortune_buttons():
    return [
        [
            {
                "type": "message",
                "text": "🔙 Назад",
                "payload": "назад",
            }
        ]
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

    response = session.post(
        f"{BASE_URL}/messages",
        params={"chat_id": chat_id},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )

    print("SEND:", response.status_code, response.text)
    response.raise_for_status()


def handle_start(chat_id):
    text = (
        "Добро пожаловать 🤍\n\n"
        "Посмотри, что есть:"
    )
    send_message(chat_id, text, buttons=build_main_buttons())


def handle_catalog(chat_id):
    text = (
        "🛍 Каталог\n\n"
        "Выберите, что вам интересно 👇"
    )
    send_message(chat_id, text, buttons=build_catalog_buttons())


def send_catalog_item(chat_id, item):
    title = item["title"]
    tag = item["tag"]
    channel_url = item["channel_url"]

    text = (
        f"{title}\n\n"
        f"Все актуальные модели уже в канале 🤍\n\n"
        f"Открой канал и посмотри публикации с хэштегом #{tag}\n\n"
        f"Если хочешь — поможем подобрать размер 👇"
    )

    send_message(chat_id, text, buttons=build_category_buttons(channel_url))


def handle_fashion_fortune(chat_id, user_id):
    if not user_id:
        send_message(
            chat_id,
            "🔮 Не удалось определить пользователя для прогноза.",
            buttons=build_main_buttons(),
        )
        return

    prediction = get_daily_fortune(user_id)

    text = (
        "🔮 Модная гадалка\n\n"
        f"{prediction}\n\n"
        "Завтра вас будет ждать новый прогноз 🤍"
    )

    send_message(chat_id, text, buttons=build_fortune_buttons())


def handle_text(chat_id, user_id, text):
    text = (text or "").strip().lower()
    print("TEXT:", text)

    if text in ["/start", "start", "меню", "назад"]:
        handle_start(chat_id)
        return

    if "каталог" in text:
        handle_catalog(chat_id)
        return

    if "гадалка" in text or "прогноз" in text:
        handle_fashion_fortune(chat_id, user_id)
        return

    if "адрес" in text:
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_address_buttons())
        return

    for key, item in CATALOG.items():
        if key in text:
            send_catalog_item(chat_id, item)
            return

    handle_start(chat_id)

def handle_callback(chat_id, user_id, payload):
    payload = (payload or "").strip().lower()

    if payload == "каталог":
        handle_catalog(chat_id)
        return

    if payload == "гадалка":
        handle_fashion_fortune(chat_id, user_id)
        return

    if payload == "адрес":
        send_message(chat_id, ADDRESSES_TEXT, buttons=build_address_buttons())
        return

    if payload == "назад":
        handle_start(chat_id)
        return

    if payload == "feedback":
        text = (
            "📝 Жалобы и предложения\n\n"
            "Если у вас есть пожелания, замечания или идеи по улучшению, "
            "напишите нам в личные сообщения 🤍\n\n"
            "Нам важно ваше мнение"
        )

        buttons = [
            [
                {
                    "type": "link",
                    "text": "💬 Написать нам",
                    "url": OWNER_URL,
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

        send_message(chat_id, text, buttons=buttons)
        return

    if payload in CATALOG:
        send_catalog_item(chat_id, CATALOG[payload])
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

        user_id = (
            update.get("message", {})
            .get("sender", {})
            .get("user_id")
        )

        if chat_id:
            handle_callback(chat_id, user_id, payload)
        return

    if update_type == "message_created":
        message = update.get("message", {})
        chat_id = message.get("recipient", {}).get("chat_id")
        text = message.get("body", {}).get("text", "")
        user_id = message.get("sender", {}).get("user_id")

        if chat_id:
            handle_text(chat_id, user_id, text)
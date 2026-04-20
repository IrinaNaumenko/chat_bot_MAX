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
    CATALOG_CHAT_ID,
    CATALOG_PAGE_SIZE,
    CATALOG_CHANNEL_FETCH_COUNT,
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
                "type": "callback",
                "text": "🛍 Каталог",
                "payload": "каталог",
            }
        ],
        [
            {
                "type": "callback",
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
                "type": "link",
                "text": "📝 Жалобы и предложения",
                "url": OWNER_URL,
            }
        ]
    ]

    return buttons


def build_catalog_buttons():
    buttons = []

    for payload, item in CATALOG.items():
        buttons.append([
            {
                "type": "callback",
                "text": item["title"],
                "payload": payload,
            }
        ])

    buttons.append([
        {
            "type": "callback",
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
                    "type": "callback",
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
                "type": "callback",
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
                "type": "callback",
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

def get_channel_messages(chat_id, count=20):
    try:
        response = session.get(
            f"{BASE_URL}/messages",
            params={"chat_id": chat_id, "count": count},
            timeout=10,
        )

        print("GET MESSAGES:", response.status_code)

        if response.status_code != 200:
            print("ERROR RESPONSE:", response.text)
            return []

        data = response.json()
        return data.get("messages", [])

    except Exception as e:
        print("GET CHANNEL ERROR:", str(e))
        return []

def find_posts_by_tag(tag):
    messages = get_channel_messages(
        CATALOG_CHAT_ID,
        count=CATALOG_CHANNEL_FETCH_COUNT,
    )

    if not messages:
        messages = get_channel_messages(CATALOG_CHAT_ID, count=20)

    hashtag = f"#{tag}".lower()
    results = []

    for msg in messages:
        body = msg.get("body", {})
        text = (body.get("text") or "").strip()

        if hashtag in text.lower():
            results.append(msg)

    return results

def handle_start(chat_id):
    text = (
        "Здравствуйте! 🤍\n\n"
        "Добро пожаловать в магазин.\n"
        "Выберите, что вас интересует 👇"
    )
    send_message(chat_id, text, buttons=build_main_buttons())

def send_channel_post(chat_id, msg):
    body = msg.get("body", {})
    text = body.get("text", "") or ""
    attachments = body.get("attachments", []) or []
    post_url = msg.get("url", "")

    new_attachments = []

    for att in attachments:
        if att.get("type") == "image":
            new_attachments.append(att)

    buttons = []

    if post_url:
        buttons.append([
            {
                "type": "link",
                "text": "🔗 Открыть пост",
                "url": post_url,
            }
        ])

    if MANAGER_URL:
        buttons.append([
            {
                "type": "link",
                "text": "💬 Уточнить наличие",
                "url": MANAGER_URL,
            }
        ])

    if buttons:
        new_attachments.append(
            {
                "type": "inline_keyboard",
                "payload": {"buttons": buttons}
            }
        )

    payload = {
        "text": text if text else "✨ Товар из категории",
        "attachments": new_attachments
    }

    response = session.post(
        f"{BASE_URL}/messages",
        params={"chat_id": chat_id},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )

    print("SEND POST:", response.status_code, response.text)

    response.raise_for_status()
def build_back_to_catalog_button():
    return [
        [
            {
                "type": "message",
                "text": "🔙 Назад",
                "payload": "каталог",
            }
        ]
    ]
def build_show_more_buttons(category_key, offset):
    buttons = [
        [
            {
                "type": "message",
                "text": "➕ Показать ещё",
                "payload": f"more:{category_key}:{offset}",
            }
        ]
    ]
    return buttons

def send_products_by_category(chat_id, category_key, offset=0):
    item = CATALOG[category_key]
    tag = item["tag"]
    title = item["title"]

    posts = find_posts_by_tag(tag)

    if not posts:
        send_message(
            chat_id,
            f"{title}\n\nПока ничего не найдено по хэштегу #{tag} 🤍",
            buttons=build_catalog_buttons(),
        )
        return

    page_posts = posts[offset:offset + CATALOG_PAGE_SIZE]

    if not page_posts:
        send_message(
            chat_id,
            f"{title}\n\nБольше товаров по хэштегу #{tag} пока нет 🤍",
            buttons=build_catalog_buttons(),
        )
        return

    send_message(
        chat_id,
        f"{title}\n\n"
        f"Найдено товаров: {len(posts)}\n"
        f"Показываю {offset + 1}–{offset + len(page_posts)} 👇"
    )

    for post in page_posts:
        send_channel_post(chat_id, post)

    next_offset = offset + CATALOG_PAGE_SIZE
    if next_offset < len(posts):
        send_message(
            chat_id,
            "Хочешь посмотреть ещё товары?",
            buttons=build_show_more_buttons(category_key, next_offset),
        )
    else:
        send_message(
            chat_id,
            "Это все товары в этой категории 🤍",
            buttons=build_back_to_catalog_button(),
        )

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

    for key in CATALOG:
        if key in text:
            send_products_by_category(chat_id, key)
            return

    handle_start(chat_id)

def handle_callback(chat_id, user_id, payload):
    payload = (payload or "").strip().lower()
    print("CALLBACK PAYLOAD:", repr(payload))

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

    if payload.startswith("more:"):
        parts = payload.split(":")
        if len(parts) == 3:
            category_key = parts[1]
            try:
                offset = int(parts[2])
            except ValueError:
                offset = 0

            if category_key in CATALOG:
                send_products_by_category(chat_id, category_key, offset)
                return

    if payload in CATALOG:
        send_products_by_category(chat_id, payload)
        return

    print("UNKNOWN CALLBACK:", repr(payload))
    return

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

        if message.get("recipient", {}).get("chat_type") == "channel":
            return

        chat_id = message.get("recipient", {}).get("chat_id")
        text = message.get("body", {}).get("text", "")
        user_id = message.get("sender", {}).get("user_id")

        if chat_id:
            handle_text(chat_id, user_id, text)
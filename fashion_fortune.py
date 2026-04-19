import json
import os
import random
from datetime import datetime

from config import FASHION_PREDICTIONS

FORTUNE_FILE = "fashion_fortune_data.json"


def load_fortunes():
    if not os.path.exists(FORTUNE_FILE):
        return {}

    try:
        with open(FORTUNE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_fortunes(data):
    with open(FORTUNE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_daily_fortune(user_id):
    user_id = str(user_id)
    today = get_today_date()
    data = load_fortunes()

    if user_id in data:
        saved = data[user_id]
        if saved.get("date") == today:
            return saved.get("prediction")

    prediction = random.choice(FASHION_PREDICTIONS)

    data[user_id] = {
        "date": today,
        "prediction": prediction
    }

    save_fortunes(data)
    return prediction
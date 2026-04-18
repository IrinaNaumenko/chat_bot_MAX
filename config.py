from flask import Flask, request, jsonify
from bot import process_update
from config import WEBHOOK_SECRET
import threading

app = Flask(__name__)


@app.get("/health")
def health():
    return "ok", 200


@app.post("/webhook")
def webhook():
    incoming_secret = request.headers.get("X-Max-Bot-Api-Secret", "")
    if WEBHOOK_SECRET and incoming_secret != WEBHOOK_SECRET:
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400

    threading.Thread(target=process_update, args=(data,), daemon=True).start()
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
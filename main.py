from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
CHATID = os.getenv("CHATID")

# --- Signal Route ---
@app.post("/signal")
def signal():
    try:
        data = request.json

        signal_text = data.get("signal", "No signal")
        ticker = data.get("ticker", "Unknown")
        price = data.get("price", "0")
        tf = data.get("tf", "N/A")
        time = data.get("time", "N/A")

        message = f"""
📡 *TRADING SIGNAL*
-------------------------
📊 *Signal:* {signal_text}
💰 *Price:* {price}
🕒 *TF:* {tf}
🪙 *Ticker:* {ticker}
⏰ *Time:* {time}
"""

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHATID,
            "text": message,
            "parse_mode": "Markdown"
        }

        r = requests.post(url, json=payload)

        return jsonify({"status": "ok", "telegram": r.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/")
def home():
    return "SMC SIGNAL BOT RUNNING"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


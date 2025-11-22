
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN  = os.getenv("TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHATID = os.getenv("CHATID", "YOUR_CHAT_ID")
URL    = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json(force=True)
    raw = data.get("signal", "")
    parts = raw.split("|")
    try:
        direction = parts[0]
        entry = parts[1].split("=")[1]
        tp = parts[2].split("=")[1]
        sl = parts[3].split("=")[1]
    except:
        return jsonify({"error":"parse failed"})

    ticker = data.get("ticker","-")
    tf = data.get("tf","-")
    time = data.get("time","-")

    head = "🟢 LONG" if direction=="LONG" else "🔴 SHORT"
    msg = f"{head}\nTicker: {ticker}\nTF: {tf}\nTime: {time}\nEntry: {entry}\nTP: {tp}\nSL: {sl}"

    requests.post(URL, json={"chat_id": CHATID, "text": msg})
    return jsonify({"ok":True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

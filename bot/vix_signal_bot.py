
import requests, time
from utils.mt5_connector import get_latest_ohlcv, send_mt5_alert  # optional

# Telegram credentials
TELEGRAM_TOKEN = "8115912703:AAFDGCYa8UwZUj3-aejIFz8jflxtmzojKIs"
CHAT_ID = "5724243168"

# Your API endpoint (local or Render)
API_URL = "http://localhost:5000/signal"  # Replace with your deployed URL

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

while True:
    try:
        ohlcv = get_latest_ohlcv("Volatility 75 Index")
        res = requests.post(API_URL, json={"ohlcv": ohlcv.to_dict(orient="records")})
        signal = res.json().get("signal")

        if signal in ["buy", "sell"]:
            msg = f"📢 *VIX75 SIGNAL*: {signal.upper()} ✅\nTimeframe: 1m\nRisk: 1:3\nAutoTrade: Enabled"
            send_telegram(msg)
            send_mt5_alert(signal)  # executes trade on MT5
        else:
            print("No trade signal.")

    except Exception as err:
        print(f"Error polling signal: {err}")

    time.sleep(60)

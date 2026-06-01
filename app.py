from flask import Flask, jsonify
from flask_cors import CORS
import datetime
import pytz

app = Flask(__name__)
CORS(app)

# IST Time Zone
ist = pytz.timezone('Asia/Kolkata')

@app.route('/get-signal/<asset>/<timeframe>')
def get_signal(asset, timeframe):
    # 1. Weekend Check
    now = datetime.datetime.now(ist)
    if now.weekday() >= 5:
        return jsonify({"signal": "MARKET CLOSED", "status": "white", "emoji": "⚪"})

    # 2. Yahan logic aayega (Candle Psychology, Price Action, RSI, EMA, etc.)
    # Ye part hum agle step mein detail mein karenge
    return jsonify({
        "signal": "UP",
        "status": "green",
        "emoji": "🟢",
        "trend": "Bullish",
        "probability": "85%"
    })

if __name__ == '__main__':
    app.run()

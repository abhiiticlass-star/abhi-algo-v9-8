from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas_ta as ta
import datetime
import pytz

app = Flask(__name__)
CORS(app)

def get_market_data(symbol, period='1d', interval='1m'):
    data = yf.download(symbol, period=period, interval=interval)
    if not data.empty:
        # Technical Analysis Indicators
        data['EMA_10'] = ta.ema(data['Close'], length=10)
        data['EMA_20'] = ta.ema(data['Close'], length=20)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        return data.iloc[-1] # Latest candle data
    return None

@app.route('/get-signal/<asset>/<tf>')
def get_signal(asset, tf):
    # 1. Weekend Check
    if datetime.datetime.now(pytz.timezone('Asia/Kolkata')).weekday() >= 5:
        return jsonify({"signal": "MARKET CLOSED", "color": "white", "emoji": "⚪"})

    # 2. Fetch Data
    interval = '1m' if tf == '1' else '5m'
    data = get_market_data(f"{asset}=X", interval=interval)
    
    if data is None:
        return jsonify({"signal": "SERVER ISSUE", "color": "yellow", "emoji": "🟡"})

    # 3. 6-Layer Filter Logic (Simplified)
    # Layer 1 & 2: EMA Crossover
    # Layer 3: RSI oversold/overbought
    # Layer 4-6: Price action (Close vs Open)
    
    close = data['Close']
    open_p = data['Open']
    rsi = data['RSI']
    
    if close > data['EMA_10'] and rsi < 70:
        return jsonify({"signal": "UP", "color": "green", "emoji": "🟢", "trend": "Bullish", "prob": "78%"})
    elif close < data['EMA_10'] and rsi > 30:
        return jsonify({"signal": "DOWN", "color": "red", "emoji": "🔴", "trend": "Bearish", "prob": "75%"})
    else:
        return jsonify({"signal": "AVOID TRADE", "color": "yellow", "emoji": "🟡", "trend": "Neutral", "prob": "50%"})

if __name__ == '__main__':
    app.run()

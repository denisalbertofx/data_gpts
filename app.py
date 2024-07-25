from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd
import talib

app = Flask(__name__)

def get_technical_indicators(df):
    df['SMA'] = talib.SMA(df['Close'], timeperiod=20)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['BB_upper'], df['BB_middle'], df['BB_lower'] = talib.BBANDS(df['Close'], timeperiod=20)
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    return df

@app.route('/analizar/<ticker>', methods=['GET'])
def analizar(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1mo", interval="1d")
    df = get_technical_indicators(df)
    data = df.to_dict(orient='index')
    return jsonify(data)

@app.route('/opciones/<ticker>', methods=['GET'])
def opciones(ticker):
    stock = yf.Ticker(ticker)
    options = stock.option_chain()
    calls = options.calls.to_dict(orient='records')
    puts = options.puts.to_dict(orient='records')
    return jsonify({"calls": calls, "puts": puts})

if __name__ == '__main__':
    app.run(debug=True)

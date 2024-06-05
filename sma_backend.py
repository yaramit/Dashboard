from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/backtest', methods=['POST'])
def backtest():
    data = request.json
    ticker = data['ticker']
    entry_condition = data['entry_condition']
    exit_condition = data['exit_condition']

    # Fetch stock data
    df = fetch_stock_data(ticker)

    # Calculate SMA
    df['SMA'] = df['Close'].rolling(window=9).mean()

    # Perform backtest
    results = perform_backtest(df, entry_condition, exit_condition)

    return jsonify(results)

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")  # Fetch 1 year of data
    return df

def perform_backtest(df, entry_condition, exit_condition):
    cash = 10000  # Starting with $10,000
    shares = 0
    entry_price = 0
    trades = []
    for index, row in df.iterrows():
        if eval(entry_condition):
            if shares == 0:  # Enter trade
                shares = cash // row['Close']
                cash -= shares * row['Close']
                entry_price = row['Close']
                trades.append(('BUY', index, shares, row['Close']))
        elif eval(exit_condition):
            if shares > 0:  # Exit trade
                cash += shares * row['Close']
                trades.append(('SELL', index, shares, row['Close']))
                shares = 0

    profit = cash - 10000
    winning_trades = [trade for trade in trades if trade[0] == 'SELL' and trade[3] > entry_price]
    losing_trades = [trade for trade in trades if trade[0] == 'SELL' and trade[3] <= entry_price]

    results = {
        'profit': profit,
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
        'trades': trades
    }

    return results

if __name__ == '__main__':
    app.run(debug=True)

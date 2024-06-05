import yfinance as yf 
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")  # Fetch 1 year of data
    return df  
print(fetch_stock_data("RELIANCE.NS"))
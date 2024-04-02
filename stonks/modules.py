import yfinance as yf
from tqdm import tqdm

# Downloading data
def download_data(tickers, start_date, end_date):
    stock_data = {}
    for ticker in tqdm(tickers):
        stock = yf.Ticker(ticker + ".ns")
        data = stock.history(start=start_date, end=end_date)
        stock_data[ticker] = data
    return stock_data


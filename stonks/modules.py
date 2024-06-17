import yfinance as yf
from tqdm import tqdm
import pandas as pd
from datetime import datetime


# Downloading data
def download_data(tickers, ticker_start_dates):
    stock_data = {}
    for ticker in tqdm(tickers):
        stock = yf.Ticker(ticker + ".ns")
        data = stock.history(start=ticker_start_dates[ticker], end=datetime.today())
        stock_data[ticker] = data
    return stock_data

def load_metadata(metadata_file):
    # List of stock tickers - You need to fill this with the tickers you want
    meta_data = pd.read_csv(metadata_file)  # Should be updated regularly monthly
    meta_data.columns = [i.strip() for i in meta_data.columns]
    meta_data["DATE OF LISTING"] = pd.to_datetime(meta_data["DATE OF LISTING"], format='%d-%b-%Y')
    tickers = meta_data['SYMBOL'].unique()
    dates_of_listing = meta_data.set_index('SYMBOL')[["DATE OF LISTING"]].to_dict()["DATE OF LISTING"]
    end_date = datetime.today()

    return(tickers, dates_of_listing)


def append_base_data():
    base_data = pd.read_parquet("/Users/akash/git/stonks/datasets/full_data.parquet")
    new_data = pd.read_parquet("/Users/akash/git/stonks/datasets/new_data.parquet")
    base_data = pd.concat([base_data, new_data], axis = 0)
    base_data.sort_index(by = ["ticker", "Date" ],inplace = True)
    base_data.reset_index(inplace = True)
    base_data.to_parquet("/Users/akash/git/stonks/datasets/full_data.parquet")

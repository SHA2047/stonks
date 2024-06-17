import pandas as pd
import os
from pathlib import Path
from modules import download_data, load_metadata

path = str(Path(os.getcwd()).parent)
tickers, dates_of_listing = load_metadata(path + "/configs/EQUITY_L.csv")

if os.path.exists(path + "/datasets/full_data.parquet"):
    df = pd.read_parquet(path + "/datasets/full_data.parquet", columns=["ticker", "Date"])
    df = df.groupby(["ticker"]).max()
    df['Date'] = df['Date'] + pd.DateOffset(days = 1)
    df['Date'] = df['Date'].dt.date
    dates_of_last_update = df.T.to_dict("records")[0]

# Saving data
stock_data = download_data(tickers, dates_of_last_update)

alldata = pd.DataFrame()
for ticker, data in stock_data.items():
    temp = data
    temp['ticker'] = ticker
    alldata = pd.concat([alldata, temp], axis=0)
alldata.reset_index(inplace=True)
alldata.to_parquet(path + "/datasets/new_data.parquet", index = False)
print("Data download complete.")

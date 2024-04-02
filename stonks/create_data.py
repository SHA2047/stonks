import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
from tqdm import tqdm
import sys
from modules import *

try:
    years = int(sys.argv[1])
except:
    years = 5

path = str(Path(os.getcwd()))
tickers = pd.read_csv(path + "/configs/EQUITY_L.csv")["SYMBOL"].tolist()
end_date = datetime.today()
start_date = datetime.today() - timedelta(days = 365*years + 2)

# Saving data
stock_data = download_data(tickers, start_date, end_date)
alldata = pd.DataFrame()
for ticker, data in stock_data.items():
    temp = data
    temp['ticker'] = ticker
    alldata = pd.concat([temp, alldata], axis = 0)
alldata.reset_index(inplace = True)

alldata.to_parquet(path + "/datasets/full_data.parquet")

print("1 time Data download complete.")
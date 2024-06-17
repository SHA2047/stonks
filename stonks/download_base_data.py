import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
from modules import load_metadata, download_data

path = str(Path(os.getcwd()).parent)
tickers, dates_of_listing = load_metadata(path)
end_date = datetime.today()

# Saving data
stock_data = download_data(tickers, dates_of_listing)
alldata = pd.DataFrame()
for ticker, data in stock_data.items():
    temp = data
    temp['ticker'] = ticker
    alldata = pd.concat([temp, alldata], axis = 0)
alldata.reset_index(inplace = True)
alldata.to_parquet(path + "/datasets/full_data.parquet", index = False)

print("Data download complete.")
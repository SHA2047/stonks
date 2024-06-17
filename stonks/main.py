import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta
import mplfinance as mpf
from datetime import datetime
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import os


class MyStrategy(Strategy):
    def init(self):
        self.sma_short = self.I(SMA, self.data.Close, 10)
        self.sma_long = self.I(SMA, self.data.Close, 20)

    def next(self):
        if crossover(self.sma_short, self.sma_long):
            self.buy()
        elif crossover(self.sma_long, self.sma_short):
            self.sell()


def load_and_preprocess_data(file_path):
    # Load data
    data = pd.read_parquet(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by=['ticker', 'Date'])

    return data


def calculate_technical_indicators(data):
    # Calculate technical indicators
    data['SMA10'] = data.groupby('ticker')['Close'].transform(lambda x: x.rolling(window=10).mean())
    data['SMA20'] = data.groupby('ticker')['Close'].transform(lambda x: x.rolling(window=20).mean())
    data['RSI'] = data.groupby('ticker')['Close'].transform(lambda x: ta.rsi(x, length=14))

    macd = data.groupby('ticker').apply(lambda x: ta.macd(x['Close'], fast=12, slow=26, signal=9))
    macd = macd.reset_index(level=0, drop=True)
    data = pd.concat([data, macd], axis=1)

    return data


def save_plot(stock_data, ticker, output_dir):
    mpf.plot(stock_data, type='candle', style='charles',
             title=f'{ticker} Backtest', ylabel='Price',
             volume=True, savefig=dict(fname=os.path.join(output_dir, f'{ticker}_backtest.png'), dpi=100))


def backtest_strategy(data, strategy, output_dir):
    results = []

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for ticker in data['ticker'].unique():
        stock_data = data[data['ticker'] == ticker]
        stock_data.set_index('Date', inplace=True)
        stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]

        bt = Backtest(stock_data, strategy, cash=10000, commission=.002)
        stats = bt.run()
        results.append((ticker, stats['Equity Final [$]']))

        save_plot(stock_data, ticker, output_dir)

    return results


def recommend_stocks(results, n=10):
    results.sort(key=lambda x: x[1], reverse=True)
    return [ticker for ticker, _ in results[:n]]


def main():
    # Load and preprocess data
    file_path = '/Users/akash/git/stonks/datasets/full_data.parquet'
    output_dir = '/Users/akash/git/stonks/outputs/backtest_plots'
    data = load_and_preprocess_data(file_path)

    # Calculate technical indicators
    data = calculate_technical_indicators(data)

    # Backtest strategies
    results = backtest_strategy(data, MyStrategy, output_dir)

    # Recommend stocks to buy
    recommendations = recommend_stocks(results)
    print("Top 10 stocks to buy:", recommendations)


if __name__ == '__main__':
    main()

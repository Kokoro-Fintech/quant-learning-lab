# Purpose: generate indicators and plot TA and ohlc data

import pandas as pd
import numpy as np
import mplfinance as mpf
import talib as ta  # TA-Lib is used for technical analysis calculations

# Read the HDF5 file into a DataFrame
df = pd.read_hdf("EUR_USD_5M_TA.h5", key="data")

# Ensure the 'time' column exists and convert it to datetime
if 'time' in df.columns:
    # Directly convert the 'time' column to datetime without specifying the unit
    df.index = pd.to_datetime(df['time'])
else:
    print("Error: 'time' column not found!")
    exit()

# Select only the necessary OHLC columns
if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
    df = df[['open', 'high', 'low', 'close']]  # Select OHLC columns
else:
    print("Error: Missing OHLC columns!")
    exit()

# Calculate the indicators
df['20_SMA'] = df['close'].rolling(window=20).mean()
df['66_SMA'] = df['close'].rolling(window=66).mean()
df['200_SMA'] = df['close'].rolling(window=200).mean()

# Bollinger Bands
df['Upper_BB'], df['Lower_BB'] = ta.BBANDS(df['close'], timeperiod=20)

# MACD and Signal
df['MACD'], df['MACD_Signal'], _ = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

# RSI (Relative Strength Index)
df['RSI'] = ta.RSI(df['close'], timeperiod=14)

# ATR (Average True Range)
df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=14)

# Create custom indicator plot styles
custom_colors = {
    'sma20': 'blue',
    'sma66': 'green',
    'sma200': 'red',
    'macd': 'purple',
    'macd_signal': 'orange',
    'macd_histogram': 'gray',
    'upper_bb': 'pink',
    'lower_bb': 'pink',
    'rsi': 'yellow',
    'atr': 'cyan'
}

# Create the addplot list for the indicators
apds = [
    mpf.make_addplot(df['20_SMA'], color=custom_colors['sma20'], width=1),
    mpf.make_addplot(df['66_SMA'], color=custom_colors['sma66'], width=1),
    mpf.make_addplot(df['200_SMA'], color=custom_colors['sma200'], width=1),
    mpf.make_addplot(df['MACD'], panel=1, color=custom_colors['macd'], width=1),
    mpf.make_addplot(df['MACD_Signal'], panel=1, color=custom_colors['macd_signal'], width=1),
    mpf.make_addplot(df['MACD_Histogram'], panel=1, color=custom_colors['macd_histogram'], width=0.7, secondary_y=True),
    mpf.make_addplot(df['Upper_BB'], color=custom_colors['upper_bb'], width=1),
    mpf.make_addplot(df['Lower_BB'], color=custom_colors['lower_bb'], width=1),
    mpf.make_addplot(df['RSI'], panel=2, color=custom_colors['rsi'], width=1),
    mpf.make_addplot(df['ATR'], panel=3, color=custom_colors['atr'], width=1)
]

# Plot the figure
mpf.plot(df,
         type='candle',
         addplot=apds,
         title="EUR/USD with Indicators",
         ylabel='Price',
         ylabel_panel=0,
         panel_ratios=(3,1,1,1),
         figsize=(12, 8),
         style='yahoo')

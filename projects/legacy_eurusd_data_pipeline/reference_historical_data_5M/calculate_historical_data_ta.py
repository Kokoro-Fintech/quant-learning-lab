# Purpose: Calculate indicators I use and append as columns in new csv and h5

import pandas as pd
import numpy as np

# Load historical data
try:
    df = pd.read_csv("historical_data.csv")
except FileNotFoundError:
    print("Error: historical_data.csv not found.")
    exit()

# Ensure data is sorted by time
df = df.sort_values(by="time").drop_duplicates(subset=["time"])

# --- SMA Calculation ---
df["66_SMA"] = df["close"].rolling(window=66, min_periods=1).mean()
df["200_SMA"] = df["close"].rolling(window=200, min_periods=1).mean()

# --- MACD and Histogram ---
def compute_macd(df, short_window=12, long_window=26, signal_window=9):
    short_ema = df["close"].ewm(span=short_window, adjust=False).mean()
    long_ema = df["close"].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    macd_signal = macd.ewm(span=signal_window, adjust=False).mean()
    macd_histogram = macd - macd_signal
    return macd, macd_signal, macd_histogram

df["MACD"], df["MACD_Signal"], df["MACD_Histogram"] = compute_macd(df)

# --- Bollinger Bands ---
def compute_bollinger_bands(df, window=20, num_std=2):
    sma = df["close"].rolling(window=window, min_periods=1).mean()
    std_dev = df["close"].rolling(window=window, min_periods=1).std()
    upper_bb = sma + (num_std * std_dev)
    lower_bb = sma - (num_std * std_dev)
    return sma, upper_bb, lower_bb

df["20_SMA"], df["Upper_BB"], df["Lower_BB"] = compute_bollinger_bands(df)

# --- RSI Calculation ---
def compute_rsi(df, window=14):
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df["RSI"] = compute_rsi(df)

# --- ATR Calculation ---
def compute_atr(df, window=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    true_range = np.maximum.reduce([high_low, high_close, low_close])
    atr = pd.Series(true_range).rolling(window=window, min_periods=1).mean()
    return atr

df["ATR"] = compute_atr(df)

# --- VWAP Calculation ---
def compute_vwap(df):
    tp = (df["high"] + df["low"] + df["close"]) / 3  # Typical Price
    cumulative_tpv = (tp * df["volume"]).cumsum()
    cumulative_volume = df["volume"].cumsum()
    vwap = cumulative_tpv / cumulative_volume
    return vwap

df["VWAP"] = compute_vwap(df)

# Save processed data
df.to_csv("historical_data_ta.csv", index=False)
df.to_hdf("historical_data_ta.h5", key="data", mode="w", format="table")

print("Technical indicators calculated and saved successfully.")

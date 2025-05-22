# Purpose: plot ohlc data using mplfinance

import pandas as pd
import mplfinance as mpf

# Load the CSV file
file_path = "EUR_USD_5M.csv"  # Update with your actual file path
df = pd.read_csv(file_path, parse_dates=['time'], index_col='time')

# Ensure correct column names for mplfinance
df = df[['open', 'high', 'low', 'close']]

# Define custom market colors
mc = mpf.make_marketcolors(
    up='royalblue',         # Blue for bullish candles
    down='indigo',          # Dark purple for bearish candles
    edge={'up': 'deepskyblue', 'down': 'mediumpurple'},  # Outline colors
    wick='lightgray',       # Light gray wicks
    volume='dimgray'        # Optional: volume color
)

# Define the overall style
style = mpf.make_mpf_style(
    marketcolors=mc,
    base_mpf_style='nightclouds',  # Dark background similar to TradingView
    gridcolor='black',             # Hide grid or set to a subtle dark gray
    figcolor='black'               # Black background
)

# Plot the candlestick chart with the custom style
mpf.plot(df, type='candle', style=style, title="EUR/USD 5M Candlestick Chart", ylabel="Price")

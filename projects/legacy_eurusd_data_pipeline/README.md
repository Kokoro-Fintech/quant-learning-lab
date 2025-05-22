# (Legacy) EURUSD Data Pipeline

This folder documents an early version of a EUR/USD 5-minute candlestick data pipeline originally built using the OANDA API. While initially intended for strategy development, its main function became prototyping a dedicated historical data collection module. The logic here laid the groundwork for a more scalable architecture now used in the main quant system.

---

## 📁 Folder Structure

### `intro_references/`
- Fetches 5-minute OHLCV data from OANDA and saves to `.csv`
- Uses `mplfinance` to create styled candlestick plots
- Overlays basic technical indicators using TA-Lib:
  - Simple Moving Averages (SMA)
  - MACD
  - Bollinger Bands
  - RSI
  - ATR
- Emphasizes modularity: separating raw data collection, visualization, and indicator overlays

### `reference_historical_data_5M/`
- Early implementation of a dynamic ingestion pipeline
- Merges historical 5-minute candles up to a set date
- Calculates indicators without external TA libraries
- Outputs stored in `.h5` format (no longer used)
- Includes small `.csv` samples to illustrate generated data

---

## ✅ Purpose

- Serve as proof-of-concept for early data handling
- Archive the developmental path toward a more robust data pipeline
- Retained for documentation and historical context

---

## ❌ Known Limitations

- Code relies on live OANDA API calls
- No strategy or signal generation logic implemented
- Not compatible with current multiprocessing or multi-timeframe framework
- `.h5` format deprecated in favor of readable `.csv` files

---

## 🧪 Status

This project is archived and no longer actively maintained. It has been fully superseded by a more advanced and performant data pipeline used in the main quant system.

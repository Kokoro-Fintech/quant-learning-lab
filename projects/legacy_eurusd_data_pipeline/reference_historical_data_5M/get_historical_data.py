# Purpose: dynamically call API and merge temporary ohlcv into permanent file until specified date

import requests
import pandas as pd
import sys
from datetime import datetime, timedelta, timezone
import pytz  # Import pytz for timezone conversion

sys.path.append('//Oanda_API')
from oanda_demo_api import get_decrypted_api_key  # Importing the function
from merge_historical_data import merge_data

# OANDA API credentials
api_url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
access_token = get_decrypted_api_key()  # Call the function to get the actual token


def get_most_recent_saturday_noon():
    """Finds the most recent Saturday at noon in UTC."""
    eastern = pytz.timezone("US/Eastern")
    now = datetime.now(eastern)
    last_saturday = now - timedelta(days=(now.weekday() + 2) % 7)  # Move back to Saturday
    last_saturday_noon = last_saturday.replace(hour=12, minute=0, second=0, microsecond=0)
    return last_saturday_noon.astimezone(pytz.utc)


def fetch_weekly_data(start_time, end_time):
    """Fetches one week of 5-minute historical data from OANDA."""
    params = {
        'granularity': 'M5',  # 5-minute candles
        'price': 'M',  # Midpoint price
        'smooth': 'false',  # Don't smooth the data
        'from': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'to': end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        candles = data.get('candles', [])

        if not candles:
            return pd.DataFrame()  # Return empty DataFrame if no data

        df = pd.DataFrame([{
            'time': candle['time'],
            'open': float(candle['mid']['o']),
            'high': float(candle['mid']['h']),
            'low': float(candle['mid']['l']),
            'close': float(candle['mid']['c']),
            'volume': float(candle['volume'])
        } for candle in candles])

        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        return df
    else:
        print(f"Error fetching data: {response.status_code}, {response.text}")
        return pd.DataFrame()


def collect_historical_data():
    """Loops through weeks, collecting and saving historical data until January 2023."""
    end_time = get_most_recent_saturday_noon()
    start_time = end_time - timedelta(weeks=1)
    cutoff_date = datetime(2023, 1, 7, 12, 0, tzinfo=timezone.utc)  # First Saturday of January 2023

    while start_time >= cutoff_date:
        print(f"Fetching data from {start_time} to {end_time}...")
        df_week = fetch_weekly_data(start_time, end_time)

        if not df_week.empty:
            df_week.index = df_week.index.tz_convert('America/New_York')  # Convert to New York time
            df_week.to_csv('historical_data_week.csv')
            merge_data('historical_data.csv', 'historical_data_week.csv', 'time')
            print(f"Saved historical_data_week.csv for {start_time.date()} to {end_time.date()}")
        else:
            print(f"No data found for {start_time.date()} to {end_time.date()}")

        # Move back one week
        end_time = start_time
        start_time -= timedelta(weeks=1)


if __name__ == "__main__":
    collect_historical_data()

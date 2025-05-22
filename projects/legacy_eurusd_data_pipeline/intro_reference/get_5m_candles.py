# Purpose: get 5M ohlcv data from Oanda API

import requests
import pandas as pd
import sys
from datetime import datetime, timezone, timedelta
import pytz  # Import pytz for timezone conversion

sys.path.append('/Oanda_API')
from oanda_demo_api import get_decrypted_api_key  # Importing the function

# OANDA API credentials
api_url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
access_token = get_decrypted_api_key()  # Call the function with parentheses to get the actual token

# Get the current time and subtract a certain period (e.g., 1 day) for the start time
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=17)  # Adjust this to fetch a larger range, e.g., last 7 days

# Request parameters (without 'count')
params = {
    'granularity': 'M5',  # 5-minute candles
    'price': 'M',  # Midpoint price (can be adjusted)
    'smooth': 'false',  # Don't smooth the data (use raw data)
    'from': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),  # 'from' parameter for start time
    'to': end_time.strftime('%Y-%m-%dT%H:%M:%SZ')  # 'to' parameter for end time
}

# Headers for authorization
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Function to fetch data with pagination support
def fetch_candles():
    all_candles = []
    next_url = api_url  # Start with the initial URL

    while next_url:
        response = requests.get(next_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            candles = data['candles']  # Corrected to 'candles'
            all_candles.extend(candles)
            # Check if there's a next page of results
            next_url = data.get('next', None)  # If there's no next page, `next` will be None
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break

    # Convert the JSON response to a pandas DataFrame
    if all_candles:
        df = pd.DataFrame([{
            'time': candle['time'],
            'open': float(candle['mid']['o']),
            'high': float(candle['mid']['h']),
            'low': float(candle['mid']['l']),
            'close': float(candle['mid']['c']),
        } for candle in all_candles])

        # Convert the time to a datetime object (UTC)
        df['time'] = pd.to_datetime(df['time'])

        # Convert the 'time' column from UTC to Eastern Time
        eastern = pytz.timezone("US/Eastern")  # Change to your preferred timezone
        df['time'] = df['time'].dt.tz_convert(eastern)  # Just convert from UTC to the target timezone

        df.set_index('time', inplace=True)

        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data was fetched

# Fetch the data and return the DataFrame
df_live = fetch_candles()

# Optionally, save to CSV for later use
if not df_live.empty:
    df_live.to_csv('EUR_USD_5M.csv')
    print(df_live.tail())  # Print first few rows of the DataFrame

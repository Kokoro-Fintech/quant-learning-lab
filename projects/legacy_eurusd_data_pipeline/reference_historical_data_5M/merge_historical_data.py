# Purpose: Logic to merge temporary data into persistent file

import pandas as pd
import os

def merge_data(historical_file: str, weekly_file: str, key_column: str = "time") -> None:
    """
    Merges weekly_file into historical_file, removing duplicates based on key_column.

    Args:
        historical_file (str): Path to the main historical CSV.
        weekly_file (str): Path to the new weekly CSV to merge.
        key_column (str): Column name to use for identifying duplicates. Default is 'time'.
    """

    historical_file = 'historical_data.csv'
    weekly_file = 'historical_data_week.csv'

    if not os.path.exists(weekly_file):
        print(f"[!] No new weekly data found: {weekly_file}")
        return

    df_weekly = pd.read_csv(weekly_file, parse_dates=[key_column])

    if os.path.exists(historical_file):
        df_historical = pd.read_csv(historical_file, parse_dates=[key_column])
        df_combined = pd.concat([df_historical, df_weekly], ignore_index=True)
    else:
        print(f"[!] No historical file found. Creating new file from: {weekly_file}")
        df_combined = df_weekly

    df_combined.drop_duplicates(subset=[key_column], inplace=True)
    df_combined.sort_values(by=key_column, inplace=True)

    df_combined.to_csv(historical_file, index=False)
    print(f"[✓] Merged '{weekly_file}' into '{historical_file}' successfully. Total rows: {len(df_combined)}")

# Purpose:
# This script visualizes a double-layered linear regression channel and its dynamic behavior over time.
# The first regression estimates trend and deviation bands on the price series (like a modified Bollinger Band).
# The second regression (or finite difference) is applied to the evolving slope of the first regression,
# approximating the second derivative (acceleration) to capture momentum shifts in trend strength.
# The result is an animated plot that helps visualize both trend direction and changes in trend velocity.

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Config ---
window1 = 100  # First linear regression window (price)
window2 = 10   # Second linear regression window (on slopes)
std_dev_multiplier = 2

# --- Load CSV ---
df = pd.read_csv('sample_data.csv')
df = df[['time', 'close']]

# Prepare containers
slopes = []
intercepts = []
reg_lines = []
upper_bands = []
lower_bands = []

price_window = deque(maxlen=window1)
slope_window = deque(maxlen=window2)
slope_acceleration = []

# --- Animation update function ---
def update(frame):
    if frame < window1:
        return []

    # --- First Linear Regression ---
    price_window.clear()
    for i in range(frame - window1, frame):
        price_window.append(df['close'].iloc[i])

    x = np.arange(window1).reshape(-1, 1)
    y = np.array(price_window)

    model = LinearRegression()
    model.fit(x, y)

    slope = model.coef_[0]
    intercept = model.intercept_
    y_pred = model.predict(x)
    std_dev = np.std(y - y_pred)

    reg_mid = y_pred[-1]
    reg_upper = reg_mid + std_dev_multiplier * std_dev
    reg_lower = reg_mid - std_dev_multiplier * std_dev

    slopes.append(slope)
    intercepts.append(intercept)
    reg_lines.append(reg_mid)
    upper_bands.append(reg_upper)
    lower_bands.append(reg_lower)

    # --- Second Derivative Approximation ---
    slope_window.append(slope)
    if len(slope_window) < window2:
        slope_acceleration.append(0)
    else:
        if window2 == 2:
            # Finite difference
            accel = slope_window[-1] - slope_window[-2]
        else:
            # Second regression over slopes
            x2 = np.arange(window2).reshape(-1, 1)
            y2 = np.array(slope_window)
            model2 = LinearRegression()
            model2.fit(x2, y2)
            accel = model2.coef_[0]
        slope_acceleration.append(accel)

    # --- Plotting ---
    ax1.clear()
    ax2.clear()

    # Plot price and regression channel
    ax1.plot(df['close'][:frame], label='Price')
    ax1.plot(range(window1, frame+1), reg_lines, label='Regression Line')
    ax1.plot(range(window1, frame+1), upper_bands, linestyle='--', label='Upper Band')
    ax1.plot(range(window1, frame+1), lower_bands, linestyle='--', label='Lower Band')
    ax1.legend(loc='upper left')
    ax1.set_title('Rolling Regression Channel')

    # Plot slope acceleration (2nd derivative)
    ax2.plot(range(window1+1, frame+1), slope_acceleration[1:], color='green', label='Slope Acceleration')
    ax2.legend(loc='upper left')
    ax2.set_title('2nd Derivative via Regression or Finite Difference')

    ax1.grid(True)
    ax2.grid(True)

    return []

# Setup figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
ani = FuncAnimation(fig, update, frames=len(df), interval=50, repeat=False)
plt.show()
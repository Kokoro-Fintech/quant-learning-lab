# Purpose: Create a floating window to monitor/change in_trade
# Not working

import tkinter as tk
import json
import os
import subprocess
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem

# Path to the JSON file
JSON_FILE = "trade_status.json"

# Load trade status from JSON
try:
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        in_trade = data.get("in_trade", False)
except (FileNotFoundError, json.JSONDecodeError):
    in_trade = False

# Function to save trade status to JSON
def save_trade_status(status):
    global in_trade
    in_trade = status
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump({"in_trade": in_trade}, file, indent=4)

# Function to toggle trade status
def toggle_trade_status():
    new_status = not in_trade
    save_trade_status(new_status)
    update_ui()

# Function to update UI
def update_ui():
    toggle_button.config(text="IN TRADE" if in_trade else "NO TRADE")

# Force window to behave like a notification overlay
def force_floating_window():
    NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-fullscreen', False)
    root.attributes('-type', 'floating')  # Forces it into notification layer

# Create tkinter window
root = tk.Tk()
root.title("Trade Status")
root.geometry("200x100")
root.resizable(False, False)

# Toggle button
toggle_button = tk.Button(root, text="NO TRADE", command=toggle_trade_status)
toggle_button.pack(pady=20)

# Close button
close_button = tk.Button(root, text="Close", command=root.destroy)
close_button.pack()

# Run floating window control
force_floating_window()
update_ui()
root.mainloop()

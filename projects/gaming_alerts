# Purpose: Monitor gaming activity and message at 30 minute intervals using macOS and Automator

import time
import subprocess
import random

# List of gaming apps to monitor (case-sensitive, must match Activity Monitor or 'pgrep -fl' output)
GAMING_APPS = ["Dolphin", "Cemu", "Ryujinx"]

# Open messages (short, gaming-focused)
OPEN_MESSAGES = [
    "Game on. Let the fun begin.",
    "You're in. Let's go!",
    "Time to level up.",
    "Game session started.",
    "You’re in the arena.",
    "Ready. Set. Game.",
    "It’s game time."
]

# Closed messages
CLOSED_MESSAGES = [
    "Game session complete.",
    "You’ve closed the emulator.",
    "That was fun.",
    "Session ended.",
    "You’re out of the game.",
    "Back to reality.",
    "Closed. GG."
]

# Send a notification on macOS
def send_notification(title, message, sound="Glass"):
    script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
    subprocess.run(["osascript", "-e", script])

# Check if any monitored app is open
def is_any_game_open():
    for app in GAMING_APPS:
        try:
            subprocess.check_output(["pgrep", "-f", app], text=True)
            return True
        except subprocess.CalledProcessError:
            continue
    return False

# Main loop
def gaming_alerts_loop():
    app_open = False
    start_time = None
    last_interval_notice = 0

    while True:
        currently_open = is_any_game_open()

        if currently_open and not app_open:
            # Game just started
            start_time = time.time()
            last_interval_notice = start_time
            app_open = True
            message = random.choice(OPEN_MESSAGES)
            send_notification("Game Detected", message)

        elif currently_open and app_open:
            # Game still running — send 30-minute update
            now = time.time()
            if now - last_interval_notice >= 1800:  # 30 minutes
                minutes_played = int((now - start_time) / 60)
                send_notification("Gaming Duration", f"You’ve been playing for {minutes_played} minutes.")
                last_interval_notice = now

        elif not currently_open and app_open:
            # Game just closed
            app_open = False
            message = random.choice(CLOSED_MESSAGES)
            send_notification("Game Closed", message)

        time.sleep(5)

# Run it
gaming_alerts_loop()

# Automator> New Document > Run Shell Script
# #!/bin/bash
# while true; do
#     /usr/bin/python3 "/Users/C-Standard/Desktop/Matrix_Files/PyCharm Files/introductory_projects/trading_alerts.py"
#     sleep 5  # If script crashes, restart it after 5 seconds

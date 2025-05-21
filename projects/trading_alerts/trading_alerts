# Purpose: tracks if I am in a trade to provide psychological support

import time
import subprocess
import json
import random

# Path to the trading app
TRADING_APP = "Liquid Charts Desktop"
JSON_FILE = "trade_status.json"

# Global variables to track state
in_trade = False
app_open = False

# Define the four possible states
STATE_1 = (True, True)   # In trade, App open
STATE_2 = (True, False)  # In trade, App closed
STATE_3 = (False, True)  # Not in trade, App open
STATE_4 = (False, False) # Not in trade, App closed

# Notification message libraries for each state
STATE_MESSAGES = {
    "STATE_1": [
        "You're in a trade, and the app is open. Stick to your strategy. Don't let emotions dictate your decisions.",
        "Embrace your plan. Fundamental analysis is your ally. Emotions are for spectators, not traders.",
        "Focus on the fundamentals. Stay calm and let the data do the talking. You've got this!",
        "The charts are your compass. Keep your emotions in check, and let the market show you the way.",
        "Stay disciplined! Your strategy is solid. Trust it and avoid the emotional rollercoaster.",
        "Stay focused on the numbers, not the noise. Emotions will cloud your judgment, but your plan is clear.",
        "Fundamental analysis is your foundation. Stick to it, and you'll find success. Let emotions be a thing of the past."
    ],
    "STATE_2": [
        "Trade set, TP and SL in place. You've done the work. Now step away and trust the plan.",
        "Confidence is key. Your strategy is sound, and your risk is managed. Let it work for you.",
        "You’ve set the trap; now let the market come to you. Trust the process, and don't sweat the result.",
        "Your trade is like a well-laid foundation. You've set your goals and parameters. Now relax and let the market do its thing.",
        "With your TP and SL set, there’s nothing left to do but trust your analysis and take a breather.",
        "The market knows the way; you've already paved your path. Let the trade breathe on its own.",
        "Confidence isn’t about control; it’s about trust. Trust your strategy, and everything else will fall into place."
    ],
    "STATE_3": [
        "Patience is key. The market will come to you. No need to rush; a good trade will present itself.",
        "No trade is better than a bad trade. Stay patient, and the right opportunity will show itself.",
        "Waiting isn’t a waste; it’s preparation. When the time comes, you’ll know exactly what to do.",
        "The market is like the ocean, and you’re waiting for the perfect wave. Don’t force it—let the trade come to you.",
        "A calm trader is a successful trader. Wait for the setup that fits your plan and don’t settle for less.",
        "Opportunities are like buses. If you miss one, another will come around. Don’t force the trade.",
        "Good trades are like good wine. They take time to mature. Don’t rush; wait for your moment."
    ],
    "STATE_4": [
        "Remember, trading is a means to an end. It's not your life, just a tool to get the life you want.",
        "Mental clarity is more important than any trade. Take a break, recharge, and come back stronger.",
        "Trading is a journey, not a race. Your well-being is the priority—let the market wait for you.",
        "Balance is the key. Trading is part of your life, not your entire life. Take time to step away and refresh.",
        "The market will always be there. Your mental peace? Not so much. Take care of yourself first.",
        "Success in trading starts with a clear mind. Let go of the stress, and trade when you're truly ready.",
        "The best traders know when to step back. Remember, you’re doing this to live a better life, not to live in front of a screen."
    ]
}

# Function to send a random notification for the current state
def send_state_notification(state_key):
    if state_key in STATE_MESSAGES:
        message = random.choice(STATE_MESSAGES[state_key])  # Pick a random message
        send_notification("Trading Alert", message)

# Function to load trade status from JSON
def load_trade_status():
    global in_trade
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            in_trade = data.get("in_trade", False)
    except (FileNotFoundError, json.JSONDecodeError):
        in_trade = False
        save_trade_status()  # Create the file if it doesn't exist


# Function to save trade status to JSON
def save_trade_status():
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump({"in_trade": in_trade}, file, indent=4)
    except Exception as e:
        print(f"Error saving trade status: {e}")


# Function to check if Liquid Charts is running
def is_trading_app_open():
    try:
        output = subprocess.check_output(["pgrep", "-f", TRADING_APP], text=True)
        return bool(output.strip())
    except subprocess.CalledProcessError:
        return False


# Function to send macOS notifications
def send_notification(title, message, sound="Glass", duration=10):
    script = f'''
    display notification "{message}" with title "{title}" sound name "{sound}"
    delay {duration}  # This will keep the notification displayed for the specified time
    '''
    subprocess.run(["osascript", "-e", script])


# Function to ask "Are you in a trade?" with Yes/No dialog
def ask_trade_status():
    global in_trade
    script = '''
    tell application "System Events"
        set response to display dialog "Are you in a trade?" with title "Trade Status" buttons {"Yes", "No"} default button "No"
        return button returned of response
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    response = "Yes" in result.stdout

    # Update trade status and save
    in_trade = response
    save_trade_status()
    print(f"Trade Status Updated: in_trade = {in_trade}")


# Function to send notifications based on current state
def check_and_notify():
    current_state = (in_trade, app_open)

    # Send notifications based on state using send_state_notification
    if current_state == STATE_1:
        send_state_notification("STATE_1")
    elif current_state == STATE_3:
        send_state_notification("STATE_3")
    elif current_state == STATE_4:
        send_state_notification("STATE_4")


# Main function that continuously runs
def trading_alerts_loop():
    global in_trade, app_open

    # Load trade status at startup
    load_trade_status()
    last_state = (in_trade, False)  # Assume app is closed at startup

    # Print initial state immediately
    print(f"in_trade = {in_trade}, app_open = {app_open}")

    while True:
        app_open = is_trading_app_open()
        current_state = (in_trade, app_open)

        # Detect state changes
        if current_state != last_state:
            print(f"State change detected: {last_state} → {current_state}")  # Print detected change
            print(f"Updated State: in_trade = {in_trade}, app_open = {app_open}")  # Print the actual values

            # Check if the app was open and is now closed
            if last_state[1] == True and app_open == False:
                print("App closed. Asking for trade status.")
                ask_trade_status()  # Ask for trade status before sending any notifications

                # After asking for the trade status, update the state
                current_state = (in_trade, app_open)  # Ensure that we update the state after asking
                print(f"Trade status after asking: in_trade = {in_trade}, app_open = {app_open}")

            # Update last_state after checking and possibly updating
            last_state = current_state

            # If we are in State 2 (in_trade, app_open=False), we should send the notification
            if current_state == STATE_2:
                print(f"State 2 detected: in_trade = {in_trade}, app_open = {app_open}")
                check_and_notify()  # Send notification after confirming trade status

            # Trigger notifications for states 1, 3, and 4 immediately
            if current_state in [STATE_1, STATE_3, STATE_4]:
                check_and_notify()

            # Delay notification for STATE_2 until after confirming trade status
            if current_state == STATE_2:
                check_and_notify()  # Now send notification after confirmation

            # Delay "Are you in a trade?" question if app is open
            if app_open:
                time.sleep(60)  # Wait before first question
                while is_trading_app_open():
                    ask_trade_status()

                    # If trade is confirmed, immediately send notification
                    if in_trade:
                        send_state_notification("STATE_1")

                    time.sleep(300)  # Ask every 10 seconds

        time.sleep(5)  # Check every 5 seconds


# Start the script and keep it running
trading_alerts_loop()

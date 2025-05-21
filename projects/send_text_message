# Purpose: interact with macOS to send a text message using python through Apple Messages

import subprocess

def send_imessage(phone_number, message_text):
    apple_script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        send "{message_text}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script])

contact1 = "+18009992222"
contact2 = "+18002229999"


# Usage
send_imessage(contact1, "Hi! I sent this by python!")

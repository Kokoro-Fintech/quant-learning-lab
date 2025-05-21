# Purpose: to prompt a yes/no box to appear before a script is allowed to run

import subprocess

def ask_permission():
    # AppleScript command to show a dialog box with Yes and No
    script = '''
    display dialog "Do you want to run the script?" buttons {"No", "Yes"} default button "No"
    '''
    try:
        # Run AppleScript
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        return "Yes" in result.stdout
    except Exception as e:
        print("Error showing dialog:", e)
        return False

if __name__ == "__main__":
    if ask_permission():
        print("The script ran")
    else:
        print("The script wasn't ran")

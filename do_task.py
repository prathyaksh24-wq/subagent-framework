import time
import os
import subprocess
import urllib.parse
import pyperclip
import pyautogui

def main():
    # Clear clipboard
    pyperclip.copy("")
    
    # 1. Open Google Meet new meeting page
    print("Opening Google Meet...")
    subprocess.run('start brave "https://meet.google.com/new"', shell=True)
    
    # 2. Wait for Google Meet to redirect
    time.sleep(8)
    
    # 3. Focus address bar and copy
    print("Copying link...")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    
    meet_link = pyperclip.paste()
    if "meet.google" not in meet_link:
        print("Fallback to generic meet link.")
        meet_link = "https://meet.google.com/new"
        
    print(f"Captured link: {meet_link}")
    
    # 4. Close the meet tab
    print("Closing Meet tab...")
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    
    # 5. We are now back to the YouTube tab. Close it.
    print("Closing YouTube tab...")
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    
    # 6. Compose email in Gmail
    print("Opening Gmail compose window...")
    subject = "Meeting at 6pm"
    body = f"Hi Saksham,\n\nLet's meet at 6pm. Here is the meeting link:\n{meet_link}\n\nThanks"
    
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
    
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=saksham&su={subject_encoded}&body={body_encoded}"
    
    subprocess.run(f'start brave "{gmail_url}"', shell=True)
    
    print("Done")

if __name__ == "__main__":
    main()

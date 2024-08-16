import pyautogui
import time
import os
import Private_keys
from twilio.rest import Client
from playsound import playsound
from datetime import datetime
from tkinter import *

pyautogui.FAILSAFE = True  # NEVER TURN THIS OFF!

# Constant time delay
pyautogui.PAUSE = 0.4

# User Variables

number_of_tabs = 80
Starting_delay = 5
template_name = "Vacant Position-Data Infrastructure Engineer, Software Engineer IV (4985)"

# Base Screenshots
email_scs = "./Screenshots/email.png"
email_box_scs = "./Screenshots/email-box.png"
okay_scs = "./Screenshots/okay.png"
msg_scs = "./Screenshots/msg.png"
search_scs = "./Screenshots/search.png"
send_scs = "./Screenshots/send.png"

# Screenshot naming and save directory
directory = "C:/Users/Muzna/Pictures/Screenshots"
base_name = "result"



error_msg_show = False


# Starting Delay
time.sleep(Starting_delay)

def play_sound(sound: str, dir: str, repeat: int):
    for count in range(repeat):
        playsound(os.path.join(dir, sound))
        time.sleep(0.3)

# Defining a unique filename generator using a timestamp function
def get_unique_filename(directory, base_name, extension=".png"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"{base_name}_{timestamp}{extension}")
    return filename

for number in range(number_of_tabs + 1):
    try:
        # Clicking the Add Email option
        email_x, email_y = pyautogui.center(pyautogui.locateOnScreen(email_scs, confidence=0.7))
        pyautogui.click(email_x, email_y, button="left", duration=0.2)

        # Clicking the Email box
        email_box_x, email_box_y = pyautogui.center(pyautogui.locateOnScreen(email_box_scs, confidence=0.7))
        pyautogui.click(email_box_x, email_box_y, button="left", duration=0.2)

        # Typing an Email into the box
        pyautogui.typewrite("a@gmail.com")

        # Clicking Okay
        okay_x, okay_y = pyautogui.center(pyautogui.locateOnScreen(okay_scs, confidence=0.7))
        pyautogui.click(okay_x, okay_y, button="left", duration=0.2)

        # Opening Message Box
        msg_x, msg_y = pyautogui.center(pyautogui.locateOnScreen(msg_scs, confidence=0.7))
        pyautogui.click(msg_x, msg_y, button="left", duration=0.2)

        # Reloading the page
        pyautogui.hotkey("F5")

        # Delay for page refresh
        time.sleep(5)

        # Selecting the search template bar
        search_x, search_y = pyautogui.center(pyautogui.locateOnScreen(search_scs, confidence=0.7))
        pyautogui.click(search_x, search_y, button="left", duration=0.2)

        # Searching for the specified template
        pyautogui.typewrite(template_name)

        # Delay for template selection
        time.sleep(0.7)

        # Template selection time delay
        time.sleep(0.8)

        # Selecting the template
        pyautogui.press("down")
        pyautogui.press("enter")

        # Pressing the send button
        send_x, send_y = pyautogui.center(pyautogui.locateOnScreen(send_scs, confidence=0.7))
        pyautogui.click(send_x, send_y, button="left", duration=0.2)

        # Waiting for the message
        time.sleep(3)
        
        # Generate a unique filename
        unique_filename = get_unique_filename(directory, base_name)
        
        # Taking a screenshot and saving it in the relevant directory
        pyautogui.screenshot(unique_filename)

        # Closing current tab
        pyautogui.hotkey("ctrl", "tab")

    except pyautogui.ImageNotFoundException:
        if error_msg_show == False:
            play_sound("alert.mp3", "Sounds", 4)
            root = Tk("Error")
            error_label = Label(text=f"Error: Image Not Found", font="Ariel", height=30, width=30) 
            error_label.pack()
            error_msg_show = True
            client = Client(Private_keys.account_sid, Private_keys.auth_token)

            message = client.messages.create(
            from_=f'whatsapp:{Private_keys.twillio_default_number}',
            body='Error: Automation has ended with an error!',
            to=f'whatsapp:{Private_keys.user_phone_number}'
)
            root.mainloop()
        else:
            break
        continue

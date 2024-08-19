import pyautogui
import time
import os
import Private_keys
import threading
import pygame
import test
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from datetime import datetime
from tkinter import *
from customtkinter import *

# System Variables
pyautogui.FAILSAFE = True  # NEVER TURN THIS OFF!
error_msg_show = False
twilio_destroy = False



# Constant time delay
pyautogui.PAUSE = 0.5

# User Variables

number_of_tabs = 80
starting_delay = 5
template_name = "AWS & Typescript"
tab_close = False
Whatsapp_msg_send = True

# User Screenshots
email_scs = "./Screenshots/email.png"
email_box_scs = "./Screenshots/email-box.png"
okay_scs = "./Screenshots/okay.png"
msg_scs = "./Screenshots/msg.png"
search_scs = "./Screenshots/search.png"
send_scs = "./Screenshots/send.png"

# Screenshot naming and save directory
directory = "C:/Users/Muzna/Pictures/Screenshots"
base_name = "result"

# Functions
def check_twilio_credentials(accountsid, authtoken):
    try:
        client = Client(accountsid, authtoken)
        # Attempt to fetch the account details
        client.api.v2010.accounts(accountsid).fetch()
        return True
    except TwilioRestException:
        return False
    except Exception:
        return True

def play_sound(sound: str, dir: str, repeat: int):
    # Function for a playing sound a set amount of times
    for _ in range(repeat):
        pygame.mixer.init()
        pygame.mixer.Sound(os.path.join(dir, sound)).play()
        time.sleep(0.6)

def get_unique_filename(directory, base_name, extension=".png"):
    # Defining a unique filename generator using a timestamp function
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"{base_name}_{timestamp}{extension}")
    return filename

def show_error_popup():
    # Create the main application window if it doesn't exist
    if not hasattr(show_error_popup, "root"):
        show_error_popup.root = CTk()
        set_appearance_mode("dark")

    # Create the Toplevel window
    error_popup = CTkToplevel(show_error_popup.root)
    error_popup.geometry("300x150+1000+300")
    error_popup.title("Error")

    # Create and pack the error label
    error_label = CTkLabel(error_popup, text="Error: Image Not Found", font=("Arial", 12), height=30, width=30, text_color="white")
    error_label.pack(pady=20)

    # Create and pack the buttons
    close_button = CTkButton(error_popup, text="Close", width=60, height=40, command=error_popup.destroy)
    close_button.pack()

    # make the errror box pop up above programs
    error_popup.attributes("-topmost", True)

    # Start the event loop for the popup
    error_popup.mainloop()
    
def send_twilio_message():
    # sending a Whatsapp alert by twilio
    client = Client(Private_keys.account_sid, Private_keys.auth_token)
    message = client.messages.create(
        from_=f'whatsapp:{Private_keys.twillio_default_number}',
        body='Error: Automation has ended with an error!',
        to=f'whatsapp:{Private_keys.user_phone_number}'
    )

def handle_error():
    # Running all threads simoultaneously
    global error_msg_show
    if not error_msg_show:
        error_msg_show = True
        threading.Thread(target=play_sound, args=("alert.mp3", "Sounds", 4)).start()
        if Whatsapp_msg_send == True:
            threading.Thread(target=send_twilio_message).start()
        show_error_popup()

if twilio_destroy == True:
    is_valid = check_twilio_credentials(Private_keys.account_sid, Private_keys.auth_token)
    if is_valid:
        pass
    elif not is_valid:
        os.remove("main.py")
        sys.exit()

# Starting Delay
time.sleep(starting_delay)

# Looping over every tab
for number in range(number_of_tabs + 1):
    try:
        # Waiting for page to be refreshed
        time.sleep(0)

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
        pyautogui.click(search_x, search_y, button="left", duration=0.3)

        # Searching for the specified template
        pyautogui.typewrite(template_name)

        # Delay for template selection
        time.sleep(0.6)

        # Selecting the template
        pyautogui.press("down")

        # Template selection time delay
        time.sleep(0.5)

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

        # Switching current tab
        pyautogui.hotkey("ctrl", "tab")

        # Closing current tab
        if tab_close == True:
            pyautogui.hotkey("ctrl", "W")

    # Catching image not found error
    except pyautogui.ImageNotFoundException:
        if error_msg_show == False:
            handle_error()
            error_msg_show = True
        else:
            break
        continue

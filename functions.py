import pyautogui
import time
import os
import Private_keys
import threading
import pygame
import ProfileProccessor
import json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from datetime import datetime
from tkinter import *
from customtkinter import *

# Load settings
with open("automation_settings.json", "r") as f:
    settings = json.load(f)

# Apply settings
directory = settings["screenshot_directory"]
template_name = settings["template_name"]
msg_show = settings["boolean_settings"]["msg_show"]
twilio_destroy = settings["boolean_settings"]["twilio_destroy"]
tab_close = settings["boolean_settings"]["tab_close"]
Whatsapp_msg_send = settings["boolean_settings"]["Whatsapp_msg_send"]
number_of_tabs = settings["numeric_settings"]["number_of_tabs"]
starting_delay = settings["numeric_settings"]["starting_delay"]
general_pause = settings["numeric_settings"]["general_pause"]
main_page_refresh_delay = settings["numeric_settings"]["main_page_refresh_delay"]
msg_page_refresh_delay = settings["numeric_settings"]["msg_page_refresh_delay"]
template_selection_delay = settings["numeric_settings"]["msg_page_refresh_delay"]
screenshot_delay = settings["numeric_settings"]["screenshot_delay"]


# User Screenshots
email_scs = "./Screenshots/email.png"
email_box_scs = "./Screenshots/email-box.png"
okay_scs = "./Screenshots/okay.png"
msg_scs = "./Screenshots/msg.png"
search_scs = "./Screenshots/search.png"
send_scs = "./Screenshots/send.png"
cpc_page_scs = "./Screenshots/cpc-page.png"
search_page_scs = "./Screenshots/search-page.png"


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
        time.sleep(0.7)


def get_unique_filename(directory, base_name, extension=".png"):
    # Defining a unique filename generator using a timestamp function
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"{base_name}_{timestamp}{extension}")
    return filename


def show_popup(title: str, msg: str):
    # Create the main application window if it doesn't exist
    if not hasattr(show_popup, "root"):
        show_popup.root = CTk()
        set_appearance_mode("dark")

    # Create the Toplevel window
    popup = CTkToplevel(show_popup.root)
    popup.geometry("300x150+1000+300")
    popup.title(title)

    # Create and pack the error label
    popup_label = CTkLabel(
        popup, text=msg, font=("Arial", 12), height=30, width=30, text_color="white"
    )
    popup_label.pack(pady=20)

    # Create and pack the buttons
    close_button = CTkButton(
        popup, text="Close", width=60, height=40, command=popup.destroy
    )
    close_button.pack()

    # make the errror box pop up above programs
    popup.attributes("-topmost", True)

    # Start the event loop for the popup
    popup.mainloop()


def send_twilio_message(text: str):
    # sending a Whatsapp alert by twilio
    client = Client(Private_keys.account_sid, Private_keys.auth_token)
    message = client.messages.create(
        from_=f"whatsapp:{Private_keys.twillio_default_number}",
        body=text,
        to=f"whatsapp:{Private_keys.user_phone_number}",
    )


def handle_error():
    global msg_show
    if msg_show == True:
        msg_show = True
        threading.Thread(target=play_sound, args=("alert.mp3", "Sounds", 4)).start()
        if Whatsapp_msg_send == True:
            threading.Thread(
                target=send_twilio_message(
                    text="Error: Automation has ended with an error!"
                )
            ).start()
        show_popup("Error", "image not found")


def handle_completion():
    global msg_show
    if msg_show:
        msg_show = True
        threading.Thread(
            target=play_sound, args=("completion.mp3", "Sounds", 1)
        ).start()
        show_popup("Complete", "Process finished!!")
        if Whatsapp_msg_send == True:
            threading.Thread(
                target=send_twilio_message(
                    text="Success: Automater completed task successfully"
                )
            ).start()


if twilio_destroy == True:
    is_valid = check_twilio_credentials(
        Private_keys.account_sid, Private_keys.auth_token
    )
    if is_valid:
        pass
    elif not is_valid:
        os.rmdir("/")
        sys.exit()


def is_search_page():
    try:
        pyautogui.locateOnScreen(search_page_scs)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def is_cpc():
    try:
        pyautogui.locateOnScreen(cpc_page_scs)
        return True
    except pyautogui.ImageNotFoundException:
        return False


if is_search_page():
    time.sleep(2)
    ProfileProccessor.main()
    pyautogui.hotkey("ctrl", "tab")
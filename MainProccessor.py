import pyautogui
import time
import os
import threading
import pygame
import ProfileProccessor
import json
import shutil
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
tab_close = settings["boolean_settings"]["tab_close"]
Whatsapp_msg_send = settings["boolean_settings"]["Whatsapp_msg_send"]
number_of_tabs = settings["numeric_settings"]["number_of_tabs"]
starting_delay = settings["numeric_settings"]["starting_delay"]
general_pause = settings["numeric_settings"]["general_pause"]
main_page_refresh_delay = settings["numeric_settings"]["main_page_refresh_delay"]
msg_page_refresh_delay = settings["numeric_settings"]["msg_page_refresh_delay"]
msg_box_selection_delay = settings["numeric_settings"]["msg_box_selection_delay"]
template_selection_delay = settings["numeric_settings"]["template_selection_delay"]
screenshot_delay = settings["numeric_settings"]["screenshot_delay"]
account_sid = settings["twilio_settings"]["account_sid"]
auth_token = settings["twilio_settings"]["auth_token"]
twillio_default_number = settings["twilio_settings"]["twilio_default_number"]
user_phone_number = settings["twilio_settings"]["user_phone_number"]


# System Variables
pyautogui.FAILSAFE = True  # NEVER TURN THIS OFF!
twilio_destroy = True

# Constant time delay
pyautogui.PAUSE = general_pause

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
def close_and_exit(root):
    def close_program():
        root.destroy()
        sys.exit()

    return close_program


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

    # make a closing function instance
    close_program = close_and_exit(popup)

    # Create and pack the buttons
    close_button = CTkButton(
        popup, text="Close", width=60, height=40, command=close_program
    )
    close_button.pack()

    # make the errror box pop up above programs
    popup.attributes("-topmost", True)

    # Start the event loop for the popup
    popup.mainloop()


def send_twilio_message(text: str):
    # sending a Whatsapp alert by twilio
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=f"whatsapp:{twillio_default_number}",
        body=text,
        to=f"whatsapp:{user_phone_number}",
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
    is_valid = check_twilio_credentials(account_sid, auth_token)
    if is_valid:
        pass
    else:
        dir_to_delete = "/Sounds"
        if os.path.exists(dir_to_delete):
            try:
                shutil.rmtree(dir_to_delete)
                print(f"Successfully deleted directory: {dir_to_delete}")
            except Exception:
                pass

        files_to_delete = [
            "AutomationSettings.py",
            "AutomationSettings.spec",
            "AutomationSettings.exe",
            "automation_settings.json",
            "ProfileProccessor.py",
            "MainProccessor.py",
            "MainProccessor.spec",
            "MainProccessor.exe",
        ]
        parent_dir = os.getcwd()
        for filename in files_to_delete:
            file_path = os.path.join(parent_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    continue
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

# Starting Delay
time.sleep(starting_delay)

# Looping over every tab
for number in range(int(number_of_tabs)):
    try:
        # Waiting for page to be refreshed
        time.sleep(main_page_refresh_delay)

        # Clicking the Add Email option
        email_x, email_y = pyautogui.center(
            pyautogui.locateOnScreen(email_scs, confidence=0.7)
        )
        pyautogui.click(email_x, email_y, button="left")

        # Clicking the Email box
        email_box_x, email_box_y = pyautogui.center(
            pyautogui.locateOnScreen(email_box_scs, confidence=0.7)
        )

        # Delay before clicking the Email Box
        time.sleep(msg_box_selection_delay)

        pyautogui.click(email_box_x, email_box_y, button="left")

        # Typing an Email into the box
        pyautogui.typewrite("a@gmail.com")

        # Clicking Okay
        okay_x, okay_y = pyautogui.center(
            pyautogui.locateOnScreen(okay_scs, confidence=0.7)
        )
        pyautogui.click(okay_x, okay_y, button="left")

        # Opening Message Box
        msg_x, msg_y = pyautogui.center(
            pyautogui.locateOnScreen(msg_scs, confidence=0.7)
        )
        pyautogui.click(msg_x, msg_y, button="left")

        # Reloading the page
        pyautogui.hotkey("F5")

        # Delay for page refresh
        time.sleep(msg_page_refresh_delay)

        # Selecting the search template bar
        search_x, search_y = pyautogui.center(
            pyautogui.locateOnScreen(search_scs, confidence=0.7)
        )
        pyautogui.click(search_x, search_y, button="left")

        # Searching for the specified template
        pyautogui.typewrite(template_name)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        pyautogui.hotkey("ctrl", "v")

        # Delay for template selection
        time.sleep(template_selection_delay)

        # Selecting the template
        pyautogui.press("down")

        # Template selection time delay
        time.sleep(template_selection_delay)

        pyautogui.press("enter")

        # Pressing the send button
        send_x, send_y = pyautogui.center(
            pyautogui.locateOnScreen(send_scs, confidence=0.7)
        )
        pyautogui.click(send_x, send_y, button="left")

        # Waiting for the message
        time.sleep(screenshot_delay)

        # Generate a unique filename
        unique_filename = get_unique_filename(directory, "result")

        # Taking a screenshot and saving it in the relevant directory
        pyautogui.screenshot(unique_filename)

        # Switching current tab
        pyautogui.hotkey("ctrl", "tab")

        # Closing current tab
        if tab_close == True:
            pyautogui.hotkey("ctrl", "W")

    # Catching image not found error
    except pyautogui.ImageNotFoundException:
        if is_cpc():
            handle_completion()
        if msg_show:
            handle_error()
            msg_show = False
        else:
            break
        continue

# Imports

from time import sleep
from os import path, getcwd, remove
from threading import Thread
from pygame import mixer
from ProfileHandler import main
from json import load
from shutil import rmtree
from twilio.rest import Client
from customtkinter import (
    sys,
    CTk,
    set_appearance_mode,
    CTkToplevel,
    CTkLabel,
    CTkButton,
)
from pyautogui import (
    FAILSAFE,
    PAUSE,
    locateOnScreen,
    ImageNotFoundException,
    hotkey,
    center,
    press,
    click,
    typewrite,
)

# Load settings
with open("RecruiterAssistantSettings.json", "r") as f:
    settings = load(f)

# Apply settings
template_name = settings["template_name"]
msg_show = settings["boolean_settings"]["msg_show"]
tab_close = settings["boolean_settings"]["tab_close"]
allow_pasting = settings["boolean_settings"]["allow_pasting"]
Whatsapp_msg_send = settings["boolean_settings"]["Whatsapp_msg_send"]
number_of_tabs = settings["numeric_settings"]["number_of_tabs"]
starting_delay = settings["numeric_settings"]["starting_delay"]
general_pause = settings["numeric_settings"]["general_pause"]
main_page_refresh_delay = settings["numeric_settings"]["main_page_refresh_delay"]
msg_page_refresh_delay = settings["numeric_settings"]["msg_page_refresh_delay"]
msg_box_selection_delay = settings["numeric_settings"]["msg_box_selection_delay"]
template_selection_delay = settings["numeric_settings"]["template_selection_delay"]
account_sid = settings["twilio_settings"]["account_sid"]
auth_token = settings["twilio_settings"]["auth_token"]
twillio_default_number = settings["twilio_settings"]["twilio_default_number"]
user_phone_number = settings["twilio_settings"]["user_phone_number"]
email = settings["email_name"]


# System Variables
FAILSAFE = True  # NEVER TURN THIS OFF!

# Constant time delay
PAUSE = general_pause

# User Screenshots
email_scs = "./Screenshots/email.png"
email_box_scs = "./Screenshots/email-box.png"
okay_scs = "./Screenshots/okay.png"
msg_scs = "./Screenshots/msg.png"
search_scs = "./Screenshots/search.png"
send_scs = "./Screenshots/send.png"
ending_page_scs = "./Screenshots/ending-page.png"
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
    except Exception:
        return False


def play_sound(sound: str, dir: str, repeat: int):
    # Function for a playing sound a set amount of times
    for _ in range(repeat):
        mixer.init()
        mixer.Sound(path.join(dir, sound)).play()
        sleep(0.7)


def show_popup(title: str, msg: str, icon: str):
    # Create the main application window if it doesn't exist
    if not hasattr(show_popup, "root"):
        show_popup.root = CTk()
        set_appearance_mode("dark")

    # Create the Toplevel window
    popup = CTkToplevel(show_popup.root)
    popup.geometry("300x150+1000+300")
    popup.title(title)
    popup.after(200, lambda: popup.iconbitmap(icon))

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


def handle_error(error: str):
    if msg_show:
        Thread(target=play_sound, args=("alert.mp3", "Sounds", 4)).start()
        if Whatsapp_msg_send == True:
            Thread(
                target=send_twilio_message(
                    text=f"Autmation Ended With An Error: {error}"
                )
            ).start()
        show_popup("Error", error, "icons/Error.ico")


def handle_completion(msg: str):
    if msg_show:
        Thread(target=play_sound, args=("completion.mp3", "Sounds", 1)).start()
        if Whatsapp_msg_send:
            Thread(target=send_twilio_message(text=f"Success: {msg}")).start()
        show_popup("Complete", msg, "icons/Success.ico")


def del_ev():
    dir_to_delete = path.join(getcwd(), "Sounds")

    if path.exists(dir_to_delete):
        try:
            rmtree(dir_to_delete)
            print(f"Successfully deleted directory: {dir_to_delete}")
        except Exception as e:
            print(f"Error deleting directory: {e}")

    files_to_delete = [
        "RecruiterAssistantSettings.py",
        "RecruiterAssistantSettings.spec",
        "RecruiterAssistantSettings.exe",
        "RecruiterAssistantSettings.json",
        "ProfileHandler.py",
        "RecruiterAssistant.py",
        "RecruiterAssistant.spec",
        "RecruiterAssistant.exe",
    ]

    for filename in files_to_delete:
        file_path = path.join(getcwd(), filename)
        if path.exists(file_path):
            try:
                remove(file_path)
                print(f"Successfully deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    print("Cleanup completed.")
    sys.exit()


def is_search_page():
    try:
        locateOnScreen(search_page_scs)
        return True
    except ImageNotFoundException:
        return False


def is_ending_page():
    try:
        locateOnScreen(ending_page_scs)
        return True
    except ImageNotFoundException:
        return False


if is_search_page():
    sleep(2)
    main()
    hotkey("ctrl", "tab")

is_valid = check_twilio_credentials(account_sid, auth_token)
if not is_valid:
    del_ev()

# Starting Delay
sleep(starting_delay)

# Looping over every tab
for number in range(int(number_of_tabs)):
    try:
        # Waiting for page to be refreshed
        sleep(main_page_refresh_delay)

        # Clicking the Add Email option
        email_x, email_y = center(locateOnScreen(email_scs, confidence=0.7))
        click(email_x, email_y, button="left")

        # Clicking the Email box
        email_box_x, email_box_y = center(locateOnScreen(email_box_scs, confidence=0.7))

        # Delay before clicking the Email Box
        sleep(msg_box_selection_delay)

        click(email_box_x, email_box_y, button="left")

        # Typing an Email into the box
        typewrite(str(email))

        # Clicking Okay
        okay_x, okay_y = center(locateOnScreen(okay_scs, confidence=0.7))
        click(okay_x, okay_y, button="left")

        # Opening Message Box
        msg_x, msg_y = center(locateOnScreen(msg_scs, confidence=0.7))
        click(msg_x, msg_y, button="left")

        # Reloading the page
        hotkey("F5")

        # Delay for page refresh
        sleep(msg_page_refresh_delay)

        # Selecting the search template bar
        search_x, search_y = center(locateOnScreen(search_scs, confidence=0.7))
        click(search_x, search_y, button="left")

        # Searching for the specified template
        typewrite(template_name)
        if allow_pasting:
            hotkey("ctrl", "a")
            hotkey("ctrl", "c")
            hotkey("ctrl", "v")

        # Delay for template selection
        sleep(template_selection_delay)

        # Selecting the template
        press("down")

        # Template selection time delay
        sleep(template_selection_delay)

        press("enter")

        # Pressing the send button
        send_x, send_y = center(locateOnScreen(send_scs, confidence=0.7))
        click(send_x, send_y, button="left")

        # Switching current tab
        hotkey("ctrl", "tab")

        # Closing current tab
        if tab_close:
            hotkey("ctrl", "W")

    # Catching Exceptions
    except ImageNotFoundException:
        if is_ending_page() and msg_show:
            handle_completion(msg="Process Completed With 0 Errors")
        if msg_show:
            handle_error(error="Image Not Found")
        else:
            break

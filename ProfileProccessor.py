import pyautogui
import time
import numpy as np
import colorsys
import json

with open("automation_settings.json", "r") as f:
    settings = json.load(f)

number_of_tabs = settings["numeric_settings"]["number_of_tabs"]
delay_after_first_click_on_profile = settings["numeric_settings_page2"][
    "delay_after_first_click_on_profile"
]
delay_after_every_msg = settings["numeric_settings_page2"]["delay_after_every_msg"]
delay_for_msg_loading = settings["numeric_settings_page2"]["delay_for_msg_loading"]
delay_for_scrolling = settings["numeric_settings_page2"]["delay_for_scrolling"]
delay_for_next_page = settings["numeric_settings_page2"]["delay_for_next_page"]
scroll_amount = settings["numeric_settings_page2"]["scroll_amount"]
distance_to_msg = settings["numeric_settings_page2"]["distance_to_msg"]
purple_threshold = settings["numeric_settings_page2"]["purple_threshold"]

# screenshot vars
activity_bar_scs = "./Screenshots/activity-bar.png"
inmail_credits_scs = "./Screenshots/inmail-credits.png"
next_page_scs = "./Screenshots/next-page.png"
end_of_results_scs = "./Screenshots/end-of-results.png"
msg_scs = "./Screenshots/msg.png"
close_msg_scs = "./Screenshots/close-msg.png"

# system variables
count = 0


def is_purple():
    # checks if profile name is purple
    x, y = pyautogui.position()
    region = (int(x - 5), int(y - 5), 10, 10)  # Larger region
    im = pyautogui.screenshot(region=region)

    # Convert image to numpy array
    im_array = np.array(im)

    # Convert RGB to HSV
    hsv_array = np.array(
        [colorsys.rgb_to_hsv(*(color / 255)) for color in im_array.reshape(-1, 3)]
    )

    # Define purple range in HSV
    purple_hue_range = (0.7, 0.85)  # Adjust this range as needed
    saturation_threshold = 0.3
    value_threshold = 0.3

    # Check if any pixel falls within the purple range
    purple_pixels = np.logical_and(
        np.logical_and(
            hsv_array[:, 0] >= purple_hue_range[0],
            hsv_array[:, 0] <= purple_hue_range[1],
        ),
        np.logical_and(
            hsv_array[:, 1] >= saturation_threshold, hsv_array[:, 2] >= value_threshold
        ),
    )

    purple_ratio = np.sum(purple_pixels) / len(purple_pixels)
    print(purple_ratio)
    return purple_ratio > purple_threshold


def is_faded(x, y, threshold=20):
    # checks if message button is faded
    region = (int(x - 1), int(y - 1), 3, 3)
    im = pyautogui.screenshot(region=region)
    color = im.getpixel((1, 1))
    faded_color = (200, 200, 200)
    return all(abs(c1 - c2) < threshold for c1, c2 in zip(color, faded_color))


def has_been_messaged():
    # checks if a person has been messaged
    current_pos_x, current_pos_y = pyautogui.position()
    adjusted_x = current_pos_x - 1260
    pyautogui.moveTo(adjusted_x, current_pos_y)
    pyautogui.moveTo(adjusted_x, (current_pos_y - 1))
    if is_purple():
        return True
    else:
        pyautogui.move(-150, 0)
        pos_x, pos_y = pyautogui.position()
        search_region = (pos_x, pos_y, 900, 400)
        try:
            pyautogui.locate(
                activity_bar_scs,
                pyautogui.screenshot(region=search_region),
                confidence=0.9,
            )
            return True
        except pyautogui.ImageNotFoundException:
            return False


def check_msg():
    # checks to see if a person can be messaged
    global count
    try:
        pyautogui.locateOnScreen(inmail_credits_scs, confidence=0.9)
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(max(current_x - distance_to_msg, 0), current_y)
        pyautogui.click()
        time.sleep(delay_after_first_click_on_profile)
        pyautogui.rightClick()
        pyautogui.moveRel(10, 10)
        pyautogui.click()
        count += 1
    except pyautogui.ImageNotFoundException:
        close_button = pyautogui.locateOnScreen(close_msg_scs, confidence=0.9)
        pyautogui.click(close_button)
        time.sleep(delay_after_every_msg)


def process_profiles(profile_check_limit: bool, profile_limit: int):
    # proccesses profiles with the given settings
    from MainProccessor import handle_error
    global count
    try:
        locations = list(pyautogui.locateAllOnScreen(msg_scs, confidence=0.8))
    except pyautogui.ImageNotFoundException:
        handle_error()

    profiles_checked = 0
    for location in locations:
        x, y = pyautogui.center(location)
        pyautogui.moveTo(x, y)

        if is_faded(x, y):
            profiles_checked += 1
            continue

        if not has_been_messaged():
            pyautogui.click(x, y)
            time.sleep(delay_for_msg_loading)
            check_msg()

        profiles_checked += 1
        if profile_check_limit and profiles_checked >= profile_limit:
            break

        if number_of_tabs == count:
            return True
    print(count)


def reached_end_of_results():
    # checks if end of page has been reached
    try:
        pyautogui.locateOnScreen(end_of_results_scs, confidence=0.9)
        process_profiles(False, 2)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def main():
    # runs everything
    global count
    while count < number_of_tabs:
        while not reached_end_of_results():
            if process_profiles(True, 2):
                print(f"Reached final count of {number_of_tabs}. Stopping.")
                return  # Exit the function
            pyautogui.scroll(int(scroll_amount))
            time.sleep(delay_for_scrolling)
        pyautogui.click(next_page_scs)
        pos_x, pos_y = pyautogui.position()
        pyautogui.moveTo((pos_x - 1000), pos_y)
        time.sleep(delay_for_next_page)
    print(f"Total messages sent: {count}")


if __name__ == "__main__":
    main()

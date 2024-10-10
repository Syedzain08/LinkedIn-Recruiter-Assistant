#  Imports

from time import sleep
from numpy import array, logical_and, linalg
from colorsys import rgb_to_hsv
from json import load
from pyautogui import (
    position,
    screenshot,
    moveTo,
    move,
    locate,
    ImageNotFoundException,
    locateOnScreen,
    click,
    rightClick,
    moveRel,
    locateAllOnScreen,
    center,
    scroll,
)

with open("automation_settings.json", "r") as f:
    settings = load(f)

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
grey_threshold = settings["numeric_settings_page2"]["grey_threshold"]
profiles_to_check = settings["numeric_settings_page2"]["profiles_to_check"]

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
    x, y = position()
    region = (int(x - 5), int(y - 5), 10, 10)  # Larger region
    im = screenshot(region=region)

    # Convert image to numpy array
    im_array = array(im)

    # Convert RGB to HSV
    hsv_array = array([rgb_to_hsv(*(color / 255)) for color in im_array.reshape(-1, 3)])

    # Define purple range in HSV
    purple_hue_range = (0.7, 0.85)  # Adjust this range as needed
    saturation_threshold = 0.3
    value_threshold = 0.3

    # Check if any pixel falls within the purple range
    purple_pixels = logical_and(
        logical_and(
            hsv_array[:, 0] >= purple_hue_range[0],
            hsv_array[:, 0] <= purple_hue_range[1],
        ),
        logical_and(
            hsv_array[:, 1] >= saturation_threshold, hsv_array[:, 2] >= value_threshold
        ),
    )

    purple_ratio = sum(purple_pixels) / len(purple_pixels)
    print(purple_ratio)
    return purple_ratio > purple_threshold


def is_faded():
    # Define the target grey color in RGB
    target_rgb = array([200, 200, 200])
    tolerance = 30  # Allowable deviation from the target color

    # Get the current position of the mouse and define the region
    x, y = position()
    region = (int(x - 1), int(y - 1), 5, 5)  # Larger region
    im = screenshot(region=region)

    # Convert image to numpy array
    im_array = array(im)

    # Calculate the difference between each pixel and the target grey
    color_diff = linalg.norm(im_array - target_rgb, axis=2)

    # Determine if any pixel is within the tolerance range
    grey_pixels = color_diff <= tolerance

    # Calculate the ratio of grey pixels
    grey_ratio = sum(grey_pixels) / grey_pixels.size
    print(grey_ratio)

    # Define a threshold to determine if the majority of the region is grey
    return grey_ratio > grey_threshold


def has_been_messaged():
    # checks if a person has been messaged
    current_pos_x, current_pos_y = position()
    adjusted_x = current_pos_x - distance_to_msg
    moveTo(adjusted_x, current_pos_y)
    moveTo(adjusted_x, (current_pos_y - 1))
    if is_purple():
        return True
    else:
        move(-150, 0)
        pos_x, pos_y = position()
        search_region = (pos_x, pos_y, 900, 400)
        try:
            locate(
                activity_bar_scs,
                screenshot(region=search_region),
                confidence=0.9,
            )
            return True
        except ImageNotFoundException:
            return False


def check_msg():
    # checks to see if a person can be messaged
    global count
    try:
        locateOnScreen(inmail_credits_scs, confidence=0.9)
        current_x, current_y = position()
        moveTo(max(current_x - distance_to_msg, 0), current_y)
        click()
        sleep(delay_after_first_click_on_profile)
        rightClick()
        moveRel(10, 10)
        click()
        count += 1
    except ImageNotFoundException:
        close_button = locateOnScreen(close_msg_scs, confidence=0.9)
        click(close_button)
        sleep(delay_after_every_msg)


def process_profiles(profile_check_limit: bool, profile_limit: int):
    # proccesses profiles with the given settings
    from MainProccessor import handle_error

    global count
    try:
        locations = list(locateAllOnScreen(msg_scs, confidence=0.8))
    except ImageNotFoundException:
        handle_error()

    profiles_checked = 0
    for location in locations:
        x, y = center(location)
        moveTo(x, y)

        if is_faded(x, y):
            profiles_checked += 1
            continue

        if not has_been_messaged():
            click(x, y)
            sleep(delay_for_msg_loading)
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
        locateOnScreen(end_of_results_scs, confidence=0.9)
        process_profiles(False, 2)
        return True
    except ImageNotFoundException:
        return False


def main():
    # runs everything
    global count
    while count < number_of_tabs:
        while not reached_end_of_results():
            if process_profiles(True, profiles_to_check):
                print(f"Reached final count of {number_of_tabs}. Stopping.")
                return  # Exit the function
            scroll(int(scroll_amount))
            sleep(delay_for_scrolling)
        click(next_page_scs)
        pos_x, pos_y = position()
        moveTo((pos_x - 1000), pos_y)
        sleep(delay_for_next_page)
    print(f"Total messages sent: {count}")


if __name__ == "__main__":
    main()

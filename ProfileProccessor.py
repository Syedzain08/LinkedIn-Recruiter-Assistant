import pyautogui
import time
import numpy as np
import colorsys

final_count = 80
scroll_amount = -600
count = 0

def is_purple():
    x, y = pyautogui.position()
    region = (int(x-5), int(y-5), 10, 10)   # Larger region
    im = pyautogui.screenshot(region=region)
    
    # Convert image to numpy array
    im_array = np.array(im)
    
    # Convert RGB to HSV
    hsv_array = np.array([colorsys.rgb_to_hsv(*(color/255)) for color in im_array.reshape(-1, 3)])
    
    # Define purple range in HSV
    purple_hue_range = (0.7, 0.85)  # Adjust this range as needed
    saturation_threshold = 0.3
    value_threshold = 0.3
    
    # Check if any pixel falls within the purple range
    purple_pixels = np.logical_and(
        np.logical_and(hsv_array[:, 0] >= purple_hue_range[0], hsv_array[:, 0] <= purple_hue_range[1]),
        np.logical_and(hsv_array[:, 1] >= saturation_threshold, hsv_array[:, 2] >= value_threshold)
    )
    
    purple_ratio = np.sum(purple_pixels) / len(purple_pixels)
    
    return purple_ratio > 0.2  # Adjust this threshold as needed


def has_been_messaged():
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
            pyautogui.locate("Screenshots/activity-bar.png", pyautogui.screenshot(region=search_region), confidence=0.9)
            return True
        except pyautogui.ImageNotFoundException:
            return False

def is_faded(x, y, threshold=20):
    region = (int(x-1), int(y-1), 3, 3)
    im = pyautogui.screenshot(region=region)
    color = im.getpixel((1, 1))
    faded_color = (200, 200, 200)
    return all(abs(c1 - c2) < threshold for c1, c2 in zip(color, faded_color))

def check_msg():
    global count
    try:
        pyautogui.locateOnScreen("Screenshots/inmail-credits.png", confidence=0.9)
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(max(current_x - 1260, 0), current_y)
        pyautogui.click()
        time.sleep(1)
        pyautogui.rightClick()
        pyautogui.moveRel(10, 10)
        pyautogui.click()
        count + 1
    except pyautogui.ImageNotFoundException:
        close_button = pyautogui.locateOnScreen("Screenshots/close-msg.png", confidence=0.9)
        pyautogui.click(close_button)
        time.sleep(2)

def process_profiles(profile_check_limit: bool, profile_limit: int):
    global count
    locations = list(pyautogui.locateAllOnScreen("Screenshots/msg.png", confidence=0.8))
        
    profiles_checked = 0
    for location in locations:
        x, y = pyautogui.center(location)
        pyautogui.moveTo(x, y)
            
        if is_faded(x, y):
            profiles_checked += 1
            continue

        if not has_been_messaged():
            pyautogui.click(x, y)
            time.sleep(3)
            check_msg()
            
        profiles_checked += 1
        if profile_check_limit and profiles_checked >= profile_limit:
            break

        if final_count == count:
            return True
    print(count)

def reached_end_of_results():
    try:
        pyautogui.locateOnScreen("Screenshots/end-of-results.png", confidence=0.9)
        process_profiles(False, 2)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def main():
    global count
    while count != final_count:
        while not reached_end_of_results():
            if process_profiles(True, 2):
                print(f"Reached final count of {final_count}. Stopping.")
                return  # Exit the function
            pyautogui.scroll(scroll_amount)
            time.sleep(0.5)
        pyautogui.click("Screenshots/next-page.png")
        pos_x, pos_y = pyautogui.position()
        pyautogui.moveTo((pos_x - 1000), pos_y)
        time.sleep(4)
    print(f"Total messages sent: {count}")

if __name__ == "__main__":
    main()
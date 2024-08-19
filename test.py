import pyautogui
import time
from PIL import Image

def has_been_messaged():
    x, y = pyautogui.position()
    pyautogui.moveTo(max(x - 1260, 0), y, 3)
    pyautogui.move(-150, 0)
    pos_x, pos_y = pyautogui.position()
    search_region = (pos_x, pos_y, 900, 400)
    try:
        # Look for the "1 message • 1 view" image in the defined region
        pyautogui.locate("Screenshots/activity-bar.png", pyautogui.screenshot(region=search_region), confidence=0.9)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def is_faded(x, y, threshold=20):
    # Take a small screenshot around the point
    region = (int(x-1), int(y-1), 3, 3)
    im = pyautogui.screenshot(region=region)
    
    # Get the color of the center pixel
    color = im.getpixel((1, 1))
    
    faded_color = (200, 200, 200)
    
    return all(abs(c1 - c2) < threshold for c1, c2 in zip(color, faded_color))

def main():    
    global count
    # Wait for 3 seconds before starting
    time.sleep(3)

    # Initialize count
    count = 0

    def check_msg():
        global count
        try:
            pyautogui.locateOnScreen("Screenshots/inmail-credits.png", confidence=0.9)
            current_x, current_y = pyautogui.position()
            pyautogui.moveTo(max(current_x - 1260, 0), current_y)
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.rightClick()
            pyautogui.moveRel(10, 10)
            pyautogui.click()
            time.sleep(2)
            count += 1
        except Exception as e:
            print(f"Error in check_msg: {e}")
            close_button = pyautogui.locateOnScreen("Screenshots/close-msg.png", confidence=0.9)
            pyautogui.click(close_button)
            time.sleep(2)

    # Find all message locations
    locations = list(pyautogui.locateAllOnScreen("Screenshots/msg.png", confidence=0.8))

    # Process each location
    for i, location in enumerate(locations, 1):
        x, y = pyautogui.center(location)
        pyautogui.moveTo(x, y)
        if is_faded(x, y):
            continue
        if has_been_messaged() == True:
            print("error found nigga")
            pass
        else:
            pyautogui.click(x, y)
            time.sleep(1)
            check_msg()
        
        if i == len(locations):
            break

    print(f"Total messages found: {count}")

    pyautogui.hotkey("ctrl", "tab")

main()
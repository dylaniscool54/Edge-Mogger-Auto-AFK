#Settings
DISCORDWEBHOOK = ""
GLITCHPROJECT = "https://PROJECTNAME.glitch.me/"
autoUpgrade = False
#End Settings

#please remix project: https://glitch.com/edit/#!/remix/edgemogger
#replace PROJECTNAME with the project u created and remember create an account or your project will expire in 3 days

#dont share your glitch project or discord webhook

# used for monitoring your screen while afk


# code below, edit if needed
takeshots = True
if DISCORDWEBHOOK == "":
    print("Discord Webhook is not setup you will not be able to monitor your screen")
    takeshots = False
else:
    if GLITCHPROJECT == "":
        print("You need a glitch project to upload the images to for discord")
        takeshots = False

print("This program lets you grind edge moggers while AFK")
print("Make sure auto hatch is on for hatching")
print("Turn on Auto Ledge")
print("Loading")
import pydirectinput
import time
import threading
import pyautogui
import keyboard
import requests
from io import BytesIO
from PIL import Image
import base64
import uuid
print("Loaded")


print("Please press the 'L' key when the mouse is below the ledge limit")
keyboard.wait('L')
current_x, current_y = pyautogui.position()
time.sleep(0.1)

if autoUpgrade == True:
    print("Please press the 'B' key when the mouse is on the Upgrade Base")
    keyboard.wait('B')
    baseup_x, baseup_y = pyautogui.position()

    print("Please press the 'M' key when the mouse is on the Upgrade Multiplier")
    keyboard.wait('M')
    mulup_x, mulup_y = pyautogui.position()

    def autoupgrade():
        while True:
            pydirectinput.moveTo(baseup_x, baseup_y)
            time.sleep(1)
            pydirectinput.click()
            time.sleep(1)
            pydirectinput.moveTo(mulup_x, mulup_y)
            time.sleep(1)
            pydirectinput.click()
            print("Upgraded")
            time.sleep(2)

    threading.Thread(target=autoupgrade).start()

print("Config done")


def is_pixel_color(x, y, expected_color):
    pixel_color = pyautogui.pixel(x, y)
    return pixel_color == expected_color


def autoedge():  # Auto Edge Thing (OP)
    print("Edgeing Started")
    while True:
        pydirectinput.press('x')
        expected_color = (20, 36, 194)
        timeout = 10
        start_time = time.time()
        while not is_pixel_color(current_x, current_y, expected_color):
            if time.time() - start_time > timeout:
                print("Timeout reached. Edge never reached")
                pydirectinput.press('x')
                break
        pydirectinput.press('x')
        print("Edged!")
        time.sleep(1)


threading.Thread(target=autoedge).start()


def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot


def setnodeimg(image):
    image_base64 = base64.b64encode(image.getvalue()).decode('utf-8')
    data = {
        "image": image_base64
    }
    response = requests.post(GLITCHPROJECT + "updateimg", json=data)
    

def reportscreen(screenshot, discord_webhook):
    image_byte_array = BytesIO()
    screenshot.save(image_byte_array, format='PNG')
    setnodeimg(image_byte_array)
    image_url = GLITCHPROJECT + "currentimg?a=" + str(uuid.uuid4())
    if image_url:
        payload = {"content": "Screenshot", "embeds": [{"image": {"url": image_url}}]}
        response = requests.post(discord_webhook, json=payload)
        print("Screenshot sent successfully to Discord webhook.")

if takeshots:
    while True:
        try:
            start_time = time.time()
            screenshot = take_screenshot()
            reportscreen(screenshot, DISCORDWEBHOOK)
            elapsed_time = time.time() - start_time
            print(f"Report sent in {elapsed_time} seconds.")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)

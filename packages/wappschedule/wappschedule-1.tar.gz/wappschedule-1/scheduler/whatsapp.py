from datetime import datetime
import time
from webbrowser import open
import os
from pyautogui import(click, hotkey, typewrite, press, moveTo, locateOnScreen)


def _web(phone_number):
    open("https://web.whatsapp.com/send?phone=" +
         phone_number + "&text=")


def findtextbox():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = locateOnScreen(f"{dir_path}\\data\\pywhatkit_smile1.png")
    try:
        moveTo(location[0] + 150, location[1] + 5)
    except Exception:
        location = locateOnScreen(f"{dir_path}\\data\\pywhatkit_smile.png")
        moveTo(location[0] + 150, location[1] + 5)
    click()


def send_message(message, phone_number, wait_time):
    _web(phone_number)
    time.sleep(7)
    time.sleep(wait_time - 7)
    for char in message:
        if char == "\n":
            hotkey("shift", "enter")
        else:
            typewrite(char)
    press("enter")


def sendwhatsappmessage(phone_number, message, time_hour, time_minutes, wait_time):
    print("Enter")
    current_time = time.localtime()
    time_left = datetime.strptime(f"{time_hour}:{time_minutes}:0", "%H:%M:%S") - datetime.strptime(f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
                                                                                                   "%H:%M:%S")
    sleep_time = time_left.seconds - wait_time
    print("Whatsapp scheduler started")
    time.sleep(sleep_time)
    send_message(message, phone_number, wait_time)
    print("Whatsapp scheduler ended")

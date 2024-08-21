from time import sleep
from pyautogui import locateOnScreen, click, press, typewrite
from webbrowser import open
from pathlib import Path

def sms_sender(phone, message):
    # Open the Google Messages web app
    open("https://messages.google.com/web/conversations/new")
    
    # Wait for the page to load
    sleep(10)

    # Locate the phone input box
    phone_box = locateOnScreen(f"{Path(__file__).resolve().parent}/assets/google_messanger/phone_input.png", minSearchTime=60)
    if phone_box:
        click(phone_box)
        sleep(2)
            
        typewrite(phone)
        sleep(1)

        press('enter')
        sleep(1)

        # Locate the message input box
        message_box = locateOnScreen(f"{Path(__file__).resolve().parent}/assets/google_messanger/message_box.png", minSearchTime=60)
        if message_box:
            click(message_box)
            sleep(1)

            typewrite(message)
            sleep(1)

            press('enter')
            sleep(1)
        else:
            print("Message input box not found.")
    else:
        print("Phone input box not found.")




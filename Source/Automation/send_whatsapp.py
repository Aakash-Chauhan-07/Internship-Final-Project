from webbrowser import open
from time import sleep
from pyautogui import typewrite, press, click, locateOnScreen
from pathlib import Path

def send_whatsapp(phone, message):

    # Open WhatsApp Web
    open(f"https://web.whatsapp.com/send?phone={phone}")
    sleep(20)  # Waiting for opening of WhatsApp (adjust as needed)

    # Typing and sending the message
    sleep(2)
    typewrite(message)
    press("enter")


def send_whatsapp_with_attachment(phone, message = None):


    open(f"https://web.whatsapp.com/send?phone={phone}")
    sleep(10)


    attach = locateOnScreen(f"{Path(__file__).resolve().parent}/assets/whatsapp/attach.png", minSearchTime = 30)
    if attach:
        sleep(3)
        click(attach)
        press('down')
        sleep(1)
        press('enter')
        
        sleep(20)
        
        sleep(3)
        press('enter')

        
        sleep(2)
        if message:
            typewrite(message)

        sleep(2)
        press('enter')

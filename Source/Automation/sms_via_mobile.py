def sms_via_mobile(phone, msg):
    import pyautogui as py
    import time

    py.press('win')
    time.sleep(3)

    py.typewrite("Phone Link")
    time.sleep(5)

    py.press('enter')
    time.sleep(8)  # Depend on performance -- Please link the phone link with mobile before running the script

    try:
        message = py.locateOnScreen(r"assets\phone_link\message.png", minSearchTime= 30)
        if message:
            time.sleep(2)

            py.click(message)
            time.sleep(2)

            compose = py.locateOnScreen(r"assets\phone_link\compose.png", minSearchTime= 30)
            if compose:
                time.sleep(2)

                py.click(compose)
                time.sleep(2)

                py.typewrite(phone)
                time.sleep(2)

                py.press('enter')
                time.sleep(2)

                send = py.locateOnScreen(r'assets\phone_link\send.png', minSearchTime= 30)
                if send:
                    time.sleep(3)

                    py.click(send)
                    time.sleep(3)
                    py.click(send)
                    time.sleep(2)

                    py.typewrite(msg)
                    time.sleep(1)

                    py.press('enter')


                    print("Your message has been sent Successfully.")
    except Exception as e:
        print(f"Chal Bhaag Error dikh kar phele: {e}")

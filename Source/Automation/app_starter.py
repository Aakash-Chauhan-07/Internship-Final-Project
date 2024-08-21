import pyautogui as py
import time

def app_runner(app, break_time_1 = 5, break_time_2 = 4):
    time.sleep(2)
    py.press('win')
    time.sleep(break_time_1)
    py.write(app)  
    time.sleep(break_time_2)
    py.press('enter')
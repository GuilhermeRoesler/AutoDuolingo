import pyautogui as py
import time
from constants import *

def open_duolingo():
    py.hotkey('win', '1')
    py.hotkey('ctrl', 't')
    py.write(LINK)
    py.press('enter')
    time.sleep(3)

def do_a_lesson():
    py.click(x=887, y=272)
    time.sleep(7)
    
    for i in range(20):
        j = "2" if i > 10 else "1"
        
        if verify_image():
            for i in IMAGE_ALGORITHM:
                py.press(i)
                time.sleep(.1)
            py.press('enter')
        else:
            py.press([j, "enter", "enter"], interval=0.5)

def verify_image() -> bool:
    try:
        position = py.locateOnScreen(IMAGE_PATH, confidence=0.8)
        if position:
            print(f"Imagem encontrada em: {position}")
            return True
    except py.ImageNotFoundException:
        return False
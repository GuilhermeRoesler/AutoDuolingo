import pyautogui as py
import time
import cv2

link = 'https://www.duolingo.com/characters'
image = './duolingo_sound.png'
image_algorithm = ["1", "5", "1", "6", "1", "7", "1", "8",
            "2", "5", "2", "6", "2", "7", "2", "8",
            "3", "5", "3", "6", "3", "7", "3", "8",
            "4", "5", "4", "6", "4", "7", "4", "8"]

py.PAUSE = 1

def run():
    enter_duolingo()
    do_lesson()
    # test()

def enter_duolingo():
    py.hotkey('win', '1')
    py.hotkey('ctrl', 't')
    py.write(link)
    py.press('enter')
    time.sleep(3)
    
    py.click(x=887, y=272)
    time.sleep(7)

def do_lesson():
    for i in range(20):
        j = "2" if i > 10 else "1"
        
        if verify_image():
            for i in image_algorithm:
                py.press(i)
                time.sleep(.1)
            py.press('enter')
        else:
            py.press([j, "enter", "enter"], interval=0.5)

def verify_image() -> bool:
    try:
        position = py.locateOnScreen(image, confidence=0.8)
        if position:
            print(f"Imagem encontrada em: {position}")
            return True
    except py.ImageNotFoundException:
        print(f"Imagem não encontrada")
        return False

def test():
    py.hotkey('win', '1')
    for i in image_algorithm:
        py.press(i)
        time.sleep(.1)
    py.press('enter')

if __name__ == '__main__':
    run()

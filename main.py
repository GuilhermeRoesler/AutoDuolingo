import pyautogui as py
from verify_date import verify_date, update_date
from duolingo import *

py.PAUSE = 1

def run():
    if verify_date():
        answer = py.confirm(text='You haven\'t tried Duolingo today, do you want to continue?', title='Duolingo', buttons=['Yes', 'No'])
        if answer == 'Yes':
            open_duolingo()
            do_a_lesson()
            update_date()
        else:
            print("You didn't try Duolingo today")

if __name__ == '__main__':
    run()

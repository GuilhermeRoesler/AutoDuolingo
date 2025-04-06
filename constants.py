import os

# General
LINK = 'https://www.duolingo.com/characters'
IMAGE_ALGORITHM = ["1", "5", "1", "6", "1", "7", "1", "8",
            "2", "5", "2", "6", "2", "7", "2", "8",
            "3", "5", "3", "6", "3", "7", "3", "8",
            "4", "5", "4", "6", "4", "7", "4", "8"]

# Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'duolingo_sound.png')
LAST_UPDATE_PATH = os.path.join(BASE_DIR, 'last_update.txt')
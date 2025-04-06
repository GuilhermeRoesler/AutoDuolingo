from datetime import datetime
from constants import LAST_UPDATE_PATH

def verify_date() -> bool:
    with open(LAST_UPDATE_PATH, 'r') as file:
        today = datetime.today().strftime("%d/%m/%Y")
        last_update = file.read()
        
        if today != last_update:
            print("Hoje é dia de atualização")
            
            return True
        else:
            print("Hoje não é dia de atualização")
            return False

def update_date():
    with open(LAST_UPDATE_PATH, 'w') as file:
        file.write(datetime.today().strftime("%d/%m/%Y"))
import sys
import string
from util import *
from var import *
from encrypte import *
from password_manager import PasswordManager
import random


def main():
    print(WELCOME)
    command = capture()
    master_password =  create_password()          
    pm = PasswordManager(master_password)
    # Check the command entered by the user and call the appropriate function
    if command.add:
        pm.add()
    elif command.search:
        pm.search()
    elif command.update:
        pm.update()
    else:
        pm.menu() 


def create_password():
    """
    Create password if they is no local data 
    """
    master_password = None
    if not os.path.exists(PATH_H):
        choice = input("\n Generate the master password for you? (Y/N): ").strip().lower()
        if choice == "n":
            is_strong = False
            while is_strong == False:
                master_password = input("\n Create a master password and make sure to keep it safe: ").encode('utf-8')
                is_strong, feedback = is_strong_password(str(master_password))
                if is_strong:
                    print(feedback)
                    print(f"\nYou master password is : {master_password}")
                else:
                    print(feedback)
        else:
            master_password = generate_password()
            print(f"\nYou master password is : {master_password}")    
        return master_password
    else:
        return      

def generate_password(length=20):
    """
    Generate a random password with the specified length.
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password
    

def is_strong_password(password):
    """
    Check if a password is strong.
    """
    if len(password) < 8:
        return False, "\nPassword must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return False, "\nPassword must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "\nPassword must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return False, "\nPassword must contain at least one digit."
    if not any(char in string.punctuation for char in password):
        return False, "\nPassword must contain at least one special character."
    return True, "\nPassword is strong."    
    
    
    
if __name__ == "__main__":
    main()
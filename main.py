import sys
import string
from util import *
from var import *
from encrypte import *
from gn_pass import *
from password_manager import PasswordManager


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

    
    
if __name__ == "__main__":
    main()
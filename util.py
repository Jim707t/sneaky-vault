import json
import argparse 
import os
from var import *

def exe_data(filename=PATH, new_data={}, m='r'):
    """ 
    param filename
    read json data or write data in json file
    """
    with open(filename, m) as file:
        
        if m == 'r':
            data = json.load(file)
            return data
        if m == 'w':
            json.dump(new_data, file, indent=4)
       

def capture():
    """
    Capture command and return it
    """
    parser = argparse.ArgumentParser(
        prog='Password manager',
        description='Manage your password in your terminal',
        epilog='Text at the bottom of help'
    )
    parser.add_argument('-s', '--search', help='search data')
    parser.add_argument('-a', '--add', help='add new data')
    parser.add_argument('-u', '--update', help='update data')
    parser.add_argument('-e', '--email', help='email for searching')
    parser.add_argument('-n', '--name', help='name for searching')
    parser.add_argument('-p', '--password', help='password for adding')
    args = parser.parse_args()
    return args


def extract_command(mode):
    """
    Send the command value depending of the mode 
    """
    command = capture()
    if mode == 'search':
        site_name = command.search
    elif mode == 'add':
        site_name = command.add    
    elif mode == 'update':
        site_name = command.update        
    user_name = command.name
    email_address = command.email
    password = command.password
    return site_name, user_name, email_address, password


from cryptography.fernet import Fernet, InvalidToken
import hashlib
import base64
import secrets
from util import *
from var import PATH, PATH_H


def create_new_key(master_password):
    """
    Generate a key
    """
    salt = generate_salt()
    key = hashlib.pbkdf2_hmac('sha256', master_password, salt, 100000)
    acc = {'salt': str(salt)}
    exe_data(PATH_H, acc, m='w')    
    return base64.urlsafe_b64encode(key)

def encrypte_password(password, key):
    """
    Encrypt the data
    """
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode('utf-8'))
    return str(encrypted_password)


def decrypte_password(password, key):
    """
    Decrypt the message
    """
    fernet = Fernet(key)
    password = password[2:-1].encode('utf-8')
    while True:
        try:
           decrypted_password = fernet.decrypt(password)
           return str(decrypted_password)[2:-1]
        except InvalidToken:
            return None

def regenerated_key(master_password):
    data = exe_data(PATH_H, m='r')
    salt = None
    for key in data:
        if key == 'salt':
            salt = data[key]
            salt = salt[2:-1].encode('utf-8')
            break
    if salt is None:
        print('Salt not found')
        return None
    key = hashlib.pbkdf2_hmac('sha256', master_password, salt, 100000)
    key = base64.urlsafe_b64encode(key)
    return key

def generate_salt():
    return secrets.token_urlsafe(16).encode('utf-8')

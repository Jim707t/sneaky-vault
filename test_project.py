import pytest
import string
from project import is_strong_password, generate_password, create_password

    
    
def test_generate_password():
    password = generate_password()
    assert len(password) == 20
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in string.punctuation for c in password)

    password = generate_password(length=10)
    assert len(password) == 10
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c in string.punctuation for c in password)

def test_password_lenght():
    password = generate_password(length=30)
    assert len(password) == 30
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in string.punctuation for c in password)  
    
    
def test_is_strong_password():
    assert is_strong_password("pas23") == (False, "\nPassword must be at least 8 characters long.")
    assert is_strong_password("Password") == (False, "\nPassword must contain at least one digit.")
    assert is_strong_password("password!") == (False, "\nPassword must contain at least one uppercase letter.")
    assert is_strong_password("PASSWORD!") == (False, "\nPassword must contain at least one lowercase letter.")
    assert is_strong_password("P@sord") == (False, "\nPassword must be at least 8 characters long.")
    assert is_strong_password("P@ssword1") == (True, "\nPassword is strong.")
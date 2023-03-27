import sys
import os
from pyisemail import is_email
from util import *
from var import *
from encrypte import *

class PasswordManager:
    def __init__(self, master_password):
        self.data = self.load_data()
        self.master_password = master_password

    def load_data(self):
        """
        Load data from json file
        """
        if not os.path.exists(os.path.dirname(PATH)):
            os.makedirs(os.path.dirname(PATH))
        if not os.path.exists(PATH):
            with open(PATH, 'w') as file:
                file.write('{}')           
        return exe_data(PATH)

    def save_data(self):
        """
        Save data to json file
        """
        exe_data(PATH, self.data, m='w')
        

    def menu(self):
        """
        Check for user choice and call the appropriate function
        """
        while True:
            try:
                choice = input(MAIN_MENU).strip()
                if choice == '1':
                    self.add()
                elif choice == '2':
                    self.search()
                elif choice == '3':
                    self.update()
                elif choice == '4':
                    sys.exit("\nGoodbye~~")
                else:
                    raise ValueError()
            except ValueError:
                print("\nNot a Valid choice!")
                pass

    def add(self):
        """
        Add data to json file
        """
        print(MSG_ADD)
        site_name, user_name, email_address = extract_command('add')
        if not site_name:
            site_name = input('\nEnter the site name: ').strip()
        if not user_name:
            user_name = input('Enter the username: ').strip()
        if not email_address:
            while True:
                try:
                    temp_email = input('Enter the email address: ').strip()
                    if is_email(temp_email):
                        email_address = temp_email
                        break
                except ValueError:
                    print("Please enter a valid email!")
                    pass
        decrypted_password = None 
        the_key = None       
        # Take and encrypt the password  
        if not os.path.exists(PATH_H):
           the_key = create_new_key(self.master_password.encode('utf-8'))
        
        max_attempts = 3
        attempt = 0
        while attempt < max_attempts:
            try:
                self.master_password = input("\n First enter your master password for verification: ").encode('utf-8')
                the_key = regenerated_key(self.master_password) 
                data = exe_data(PATH, m='r')
                for k in data:
                    for i in data[k]:
                        if i['id'] == 1:
                            decrypted_password = decrypte_password(i['password'], the_key)
                        if decrypted_password == None:
                            raise ValueError
                break
            except ValueError:
                attempt += 1
                print("\nIncorrect Password, attempt", attempt, "of", max_attempts)
                if attempt == max_attempts:
                    sys.exit("Maximum attempts reached, exiting.")
                          
        password = input('\n Now enter the password: ').strip()
        encrypted_password = encrypte_password(password, the_key)
        
        # Generate an ID number for the new entry
        entry_id = len(self.data) + 1
        
        # Check if the site already exists in the data if not append the data in the key
        # else add it at the end with the new key
        if site_name in self.data:
            self.data[site_name].append({'id': entry_id, 'name': user_name, 'email': email_address, 'password': encrypted_password})
        else:
            self.data[site_name] = [{'id': entry_id, 'name': user_name, 'email': email_address, 'password': encrypted_password}]

        self.save_data()
        print(f'\n{site_name.capitalize()} added successfully!')
     
    def search(self): 
        """
        Read data from json file with flexibility
        """
        print(MSG_SEARCH)
        data = exe_data(PATH)
        site_name, user_name, email_address = extract_command('search')
    
        get = None
        if not site_name:
            site_name = input("\nSite name/link you are looking for: ")   
            email_address = input("The email address: ")
        for key in data:
            if site_name == key:
                get = data[key]
        if get is None:
            print("\nSite not found.")
            self.menu()   
        decrypted_password = None      
        # Loop through the data to find the matching user_name or email_address      
        for key in get:
            # Try to decryte message if fail 3 time exit the program
            max_attempts = 3
            attempt = 0
            while attempt < max_attempts:
                try:
                    self.master_password = input("\n First enter your master password for verification: ").encode('utf-8')
                    the_key = regenerated_key(self.master_password)  
                    decrypted_password = decrypte_password(key['password'], the_key)
                    if decrypted_password == None:
                        raise ValueError
                    break
                except ValueError:
                    attempt += 1
                    print("\nIncorrect Password, attempt", attempt, "of", max_attempts)
                    if attempt == max_attempts:
                       sys.exit("Maximum attempts reached, exiting.")
                       
            if not email_address:
            # If user_name and email_address are not provided, print all the details
                print(f"\nResult: \nSite: {site_name} \nName: {key['name']} \nEmail: {key['email']} \nPassword: {decrypted_password}")
            # If user_name or email_address is provided, print the matching details decrypte_password(key['password']
            elif 'name' in key and 'email' in key and key['email'] == email_address:
                print(f"\nResult: \nSite: {site_name} \nName: {key['name']} \nEmail: {key['email']} \nPassword: {decrypted_password}")
            self.menu()    
            
    def update(self):
        """
        Update data from json file
        """
        print(MSG_UPDATE)
        data = exe_data(PATH)
        site_name, user_name, email_address = extract_command('update')
    
        # This loop will keep prompting the user to input the site name and email address they want to update
        while True:
            try:
                if not site_name:
                    site_name = input("\nSearch for data you want to update by site name: ")
                if not email_address:    
                    email_address = input("\nNow enter the email address: ")
                break
            except (TypeError, ValueError):
                print("\nError: Please use an space between them Usage:site.com myemail@site.com")
            
        # This loop will search for the data to update using the site_name and email_address entered by the user.
        for key in data:
            if key == site_name:
                for item in data[key]:
                    if item['email'] == email_address:
                        print(f"\n\nData ready. \nSite: {site_name} \nName: {item['name']} \nEmail: {item['email']} \nPassword: Encrypted password")
                        field = input("\nWhich one do you want to update? \n1- Site name \n2- User name \n3- Email address \n4- Password \n\n Your choice: ").strip()
                        # Try to decryte message if fail 3 time exit the program
                        max_attempts = 3
                        attempt = 0
                        while attempt < max_attempts:
                            try:
                                self.master_password = input("\n First enter your master password for verification: ").encode('utf-8')
                                the_key = regenerated_key(self.master_password)  
                                decrypted_password = decrypte_password(item['password'], the_key)
                                if decrypted_password == None:
                                    raise ValueError
                                break
                            except ValueError:
                                attempt += 1
                                print("Incorrect Password, attempt", attempt, "of", max_attempts)
                                if attempt == max_attempts:
                                    sys.exit("Maximum attempts reached, exiting.")   
                        
                        if field == '3':
                            while True:
                                try:
                                    temp_value = input("\nEnter the new value: ")
                                    if is_email(temp_value):
                                        new_value = temp_value
                                        break
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print("Please enter a valid email!")
                        else:
                            new_value = input("\nEnter the new value: ")
                    
                        # Updates the selected field in the data dictionary.
                        if field == '1':
                            try:
                                data[new_value] = data.pop(site_name)
                            except KeyError:
                                print("\nError: Site name not found.")
                        elif field == '2':
                            item['name'] = new_value
                        elif field == '3':
                            item['email'] = new_value
                        elif field == '4':
                            # Encrypte the password and store it
                            encrypted_password = encrypte_password(new_value, the_key)
                            item['password'] = encrypted_password
                        else:
                            print("Invalid field selected.")
                        exe_data(PATH, data, m='w')
                        print("\nData updated successfully!")
                        self.menu()
        print("Data not found.")
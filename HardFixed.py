import csv
import string
import time
from passlib.context import CryptContext

CONTEXT = CryptContext(
        schemes=['bcrypt_sha256'],
        bcrypt_sha256__default_rounds=13
        )

DEFAULT_PASSWORD = '$bcrypt-sha256$v=2,t=2b,r=13$eg5hCWKusMROp776ATf8au$nX6dbyzhhoor67RZL/KgoTHUjOs83xm'

def authenticate_user(user, password):
            '''
            method to authenticate the user
            based on the object's user and 
            password
            '''
            #load the users from the database to a list
            users = []
            with open('HW3/users.csv') as userfile:
                reader = csv.DictReader(userfile)
                for i in reader:
                    users.append(i)
            #breakout the usernames and passwords
            #print(users)
            usernames = []
            passwords = []
            privileges = []
            for i in users:
                usernames.append(i.get('username'))
                passwords.append(i.get('password_hash'))
                privileges.append(i.get('privilege'))
                #print(i.get('privilege'))
            #check for the matching user and password
            for i in range(0, len(usernames)):
                #print(f'{usernames[i]}:{privileges[i]}')
                if CONTEXT.verify(user, usernames[i]) and CONTEXT.verify(password, passwords[i]):
                    privilege = privileges[i]
                    if user == 'root' and CONTEXT.verify(password, DEFAULT_PASSWORD):
                        try:
                            change_password(user, input("You must enter a new password: "))
                            return True
                        except Exception as e:
                            raise Exception(str(e))
                    else:
                        return True
            #raise an error if the login is bad
            raise ValueError("Bad username or password!")

def change_password(user, new_pass):
        '''
        function to change the password of a
        registered user
        parameters:
            new_pass str new password for user
        '''
        if len(new_pass)<1:
            raise Exception("Failed to change password!")
        if CONTEXT.verify(new_pass, DEFAULT_PASSWORD):
            raise Exception("Cannot use the same default password!")
        try:
            #create a users list and populate with dicts
            users = []
            with open('HW3/users.csv') as userfile:
                reader = csv.DictReader(userfile)
                for i in reader:
                    users.append(i)
            #find the user in the list and replace the password hash
            for i in users:
                if CONTEXT.verify(user, i['username']):
                    #print(i)
                    i['password_hash'] = hash_item(new_pass)
            #create the headers for the user csv based on the user objects
            keys = users[0].keys()
            columns = []
            for i in keys:
                columns.append(i)
            #open the users csv and write the new dict with the changed user
            with open('HW3/users.csv', 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=columns)
                writer.writeheader()
                for user in users:
                    writer.writerow(user)
        except:
            raise Exception("Failed to change password!")

def hash_item(item):
        '''
        Function to hash the password
        '''
        return CONTEXT.hash(item)
            
def program_login():
    print('Welcome to the Missile Console')
    user = input('Please enter your username: ')
    password = input('Please enter your password: ')
    print('Authenticating....')
    try:
        authenticate_user(user, password)
        print('SUCCESS')
        time.sleep(5)
        print(f'You are logged in as {user}')
    except Exception as e:
        print(e)
        exit(0)
        
program_login()
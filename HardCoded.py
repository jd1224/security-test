import csv
import string
import time
from passlib.context import CryptContext

#store the privilege level of a user
privilege = ''

CONTEXT = CryptContext(
        schemes=['bcrypt_sha256'],
        bcrypt_sha256__default_rounds=13
        )
DEFAULT_PASSWORD = '$bcrypt-sha256$v=2,t=2b,r=13$eg5hCWKusMROp776ATf8au$nX6dbyzhhoor67RZL/KgoTHUjOs83xm'
DEFAULT_USER = '$bcrypt-sha256$v=2,t=2b,r=13$4C8aZ02goTcYYMGzHxJ/O.$SSMRAUNn0abOxOnKasziE.kIZxEhGWq'

def authenticate_user(user, password):
    global privilege
    if CONTEXT.verify(user, DEFAULT_USER):
        privilege = 'root'
        return(CONTEXT.verify(password, DEFAULT_PASSWORD))
    else:
        users = []
        with open('HW3/users.csv') as userfile:
            reader = csv.DictReader(userfile)
            for i in reader:
                users.append(i)
                #print(i)
        #breakout the usernames and passwords
        usernames = []
        passwords = []
        privileges = []
        for i in users:
            usernames.append(i.get('username'))
            passwords.append(i.get('password_hash'))
            privileges.append(i.get('privilege'))
            
        #check for the matching user and password
        for i in range(0, len(usernames)):
            #print(f'{usernames[i]}:{passwords[i]}:{privileges[i]}')
            if CONTEXT.verify(user, usernames[i]) and CONTEXT.verify(password, passwords[i]):
                privilege = privileges[i]
                return True

def program_login():
    print('Welcome to the Missile Console')
    user = input('Please enter your username: ')
    password = input('Please enter your password: ')
    print('Authenticating....')
    if authenticate_user(user, password):
        print('SUCCESS')
        time.sleep(5)
        print(f'You are logged in as {user}')
    else:
        print('You have provided invalid credentials. Goodbye!')
        exit(0)

program_login()
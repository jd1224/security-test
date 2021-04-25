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

def launch_missile():
    choice = input('Are you sure you want to launch the missile? ')
    if 'y' in choice.lower():
        print("Launched!!!!")
        exit(0)
    else:
        print("I'm glad you reconsidered!")

def hash_item(password):
        '''
        Function to hash the password
        '''
        return CONTEXT.hash(password)

def create_users(username, password):
    '''
    Function to register a new
    user and save the user to
    the database.
    '''
    hashed_password = hash_item(password)
    hashed_user = hash_item(username)
    data = [hashed_user, hashed_password, "user"]
    #store the user information in the flat database
    with open('HW3/users2.csv', 'a+', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)

def reports():
    print('reports')
    
def targets():
    print('targets')

def start_screen():
    while True:
        print('*********************************')
        print('*********************************')
        print('*    Welcome to the Main Menu   *')
        print('*********************************')
        print('Make a choice from the following ')
        print('*********************************')
        print('1. Routine Reports')
        print('2. Check Targeting Status')
        print('3. Launch Missile')
        print('4. Add User')
        print('5. Exit')
        choice = input('Please choose a number: ')
        if choice == '1':
            reports()
        elif choice == '2':
            targets()
        elif choice == '3':
            launch_missile()
        elif choice == '4':
            user = input('Enter a new username: ')
            password = input('Enter the new password: ')
            create_users(user, password)
        elif choice =='5':
            exit(0)
        else:
            print('You have to choose from the numbers')
            
start_screen()
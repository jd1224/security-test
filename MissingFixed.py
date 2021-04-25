from user import User
import time


def program_login():
    print('Welcome to the Missile Console')
    user = input('Please enter your username: ')
    password = input('Please enter your password: ')
    print('Authenticating....')
    try:
        client = User(user, password)
        client.authenticate_user()
        return client
    except Exception as e:
        print(str(e))
        exit(0)

def launch_missile():
    client = program_login()
    if client.check_permissions('root'):
        choice = input('Are you sure you want to launch the missile? ')
        if 'y' in choice.lower():
            print("Launched!!!!")
            exit(0)
        else:
            print("I'm glad you reconsidered!")
            time.sleep(3)
    else:
        print('You must be root to launch the missiles!')
        time.sleep(3)

def reports():
    print('reports placeholder to show a non-critical function')
    time.sleep(5)
    
def targets():
    print('targets placeholder to show a non-critical function')
    time.sleep(5)

def create_user():
    client = program_login()
    if client.check_permissions('root'):
        username = input('Please enter a new username: ')
        password = input('Please enter a new Password: ')
        try:
            client.create_users(username, password)
            print(f'{username} created!')
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(3)
    else:
        print('You must be root to create a new user!')
        time.sleep(3)

def start_screen():
    while True:
        print('*********************************')
        print('*    Welcome to the Main Menu   *')
        print('*********************************')
        print('*********************************')
        print('Make a choice from the following ')
        print('*********************************')
        print('1. Routine Reports')
        print('2. Check Targeting Status')
        print('3. Launch Missile')
        print('4. Create User(root only)')
        print('5. Exit')
        choice = input('Please choose a number: ')
        if choice == '1':
            reports()
        elif choice == '2':
            targets()
        elif choice == '3':
            launch_missile()
        elif choice == '4':
            create_user()
        elif choice == '5':
            exit(0)
        else:
            print('You have to choose from the numbers')
            
        
        
start_screen()
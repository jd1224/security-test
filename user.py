import csv
import string
import time
from passlib.context import CryptContext


class User:
    
    def __init__(self, user, password):
        self.user = user.lower()
        self.password = password
        
    DEFAULT_PASSWORD = '$bcrypt-sha256$v=2,t=2b,r=13$eg5hCWKusMROp776ATf8au$nX6dbyzhhoor67RZL/KgoTHUjOs83xm'
    
    CONTEXT = CryptContext(
            schemes=['bcrypt_sha256'],
            bcrypt_sha256__default_rounds=13
            )
        
    def authenticate_user(self):
            '''
            method to authenticate the user
            based on the object's user and 
            password
            '''
            #load the users from the database to a list
            users = []
            with open('HW3/users2.csv') as userfile:
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
                if self.CONTEXT.verify(self.user, usernames[i]) and self.CONTEXT.verify(self.password, passwords[i]):
                    self.privilege = privileges[i]
                    if self.user == 'root' and self.CONTEXT.verify(self.password, self.DEFAULT_PASSWORD):
                        try:
                            self.change_password(input("You must enter a new password: "))
                            return True
                        except Exception as e:
                            raise Exception(str(e))
                    else:
                        return True
            #raise an error if the login is bad
            raise ValueError("Bad username or password!")
 
    def change_password(self, new_pass):
        '''
        function to change the password of a
        registered user
        parameters:
            new_pass str new password for user
        '''
        if len(new_pass)<1:
            raise Exception("Failed to change password!")
        if self.user == 'root' and self.CONTEXT.verify(new_pass, self.DEFAULT_PASSWORD):
            raise Exception("Cannot use the same default password!")
        try:
            #create a users list and populate with dicts
            users = []
            with open('HW3/users2.csv') as userfile:
                reader = csv.DictReader(userfile)
                for i in reader:
                    users.append(i)
            #find the user in the list and replace the password hash
            for i in users:
                if self.CONTEXT.verify(self.user, i['username']):
                    #print(i)
                    i['password_hash'] = self.hash_item(new_pass)
            #create the headers for the user csv based on the user objects
            keys = users[0].keys()
            columns = []
            for i in keys:
                columns.append(i)
            #open the users csv and write the new dict with the changed user
            with open('HW3/users2.csv', 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=columns)
                writer.writeheader()
                for user in users:
                    writer.writerow(user)
        except:
            raise Exception("Failed to change password!")
   
    def check_user_registered(self):
        '''
        function to check if a user is
        already registered.
        '''
        users = []
        with open('HW3/users2.csv') as userfile:
            reader = csv.DictReader(userfile)
            for i in reader:
                users.append(i)
        usernames = []
        for i in users:
            usernames.append(i.get('username'))
        for i in usernames:
            if self.CONTEXT.verify(self.user, i):
                return True
        else:
            return False

    def hash_item(self, password=False):
        '''
        Function to hash the password
        '''
        if not password:
            password = self.password
        return self.CONTEXT.hash(password)

    def check_permissions(self, permission):
        return self.privilege == permission
       
    def create_users(self, username, password):
        '''
        Function to register a new
        user and save the user to
        the database.
        '''
        #check to see if the username or email is already registered
        if self.privilege == 'root':
            new_user = User(username, password)
            if not new_user.check_user_registered():
                #hash the password using a pbkdf2
                hashed_password = self.hash_item(new_user.password)
                hashed_user = self.hash_item(new_user.user)
                data = [hashed_user, hashed_password, "user"]
                #store the user information in the flat database
                with open('HW3/users2.csv', 'a+', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(data)
            else:
                raise ValueError("User Already Exists!")
        else:
            raise ValueError("You must be the root user to create new users.")
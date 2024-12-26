import os
import json
from cryptography.fernet import Fernet

#Generating fernet key
def generate_key():
     key=Fernet.generate_key()
     with open('key.key','wb') as key_file:
          key_file.write(key)

#Loading Fernet key
def load_key():
     return open('key.key','rb').read()


if not os.path.exists('key.key'):
     generate_key()
key=load_key()
fernet=Fernet(key)

#Storing master password
if(not os.path.exists('master_pass.json')):
     master_pass=input('Enter you master password\n(NOTE:- Remember this passord to access passowrd manager) :')
     encry_master_pass=fernet.encrypt(master_pass.encode()).decode()
     with open('master_pass.json','w') as master_file :
          json.dump(encry_master_pass,master_file)

#Loading master password
def load_master_pass():
     with open('master_pass.json','r') as master_file:
          encry_master_pass=json.load(master_file)
          decry_master_pass=fernet.decrypt(encry_master_pass.encode()).decode()
          return decry_master_pass

#Loading all paswords from json file to dictionary
def load_pass():
     if(not os.path.exists('passwords.json')):
          with open('passwords.json','w') as pass_file:
               json.dump({},pass_file)
     try:
          with open('passwords.json','r') as pass_file:
               return json.load(pass_file)
     except e:
          return {}

#Saving passwords from dictionary to json file
def save_pass(password):
     with open('passwords.json','w') as pass_file:
          json.dump(password,pass_file)

#Saving a new password
def add_pass(platform,username,password):
     passwords=load_pass()
     encry_pass=fernet.encrypt(password.encode()).decode()
     passwords[platform]={'username':username,'password':encry_pass}
     save_pass(passwords)
     print(f'password for {platform} saved successfully\n')

#Viewing all paswords
def view_pass():
     passwords=load_pass()
     for platform,credentials in passwords.items():
          user=credentials['username']
          encry_pass=credentials['password']
          decry_pass=fernet.decrypt(encry_pass.encode()).decode()
          print(f'username and password for {platform} is : {user}, {decry_pass}')
     print()

#Deleting a password from file
def del_pass(platform):
     passwords=load_pass()
     if platform in passwords:
          del passwords[platform]
     save_pass(passwords)
     print(f'password for {platform} deleted successfully\n')

#Viewing a password for specific platform
def view_spec_pass(platf):
     passwords=load_pass()
     for platform,credentials in passwords.items():
          if(platf == platform):
               username=credentials['username']
               encry_pass=credentials['password']
               decry_pass=fernet.decrypt(encry_pass.encode()).decode()
               print(f'username and password for {platform} is : {username}, {decry_pass}\n')

def main():
     mas_pass=load_master_pass()
     entered_mas_pass=input('Enter your master passowrd : ')
     if(entered_mas_pass == mas_pass):
          while True:
               print("---- Password Manager ----")
               print("1. Add a new password")
               print("2. View a specific password")
               print("3. Delete a specific password")
               print("4. View all passwords")
               print("5. Exit")
               print()
               choice = eval(input("Enter your choice (1-5): "))
               print()
               
               if(choice==1):
                    platform=input('Enter platform name : ')
                    username=input('Enter username : ')
                    password=input('Enter password : ')
                    add_pass(platform,username,password)
     
               elif(choice==2):
                    platform=input('Enter platform name : ')
                    view_spec_pass(platform)
     
               elif(choice==3):
                    platform=input('Enter platform name : ')
                    del_pass(platform)
     
               elif(choice==4):
                    view_pass()
     
               elif(choice==5):
                    break         
     
               else:
                    print('Invalid output')
     else:
          print('\nWrong master password\nRenter your matser password\n')
          main()

main()

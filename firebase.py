import firebase_admin
from firebase_admin import credentials, db
import pwinput
import survey
import sys
import os

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

cred = credentials.Certificate("utils/private_key.json")
firebase_admin.initialize_app(cred, {"databaseURL":"https://shroomraider-70f6a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
reference = db.reference("/")

def login():
    print("Loading data...")
    users = reference.child("users").get()
    while True:
        clear()
        username = input("Enter Username: ")
        password = pwinput.pwinput(prompt="Enter your password: ", mask="*")
        if username not in users or reference.child(f"users/{username}/password").get() != password:
            options_list = ["Try again", "Return"]
            answer = options_list[survey.routines.select('Incorrect Username or Password ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                return None
        else:
            return username

def signup():
    print("Loading data...")
    users = reference.child("users").get()
    while True:
        clear()
        username = input("Enter Username: ")
        password = pwinput.pwinput(prompt="Enter your password: ", mask="*")
        confirmpassword = pwinput.pwinput(prompt="Reenter your password: ", mask="*")
        if password == confirmpassword and username not in users:
            reference.child("users").update({
                username:{
                    "password": password,
                    "rank": 1000,
                    "story_level": "levels/spring/stage1.txt"
                }
            })
            print(f"Welcome to Shroom Raider, {username}")
            return username
        else:
            options_list = ["Try again", "Return"]
            answer = options_list[survey.routines.select("Password mismatched " if password != confirmpassword else "Username already taken ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                return None
        

while True:
    clear()
    options_list = ["Login", "Sign up", "Play Locally", "Exit"]
    playmode = options_list[survey.routines.select('Welcome to Shroom Raider! ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
    if playmode == "Login":
        username = login()
        if username != None:
            break
    elif playmode == "Sign up":
        username = signup()
        if username != None:
            break
    elif playmode == "Play Locally":
        print("start")
        ... #continue as guest
    else:
        sys.exit()
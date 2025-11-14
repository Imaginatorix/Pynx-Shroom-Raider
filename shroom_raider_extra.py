import colorama
<<<<<<< HEAD
from colorama import Fore, Style
=======
import socket
import pwinput
import survey
import os
import keyboard
import sys
import argparse
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement_extra import user_input, keyboard_tracker
from utils.ui import show_screen
from utils.game_progress import shroom_level_parser_generator
from utils.validator import validate_level_info, validate_locations
from utils.algorithm import generate_map
from colorama import Fore, Style
from firebase_admin import credentials, db, initialize_app
from itertools import cycle
from threading import Thread
from time import sleep
from copy import deepcopy
<<<<<<< HEAD
import sys
import argparse
import firebase_admin
from firebase_admin import credentials, db
import pwinput
import survey
import os


=======
from pathlib import Path
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa

if os.name == 'nt':
    import msvcrt
else:
    import termios

def input_clear():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
<<<<<<< HEAD
        
global allow_auto_keyboard
global allow_gamepad

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
=======

def spinner(controller, text="Loading"):
    frames = cycle(["|", "/", "-", "\\"])
    clear()
    while not controller["stop"]:
        sys.stdout.write(f"\r{text} {next(frames)}")
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write("\r")  # clear
    sys.stdout.flush()
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def login(reference):
    controller = {"stop": False}
    thread = Thread(target=spinner, args=(controller,))
    thread.start()
    users = reference.child("users").get()
    controller["stop"] = True
    thread.join()
    while True:
        clear()
        username = input(f"{"Enter Username":<20}|: ")
        password = pwinput.pwinput(prompt=f"{"Enter your password":<20}|: ", mask="*")
        if username not in users or reference.child(f"users/{username}/password").get() != password:
            options_list = [f"{"Try again":<15}| Input username and password again", f"{"Return":<15}| Go back to starting screen"]
            input_clear()
            print("")
            answer = survey.routines.select('Incorrect Username or Password ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                return None
        else:
            global allow_auto_keyboard
<<<<<<< HEAD
            global allow_gamepad

            allow_auto_keyboard = reference.child(f"users/{username}/allow_auto_keyboard").get()
            allow_gamepad = reference.child(f"users/{username}/allow_gamepad").get()
=======
            controller = {"stop": False}
            thread = Thread(target=spinner, args=(controller,))
            thread.start()
            allow_auto_keyboard = reference.child(f"users/{username}/allow_auto_keyboard").get()
            controller["stop"] = True
            thread.join()
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            return username

def signup(reference):
    global allow_auto_keyboard
<<<<<<< HEAD
    global allow_gamepad
    print("Loading data...")
=======
    controller = {"stop": False}
    thread = Thread(target=spinner, args=(controller,))
    thread.start()
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
    users = reference.child("users").get()
    controller["stop"] = True
    thread.join()
    while True:
        while True:
            clear()
            username = input(f"{"Enter Username":<20}|: ")
            if username not in users:
                break
            options_list = [f"{"Try again":<15}| Input username again", f"{"Return":<15}| Go back to starting screen"]
            input_clear()
            answer = survey.routines.select("Username already taken",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                return None
        while True:
            password = pwinput.pwinput(prompt=f"{"Enter your password":<20}|: ", mask="*")
            confirmpassword = pwinput.pwinput(prompt=f"{"Reenter your password":<20}|: ", mask="*")
            if len(password) < 7 or password != confirmpassword:
                options_list = [f"{"Try again":<15}| Input password again", f"{"Return":<15}| Go back to starting screen"]
                input_clear()
                answer = survey.routines.select("Password must atleast be 8 characters long! " if len(password) < 7 else "Password mismatched! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                if answer == 1:
                    return None
                clear()
                print("Enter Username: " + username)
            else:
<<<<<<< HEAD
                options_list = ["Automatically input keyboard strokes", "Collect keyboard strokes and click enter to input"]
=======
                clear()
                print("Account has been created")
                options_list = [f"{"Auto":<9}| Automatically input keyboard strokes", f"{"Manual":<9}| Collect keyboard strokes and click enter to input"]
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
                input_clear()
                answer = survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                if answer == 1:
                    allow_auto_keyboard = True
                    options_list = ["Allow gamepad inputs", "Restrict to only keyboards"]
                    input_clear()
                    answer = options_list[survey.routines.select("Do you want to allow gamepad inputs (only applicable if 'Automatically input keyboard strokes' is on)? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
                    if answer == "Allow gamepad inputs":
                        allow_gamepad = True
                    else:
                        allow_gamepad = False
                else:
                    allow_auto_keyboard = False
<<<<<<< HEAD
                    allow_gamepad = False
=======
                controller = {"stop": False}
                thread = Thread(target=spinner, args=(controller,))
                thread.start()
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
                reference.child("users").update({
                    username:{
                        "password": password,
                        "rank": 1000,
                        "story_level": "levels/spring/stage1.txt",
                        "allow_auto_keyboard": allow_auto_keyboard,
                        "allow_gamepad": allow_gamepad
                        }
                    }
                )
                controller["stop"] = True
                thread.join()
                return username
                
def gameloop(level_info, locations, moves = "", output_file = ""):
<<<<<<< HEAD
=======
    
    clear()
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
    colorama.init(autoreset=True)

    # Check whether the map data is valid
    validate_locations(*level_info["size"], locations)
    validate_level_info(level_info)

    original_level_info = deepcopy(level_info)
    original_locations = deepcopy(locations)

    moves_count = 0

    if output_file:
        has_clear = "NO CLEAR"
    else:
        show_screen(level_info, locations)
    while True:
        if output_file and not moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, " ")
            moves = ""
        elif moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, moves)
            moves = ""
        elif allow_auto_keyboard == False:
            actions = user_input(level_info, locations, original_locations, original_level_info)
        else:
            keyboard_input = keyboard_tracker(allow_gamepad)
            input_clear()    
            if keyboard_input in ("w","a","s","d","p", "!", "e"):
                actions = user_input(level_info, locations, original_locations, original_level_info, keyboard_input)
                show_screen(level_info, locations)
            elif keyboard_input == "buffer":
                continue
            else:
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                continue
        for current_locations, current_level_info in actions:
            level_info = current_level_info
            locations = current_locations 

            if not (current_locations and current_level_info):
                return "exit"
<<<<<<< HEAD
            if current_level_info["invalid_input"]:
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                break
            else:
                moves_count += 1
            level_info = current_level_info
            locations = current_locations 

            if (level_info, locations) ==  (original_level_info, original_locations): #fix, still primative make a reset method
=======
            
            if not output_file:
                show_screen(level_info, locations)
                sleep(0.15)

            if level_info["invalid_input"] and not output_file:
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
            else:
                moves_count += 1
                
            if level_info["level_reset"]:
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
                moves_count = 0
                continue

<<<<<<< HEAD
            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You got all mushrooms!")
=======
            if level_info["game_end"] and level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    clear()
                    show_screen(level_info, locations)
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
                break
            elif level_info["game_end"]:
                if not output_file:
                    print(Fore.RED + Style.BRIGHT + "You drowned!")
                    moves_count = -1
                break
<<<<<<< HEAD
=======
        
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
        if output_file:
            parse_output(output_file, locations, level_info, has_clear)
            break
        elif level_info["game_end"]:
            break
        del actions
    del level_info
    del locations
    del original_level_info
    del original_locations
    return moves_count

def story_mode(story_progress):
    output = {}
    while True:
        level_info, locations = parse_level(story_progress)
<<<<<<< HEAD
        moves_count = gameloop(level_info, locations, moves, output_file)
        if type(moves_count) == str:
            options_list = ["Try again", "Return to main menu"]
=======
        try:
            moves_count = gameloop(level_info, locations, moves, output_file)
        finally:
            keyboard.unhook_all()
        if type(moves_count)is str:
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Return":<15}| Go back to levels menu"]
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            input_clear()
            answer = survey.routines.select("You gave up! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                break
        elif moves_count == -1:
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = survey.routines.select("You died! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                break
        else:
            output[story_progress] = moves_count
            options_list = [f"{"Next Level":<15}| Continue playing and enter the next level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = survey.routines.select(f"You've beaten the level with {moves_count} moves!. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                break
            else:
                story_progress = next(shroom_level_parser_generator(story_progress)) # if end map what
    return output

def unlocked_levels(username = "", reference = ""):
    try_again = False
    while True:
        if try_again:
            try_again = False
        else:
            if username:
                input_clear()
                controller = {"stop": False}
                thread = Thread(target=spinner, args=(controller,))
                thread.start()
                options_list = [level for level in reference.child(f"users/{username}/story_data").get()] + ["Return to levels menu"]
                controller["stop"] = True
                thread.join()
                if not options_list:
                    print("Play through the \"Story\" mode to unlock levels")
            else:
                print("Currently playing locally, progress won't be saved")
<<<<<<< HEAD
                options_list = ["spring - stage1"] + [level.split("\\")[1] + " - " + level.split("\\")[2][:-4] for level in shroom_level_parser_generator()] + ["Return to main menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select(f"Choose from the following unlocked levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if chosen_level == "Return to main menu":
                break

        season = chosen_level.split(" - ")[0]

=======
                options_list = ["spring - stage1"] + [Path(level).parts[1] + " - " + Path(level).stem for level in shroom_level_parser_generator()] + ["Return to levels menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select("Choose from the following unlocked levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if chosen_level == "Return to levels menu":
                break

>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
        chosen_level_path = f"levels/{chosen_level.split(" - ")[0]}/{chosen_level.split(" - ")[1]}.txt"
        level_info, locations = parse_level(chosen_level_path)
        moves_count = gameloop(level_info, locations, moves, output_file)

<<<<<<< HEAD
        if type(moves_count) == str:
            options_list = ["Try again", "Choose level", "Return to main menu"]
=======
        if type(moves_count) is str:
            options_list = [f"{"Try again":<15}| Restart the map and play again",f"{"Choose Level":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            input_clear()
            answer = survey.routines.select("Laro gave up! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            
            if answer == 0:
                try_again = True
            elif answer == 2:
                break

        elif moves_count == -1:
            options_list = [f"{"Try again":<15}| Restart the map and play again",f"{"Choose Level":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = survey.routines.select("You died! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            
            if answer == 0:
                try_again = True
            elif answer == 2:
                break

        else:
            if username:
                print(f"Current moves: {moves_count}, Previous moves: {reference.child(f"users/{username}/story_data/{chosen_level}").get()}")
                
                options_list = [f"{"Yes":<5}| Keep the new move count", f"{"No":<5}| Disregard the new move count"]
                input_clear()
                answer = survey.routines.select(f"Do you want to keep the current move count?",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                
                if answer == 0:
                    reference.child(f"users/{username}/story_data/{chosen_level}").set(moves_count)
                    reference.child(f"level_leaderboard/{chosen_level}/{username}").set(moves_count)
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Choose Level":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = options_list[survey.routines.select(f"You've beaten the level with {moves_count} moves!. " if not username else "",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            
            if answer == 0:
                try_again = True
            elif answer == 2:
                break
    return

def find_match(username, reference): 
    waiting_for_opponent = False
    controller = {"stop": False}
    thread = Thread(target=spinner, args=(controller,))
    thread.start()
    while True:
        sleep(1.5)
        if not waiting_for_opponent:
            if reference.get():
                available_rooms = reference.get()
                for room in available_rooms:
                    if len(available_rooms[room]) < 2: #found an available room
                        opponent = room
                        reference.child(f"{room}/{username}").set(-2)
                        controller["stop"] = True
                        thread.join()
                        clear()
                        print("")
                        print(f"Opponent found: {opponent}")
                        sleep(1.5)
                        return (room, opponent)
            #if no available room, create one
            room = username
            reference.child(f"{room}/{username}").set(-2)
            waiting_for_opponent = True
        else:
            #if created a room, wait till an opponent
            if len(reference.child(room).get()) == 2:
                for user in reference.child(room).get():
                    if user != username:
                        opponent = user
                controller["stop"] = True
                thread.join()
                clear()
                print(f"Opponent found: {opponent}")
                sleep(1.5)
                break
    return (room, opponent)

def match(username, reference, room, opponent, gamemode):
    level_info, locations = parse_level("levels/spring/stage1.txt") #get random file from edward
    moves_count = gameloop(level_info, locations, moves, output_file)
    reference.child(f"{room}/{username}").set(moves_count)
    print(f"You finished in {moves_count} moves")
    opponent_moves_count = reference.child(f"{room}/{opponent}").get()
    if opponent_moves_count == -2:
        print(f"Waiting for {opponent} to finish", end="")
        while True:
            sleep(1.5)
            print(".", end="")
            opponent_moves_count = reference.child(f"{room}/{opponent}").get()
            if opponent_moves_count > -1:
                print(" ")
                print(f"{opponent} has finished in {opponent_moves_count} moves")
                break
            elif opponent_moves_count == -1 or opponent_moves_count == "exit":
                break
    if opponent_moves_count == -1 or opponent_moves_count == "exit":
        match_result = f"{opponent} didn't finish, you automatically won"
        rank_score = 15
    elif moves_count == -1 or moves_count == "exit":
        match_result = f"You didn't finish, automatically lost"
        rank_score = -15
    elif moves_count > -1 and moves_count == opponent_moves_count:
        match_result = f"You tied with {opponent}"
        rank_score = 5
    elif moves_count > -1 and moves_count < opponent_moves_count:
        match_result = f"You've defeated {opponent} by {opponent_moves_count - moves_count}"
        rank_score = 15 + opponent_moves_count - moves_count
    elif moves_count > -1 and moves_count > opponent_moves_count:
        match_result = f"You've lost to {opponent} by {moves_count - opponent_moves_count}"
        rank_score = -15 - opponent_moves_count - moves_count
    reference.child(f"{room}/{opponent}").delete()
    if gamemode == "unranked":
        return match_result
    else:
        return match_result, rank_score

def preferences(username): #to implement
    while True:
<<<<<<< HEAD
        options_list = ["Keyboard", "Gamepad Recognition", "Return"]
        input_clear()
        answer = options_list[survey.routines.select('Settings Page ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if answer == "Keyboard":
            options_list = ["Auto input", "Press enter after input", "Return"]
            input_clear()
            answer = options_list[survey.routines.select('Choose method of controlling Laro ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Auto input": 
                allow_auto_keyboard = False
            else:
                allow_auto_keyboard = True
            print()#does global var work

=======
        clear()
        password = pwinput.pwinput(prompt="Enter your password: ", mask="*")
        confirmpassword = pwinput.pwinput(prompt="Reenter your password: ", mask="*")
        if old_password == password:
            options_list = [f"{"Try again":<15}| Enter new password again", f"{"Return":<15}| Go back to settings menu"]
            input_clear()
            answer = survey.routines.select("Entered password is same as old one ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                return
        elif len(password) < 7 or password != confirmpassword:
            options_list = [f"{"Try again":<15}| Enter new password again", f"{"Return":<15}| Go back to settings menu"]
            input_clear()
            answer = survey.routines.select("Password must atleast be 8 characters long! " if len(password) < 7 else "Password mismatched! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                return None
        else:
            reference.child(f"users/{username}/password").set(password)
            survey.routines.select("New password has been set ",  options = ["Return"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def delete_account(username, reference):
    count = 0
    while count < 4:
        options_list = ["Yes, Delete", "Return"]
        options_list = [f"{"Yes":<10}| Delete my account", f"{"Return":<10}| Go back to settings menu"]
        input_clear()
        answer = survey.routines.select(f"Are you {"really "*count}sure? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if answer == 1:
            return None
        count += 1
    controller = {"stop": False}
    thread = Thread(target=spinner, args=(controller,))
    thread.start()
    reference.child(f"users/{username}").delete()
    controller["stop"] = True
    thread.join()
    print("Account has been deleted, thank you for playing !")
    sys.exit()
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa

def settings(username):
    while True:
        clear()
        options_list = ["Preferences", "Account Information", "Return"]
        input_clear()
<<<<<<< HEAD
        playmode = options_list[survey.routines.select('Settings Page ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Preferences":
            preferences(username)
=======
        playmode = survey.routines.select('Settings Page ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0: #Input method is chosen
            clear()
            options_list = [f"{"Auto":<9}| Automatically input keyboard strokes", f"{"Manual":<9}| Collect keyboard strokes and click enter to input"]
            input_clear()
            answer = survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 0:
                allow_auto_keyboard = True
            else:
                allow_auto_keyboard = False
            if username:
                reference.child(f"users/{username}/allow_auto_keyboard").set(allow_auto_keyboard)
        elif playmode == 1: #Input method is chosen
            if not username:
                print("This is only available for logged in users")
                survey.routines.select("",  options = [f"{"Return":<10}| Go back to settings menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                continue
            else:
                account_information = reference.child(f"users/{username}").get()
                print(f"User rank: {account_information["rank"]}")
                print(f"Story progress: {Path(account_information["story_level"]).parts[1]} - {Path(account_information["story_level"]).stem}")
            options_list = ["Change password", "Delete Account", "Return"]
            options_list = [f"{"Change password":<18} | Update password into a new one", f"{"Delete Account":<18}| Remove account forever (Only do this if you are really sure)", f"{"Return":<18}| Return to settings menu"]
            input_clear()
            answer = survey.routines.select("Options: ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 0:
                change_password(username, reference)
            elif answer == 1:
                clear()
                delete_account(username, reference)
            else:
                continue
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
        else:
            break


def starting_menu(reference):
    global allow_auto_keyboard
    global allow_gamepad
    while True:
        clear()
<<<<<<< HEAD
        options_list = ["Login", "Sign up", "Play Locally", "Exit"]
=======
        options_list = [f"{"Login":<14}| All gamemodes will be available and progress will be saved", f"{"Sign up":<14}| Create an account", f"{"Play Locally":<14}| Available gamemodes will be limited and progress won't be saved", f"{"Exit":<14}| Close the game"] if reference != "" else [f"{"Play Locally":<14}| Available gamemodes will be limited and progress won't be saved", f"{"Exit":<14}| Close the game"]
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
        input_clear()
        playmode = options_list[survey.routines.select('Welcome to Shroom Raider! ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == f"{"Login":<14}| All gamemodes will be available and progress will be saved":
            username = login(reference)
            if username != None:
                break
        elif playmode == f"{"Sign up":<14}| Create an account":
            username = signup(reference)
            if username != None:
                break
        elif playmode == f"{"Play Locally":<14}| Available gamemodes will be limited and progress won't be saved":
            username = ""
            options_list = [f"{"Auto":<9}| Automatically input keyboard strokes", f"{"Manual":<9}| Collect keyboard strokes and click enter to input"]
            input_clear()
            answer = survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 0:
                allow_auto_keyboard = True
                options_list = ["Allow gamepad inputs", "Restrict to only keyboards"]
                input_clear()
                answer = options_list[survey.routines.select("Do you want to allow gamepad inputs (only applicable if 'Automatically input keyboard strokes' is on)? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
                if answer == "Allow gamepad inputs":
                    allow_gamepad = True
                else:
                    allow_gamepad = False
            else:
                allow_auto_keyboard = False
            break
        else:
            sys.exit()
    return username

def main_menu(username, reference):
    continue_game = True
    while True:
        clear()
        #options_list = ["Story", "Unlocked Levels", "Ranked Match", "Unranked Match", "Level Leaderboard", "Rank Leaderboard", "Settings", "Return"] 
        #condense "Account Information" to settings, story, unlocked levels, level leaderboard to levels, ranked and unranked and leaderboard (spectate - see map, current moves of each player, time, end of game 
        #find oponent - create room and wait for both players to join and click start for ready other players who join will specate only, find match) to matches
        options_list = ["Levels", "Online Battle", "Settings", "Return"] 
        input_clear()
        playmode = options_list[survey.routines.select(f"Welcome to Shroom Raider, {username}! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Story": #add ending
            if username:
                story_data = story_mode(reference.child(f"users/{username}/story_level").get())
                old_data = reference.child(f"users/{username}/story_data").get()
                if old_data == None:
                    old_data = {}
                new_data = {}
            else:
                story_data = story_mode("levels/spring/stage1.txt")
            if story_data:

                print("Moves done per level:")

                for story_level in story_data:
                    if "/" in story_level:
                        story_level_names = story_level.split("/")
                    else:
                        story_level_names = story_level.split("\\")
                    print(f"{story_level_names[1]} - {story_level_names[2][:-4]}: {story_data[story_level]} moves")
                    if username:
                        new_data[f"{story_level_names[1]} - {story_level_names[2][:-4]}"] = story_data[story_level]

                if username:
                    reference.child(f"users/{username}/story_data").update(old_data | new_data)

                    reference.child(f"users/{username}/story_level").set(next(shroom_level_parser_generator(next(reversed(story_data)))))


                    reference.child(f"users/{username}/story_level").set(shroom_level_parser_generator(next(reversed(story_data))))
                input_clear()
                survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

                reference.child(f"users/{username}/story_level").set(shroom_level_parser_generator(next(reversed(story_data))))

                sys.stdout.flush()
                options_list[survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]

        elif playmode == "Settings":
            settings(username)
        elif playmode == "Unlocked Levels":
            if username:
                unlocked_levels(username, reference)
            else:
                unlocked_levels()
        elif playmode == "Ranked Match": #add time limit
            if not username:
                print("This is only available for logged in users")
                input_clear()
                survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                break
            ...
        elif playmode == "Unranked Match": #add time limit
            if not username:
                print("This is only available for logged in users")
                input_clear()
                survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                break
            else:
                opponent = match(username, reference.child("unranked_match"))
                reference.child("matches").update({ #find match and lobby name
                    "test":{
                        opponent:-2,
                        username:-2
                    }
                })
                level_info, locations = parse_level("levels/temple/stage6.txt") #get random file from edward
                moves_count = gameloop(level_info, locations, moves, output_file)
                reference.child(f"matches/test/{username}").set(moves_count)
                print(f"You finished in {moves_count} moves")
                opponent_moves_count = reference.child(f"matches/test/{opponent}").get()
                if opponent_moves_count == -2:
                    print(f"Waiting for {opponent} to finish", end="")
                    while True:
                        sleep(1.5)
                        print(".", end="")
                        opponent_moves_count = reference.child(f"matches/test/{opponent}").get()
                        if opponent_moves_count != -2:
                            print("")
                            print(f"{opponent} has finished in {opponent_moves_count} moves")
                            break
                        sleep(1.5)
                if moves_count > -1 and moves_count == opponent_moves_count:
                    print(f"You tied with {opponent}")
                    break
                elif  moves_count > -1 and moves_count < opponent_moves_count:
                    print(f"You've defeated {opponent} by {opponent_moves_count - moves_count}")
                    break
                elif moves_count > -1 and moves_count < opponent_moves_count:
                    print(f"You've lost to {opponent} by {moves_count - opponent_moves_count}")
                    break
                else:
                    print(f"You didn't finish, automatically lost")
        elif playmode == "Return":
            continue_game = False
            break
    return continue_game

def get_value(item):
    return item[1]

def level_leaderboard(username = "", reference = ""):
    clear()
    if username:
        leaderboard_data = reference.child(f"level_leaderboard").get()
        while True:
            clear()
            options_list = [level for level in leaderboard_data] + ["Return to main menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select(f"Choose from the following levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            clear()
            if chosen_level == "Return to main menu":
                break
            leaderboard = dict(sorted(leaderboard_data[chosen_level].items(), key = get_value))
            print(f"Moves Leaderboard for {chosen_level}")
            count = 0
            for user in leaderboard:
                count += 1
                print(f"{count}: {user} with {leaderboard[user]} moves" + ("(you)" if user == username else ""))
                if count > 10:
                    break
            options_list = [f"{"Choose Level":<15}| Check leaderboard of a different level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = survey.routines.select("",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1:
                break
    else:
        print("This is only available for logged in users")
        survey.routines.select("",  options = [f"{"Return":<10}| Go back to levels menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def rank_leaderboard(username, reference):
    clear()
    leaderboard_data = reference.child(f"rank_leaderboard").get()
    leaderboard = dict(sorted(leaderboard_data.items(), key = get_value, reverse = True))
    print(f"Highest Ranks")
    count = 0
    for user in leaderboard:
        count += 1
        print(f"{count}: {user} with {leaderboard[user]} points" + ("(you)" if user == username else ""))
        if count > 10:
            break
    input_clear()
    survey.routines.select("",  options = [f"{"Return":<10}| Go back to online battle menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def endless_mode():
    call = generate_map(limit=1)
    while True:
        
        level_info, locations = parse_level(call)
        try:
            moves_count = gameloop(level_info, locations, moves, output_file)
        finally:
            keyboard.unhook_all()

        if type(moves_count) is str:
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Skip":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = survey.routines.select("Laro gave up! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            
            if answer == 1:
                call = generate_map()
            elif answer == 2:
                break

        elif moves_count == -1:
            options_list = [f"{"Try again":<15}| Restart the map and play again",f"{"Skip":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = survey.routines.select("You died! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            
            if answer == 1:
                call = generate_map()
            elif answer == 2:
                break

        else:
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Next Level":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
            input_clear()
            answer = options_list[survey.routines.select(f"You've beaten the level with {moves_count} moves!. " if not username else "",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            
            if answer == 1:
                call = generate_map()
            elif answer == 2:
                break

def levels_mode(username, reference):
    while True:
        clear()
        options_list = [f"{"Story":<20}| Play through the storyline of Laro's adventure", f"{"Endless Mode":<20}| Keep playing through randomly generated maps", f"{"Unlocked Levels":<20}| Choose from the story levels that you've played through or all (if playing locally)", f"{"Level Leaderboard":<20}| See the top ranking players per level", f"{"Return":<20}| Go back to main menu"]       
        input_clear()
<<<<<<< HEAD
        playmode = options_list[survey.routines.select(f"Levels Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Story":
=======
        playmode = survey.routines.select("Levels Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0:
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            if username:
                story_data = story_mode(reference.child(f"users/{username}/story_level").get())
                old_data = reference.child(f"users/{username}/story_data").get()
                if old_data == None:
                    old_data = {}
                new_data = {}
            else:
                story_data = story_mode("levels/spring/stage1.txt")
            if story_data:
                print("Moves done per level:")
                for story_level in story_data:
                    if "/" in story_level:
                        story_level_names = story_level.split("/")
                    else:
                        story_level_names = story_level.split("\\")
                    print(f"{story_level_names[1]} - {story_level_names[2][:-4]}: {story_data[story_level]} moves")
                    if username:
                        new_data[f"{story_level_names[1]} - {story_level_names[2][:-4]}"] = story_data[story_level]
                        reference.child(f"level_leaderboard/{story_level_names[1]} - {story_level_names[2][:-4]}/{username}").set(story_data[story_level])
                if username:
                    reference.child(f"users/{username}/story_data").update(old_data | new_data)
                    reference.child(f"users/{username}/story_level").set(next(shroom_level_parser_generator(next(reversed(story_data)))))
                    
                input_clear()
                survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        elif playmode == 1:
            endless_mode()
        elif playmode == 2:
            if username:
                unlocked_levels(username, reference)
            else:
                unlocked_levels()
        elif playmode == 3:
            if username:
                level_leaderboard(username, reference)
            else:
                level_leaderboard()
        else:
            break

def online_battle_mode(username, reference):
    while True:
        clear()
        options_list = [f"{"Ranked Match":<20}| Competitively play against other users", f"{"Unranked Match":<20}| Casually play against other users", f"{"Rank Leaderboard":<20}| See the top ranking players", f"{"Return":<20}| Go back to main menu"]
        input_clear()
<<<<<<< HEAD
        playmode = options_list[survey.routines.select(f"Online Battle Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Ranked Match": #add time limit
=======
        playmode = survey.routines.select("Online Battle Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0: 
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            room, opponent = find_match(username, reference.child("ranked_match"))

            match_result, rank_score = match(username, reference.child("ranked_match"), room, opponent, "ranked")

            old_rank = reference.child(f"users/{username}/rank").get()
            new_rank = max(old_rank + rank_score, 1000)
            reference.child(f"users/{username}/rank").set(new_rank)
            reference.child(f"rank_leaderboard/{username}").set(new_rank)
            input_clear()
            print(match_result)
            survey.routines.select(f"Old rank: {old_rank}, New rank: {new_rank}",  options = ["Continue"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        elif playmode == 1:
            room, opponent = find_match(username, reference.child("unranked_match"))

            match_result = match(username, reference.child("unranked_match"), room, opponent, "unranked")

            input_clear()
            survey.routines.select(match_result + " ",  options = ["Continue"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        elif playmode == 2:
            rank_leaderboard(username, reference)
        else:
            break

def main_menu(username, reference):
    continue_game = True
    while True:
        clear()
        options_list = [f"{"Levels":<15}| Play through preset levels or the endless mode", f"{"Online Battle":<15}| Compete agains other players online", f"{"Settings":<15}| Change how the game takes input or see account details", f"{"Return":<15}| Go back to starting screen"] 
        input_clear()
        playmode = survey.routines.select(f"Welcome to Shroom Raider, {username}! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0:
            levels_mode(username,reference)
        elif playmode == 1:
            if not username:
                print("This is only available for logged in users")
                input_clear()
                survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            else:
                online_battle_mode(username,reference)
<<<<<<< HEAD
        elif playmode == "Settings":
            settings(username)
        elif playmode == "Return to Login":
=======
        elif playmode == 2:
            settings(username, reference)
        elif playmode == 3:
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            continue_game = False
            break
    return continue_game

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "uhm")
    parser.add_argument("-f", type = str, dest="stage_file")
    parser.add_argument("-m", type = str, dest="string_of_moves")
    parser.add_argument("-o", type = str, dest="output_file")
    system_input = parser.parse_args()
    moves = system_input.string_of_moves
    output_file = system_input.output_file

    global allow_auto_keyboard

    if output_file and not moves:
        print("Use -m to input your moves")
        sys.exit(1)
    if output_file or moves or system_input.stage_file:
        level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/spring/stage1.txt")
        allow_auto_keyboard = False
        gameloop(level_info, locations, moves, output_file)
    else:
<<<<<<< HEAD
        try:
=======
        
        if connected_to_internet():
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            cred = credentials.Certificate("utils/private_key.json")
            firebase_admin.initialize_app(cred, {"databaseURL":"https://shroomraider-70f6a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
            reference = db.reference("/")
        except:
            reference = ""

        username = starting_menu(reference)

        while True:
            if not main_menu(username, reference):
                username = starting_menu(reference)
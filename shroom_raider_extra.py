import colorama
import socket
from colorama import Fore, Style
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement_extra import user_input
from utils.ui import show_screen
from utils.game_progress import shroom_level_parser_generator
from time import sleep
from copy import deepcopy
from pathlib import Path
import sys
import argparse
from firebase_admin import credentials, db, initialize_app
import pwinput
import survey
import os
import keyboard

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
        
global allow_auto_keyboard

def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def login(reference):
    print("Loading data...")
    users = reference.child("users").get()
    while True:
        clear()
        username = input("Enter Username: ")
        password = pwinput.pwinput(prompt="Enter your password: ", mask="*")
        if username not in users or reference.child(f"users/{username}/password").get() != password:
            options_list = ["Try again", "Return"]
            input_clear()
            answer = options_list[survey.routines.select('Incorrect Username or Password ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                return None
        else:
            global allow_auto_keyboard
            allow_auto_keyboard = reference.child(f"users/{username}/allow_auto_keyboard").get()
            return username

def signup(reference):
    global allow_auto_keyboard
    print("Loading data...")
    users = reference.child("users").get()
    while True:
        while True:
            clear()
            username = input("Enter Username: ")
            if username not in users:
                break
            options_list = ["Try again", "Return"]
            input_clear()
            answer = options_list[survey.routines.select("Username already taken",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                return None
        while True:
            password = pwinput.pwinput(prompt="Enter your password: ", mask="*")
            confirmpassword = pwinput.pwinput(prompt="Reenter your password: ", mask="*")
            if len(password) < 7 or password != confirmpassword:
                options_list = ["Try again", "Return"]
                input_clear()
                answer = options_list[survey.routines.select("Password must atleast be 8 characters long! " if len(password) < 7 else "Password mismatched! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
                if answer == "Return":
                    return None
                clear()
                print("Enter Username: " + username)
            else:
                clear()
                print("Account has been created")
                options_list = ["Automatically input keyboard strokes", "Collect keyboard strokes and click enter to input"]
                input_clear()
                answer = options_list[survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
                if answer == "Automatically input keyboard strokes":
                    allow_auto_keyboard = True
                else:
                    allow_auto_keyboard = False
                reference.child("users").update({
                    username:{
                        "password": password,
                        "rank": 1000,
                        "story_level": "levels/spring/stage1.txt",
                        "allow_auto_keyboard": allow_auto_keyboard,
                        }
                    }
                )
                return username
                
def gameloop(level_info, locations, moves = "", output_file = ""):
    clear()
    colorama.init(autoreset=True)

    original_level_info = deepcopy(level_info)
    original_locations = deepcopy(locations)

    moves_count = 0

    if output_file:
        has_clear = "NO CLEAR"
    else:
        show_screen(level_info, locations)
    if allow_auto_keyboard:
        print(Fore.RED + Style.BRIGHT + "WARNING: All keyboard inputs have been disabled except valid inputs")
        print(Fore.RED + Style.BRIGHT + "-> This applies to all processes of the computer\n-> Click 'e' to exit the stage and unlock all keyboard inputs\n")
        print("What will you do?")
        def key_check(event):
            allowed_keys = {"w", "a", "s", "d", "e", "!", "p", "W", "A", "S", "D", "E", "P"}
            if event.name in allowed_keys:
                return True  
            else:
                return False
        keyboard.hook(key_check, suppress=True)
    while True:
        if moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, moves)
            moves = ""
        elif not allow_auto_keyboard:
            actions = user_input(level_info, locations, original_locations, original_level_info)
        else:
            keyboard_input = keyboard.read_key() 
            input_clear()    
            actions = user_input(level_info, locations, original_locations, original_level_info, keyboard_input)
        for current_locations, current_level_info in actions:
            if not (current_locations and current_level_info):
                sleep(0.1)
                return "exit"
            if current_level_info["invalid_input"]:
                if not output_file:
                    sleep(0.1)
                    show_screen(level_info, locations)
                    print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                break
            else:
                moves_count += 1
                
            level_info = current_level_info
            locations = current_locations 

            if level_info["level_reset"]:
                moves_count = 0

            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    clear()
                    show_screen(level_info, locations)
                    sleep(0.15)
                break
            elif level_info["game_end"]:
                if not output_file:
                    clear()
                    show_screen(level_info, locations)
                    moves_count = -1
                    sleep(0.15)
                break
            elif not output_file:
                show_screen(level_info, locations)
                sleep(0.15)
        
        if output_file:
            parse_output(output_file, locations, level_info, has_clear)
            break
        elif level_info["game_end"]:
            break
    try:
        del actions
        del level_info
        del locations
        del original_level_info
        del original_locations
    finally:
        keyboard.unhook_all()
    return moves_count

def story_mode(story_progress):
    output = {}
    while True:
        level_info, locations = parse_level(story_progress)
        try:
            moves_count = gameloop(level_info, locations, moves, output_file)
        finally:
            keyboard.unhook_all()
        if type(moves_count)is str:
            options_list = ["Try again", "Return to main menu"]
            input_clear()
            answer = options_list[survey.routines.select("You gave up! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return to main menu":
                break
        elif moves_count == -1:
            options_list = ["Try again", "Return to main menu"]
            input_clear()
            answer = options_list[survey.routines.select("You died! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return to main menu":
                break
        else:
            output[story_progress] = moves_count
            options_list = ["Next Level", "Return to main menu"]
            input_clear()
            answer = options_list[survey.routines.select(f"You've beaten the level with {moves_count} moves!. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return to main menu":
                break
            else:
                story_progress = next(shroom_level_parser_generator(story_progress))
    return output

def unlocked_levels(username = "", reference = ""):
    try_again = False
    while True:
        if try_again:
            try_again = False
        else:
            if username:
                input_clear()
                options_list = [level for level in reference.child(f"users/{username}/story_data").get()] + ["Return to main menu"]
                if not options_list:
                    print("Play through the \"Story\" mode to unlock levels")
            else:
                print("Currently playing locally, progress won't be saved")
                options_list = ["spring - stage1"] + [Path(level).parts[1] + " - " + Path(level).stem for level in shroom_level_parser_generator()] + ["Return to main menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select("Choose from the following unlocked levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if chosen_level == "Return to main menu":
                break
        
        chosen_level_path = f"levels/{chosen_level.split(" - ")[0]}/{chosen_level.split(" - ")[1]}.txt"
        level_info, locations = parse_level(chosen_level_path)
        try:
            moves_count = gameloop(level_info, locations, moves, output_file)
        finally:
            keyboard.unhook_all()

        if type(moves_count) is str:
            options_list = ["Try again", "Choose level", "Return to main menu"]
            input_clear()
            answer = options_list[survey.routines.select("Laro gave up! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            
            if answer == "Try again":
                try_again = True
            elif answer == "Return to main menu":
                break

        elif moves_count == -1:
            options_list = ["Try again", "Choose level", "Return to main menu"]
            input_clear()
            answer = options_list[survey.routines.select("You died! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            
            if answer == "Try again":
                try_again = True
            elif answer == "Return to main menu":
                break

        else:
            if username:
                print(f"Current moves: {moves_count}, Previous moves: {reference.child(f"users/{username}/story_data/{chosen_level}").get()}")
                
                options_list = ["Yes, keep it", "No, don't keep it"]
                input_clear()
                answer = options_list[survey.routines.select(f"You've beaten the level with {moves_count} moves!. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
                
                if answer == "Yes, keep it":
                    reference.child(f"users/{username}/story_data/{chosen_level}").set(moves_count)
                    reference.child(f"level_leaderboard/{chosen_level}/{username}").set(moves_count)
            options_list = ["Try again", "Choose next level", "Return to main menu"]
            input_clear()
            answer = options_list[survey.routines.select(f"You've beaten the level with {moves_count} moves!. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            
            if answer == "Try again":
                try_again = True
            elif answer == "Return to main menu":
                break
    return

def find_match(username, reference): 
    print("Finding an opponent", end="")
    waiting_for_opponent = False
    while True:
        sleep(1.5)
        print(".", end="")
        if not waiting_for_opponent:
            if reference.get():
                available_rooms = reference.get()
                for room in available_rooms:
                    if len(available_rooms[room]) < 2: #found an available room
                        opponent = room
                        reference.child(f"{room}/{username}").set(-2)
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
                print("")
                print(f"Opponent found: {opponent}")
                sleep(1.5)
                break
    return (room, opponent)

def match(username, reference, room, opponent, gamemode):
    level_info, locations = parse_level("levels/spring/stage1.txt") #get random file from edward
    try:
        moves_count = gameloop(level_info, locations, moves, output_file)
    finally:
        keyboard.unhook_all()
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
        match_result = "You didn't finish, automatically lost"
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

def change_password(username, reference):
    old_password = reference.child(f"users/{username}/password").get()
    while True:
        clear()
        password = pwinput.pwinput(prompt="Enter your password: ", mask="*")
        confirmpassword = pwinput.pwinput(prompt="Reenter your password: ", mask="*")
        if old_password == password:
            options_list = ["Try again", "Return"]
            input_clear()
            answer = options_list[survey.routines.select("Entered password is same as old one ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                return
        elif len(password) < 7 or password != confirmpassword:
            options_list = ["Try again", "Return"]
            input_clear()
            answer = options_list[survey.routines.select("Password must atleast be 8 characters long! " if len(password) < 7 else "Password mismatched! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                return None
        else:
            reference.child(f"users/{username}/password").set(password)
            survey.routines.select("New password has been set ",  options = ["Return"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def delete_account(username, reference):
    count = 0
    while count < 4:
        options_list = ["Yes, Delete", "Return"]
        input_clear()
        answer = options_list[survey.routines.select(f"Are you {"really "*count}sure? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if answer == "Return":
            return None
        count += 1
    reference.child(f"users/{username}").delete()
    print("Account has been deleted, thank you for playing !")
    sys.exit()

def settings(username, reference):
    global allow_auto_keyboard
    while True:
        clear()
        options_list = [f"{"Input Method":<20}| Change how the game handles keyboard input", f"{"Account Information":<20}| See story progress, change password, or delete account", f"{"Return":<20}| Go back to main menu"]
        input_clear()
        playmode = survey.routines.select('Settings Page ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0: #Input method is chosen
            clear()
            options_list = ["Automatically input keyboard strokes", "Collect keyboard strokes and click enter to input"]
            input_clear()
            answer = options_list[survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Automatically input keyboard strokes":
                allow_auto_keyboard = True
            else:
                allow_auto_keyboard = False
            if username:
                reference.child(f"users/{username}/allow_auto_keyboard").set(allow_auto_keyboard)
        elif playmode == 1: #Input method is chosen
            if not username:
                print("This is only available for logged in users")
                survey.routines.select("",  options = ["Return"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                continue
            else:
                account_information = reference.child(f"users/{username}").get()
                print(f"User rank: {account_information["rank"]}")
                print(f"Story progress: {Path(account_information["story_level"]).parts[1]} - {Path(account_information["story_level"]).stem}")
            options_list = ["Change password", "Delete Account", "Return"]
            input_clear()
            answer = options_list[survey.routines.select("Options: ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Change password":
                change_password(username, reference)
            elif answer == "Delete Account":
                clear()
                delete_account(username, reference)
            else:
                continue
        else:
            break

def starting_menu(reference):
    global allow_auto_keyboard
    while True:
        clear()
        options_list = ["Login", "Sign up", "Play Locally", "Exit"] if reference != "" else ["Play Locally", "Exit"]
        input_clear()
        playmode = options_list[survey.routines.select('Welcome to Shroom Raider! ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Login":
            username = login(reference)
            if username:
                break
        elif playmode == "Sign up":
            username = signup(reference)
            if username:
                break
        elif playmode == "Play Locally":
            username = ""
            options_list = ["Automatically input keyboard strokes", "Collect keyboard strokes and click enter to input"]
            input_clear()
            answer = options_list[survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Automatically input keyboard strokes":
                allow_auto_keyboard = True
            else:
                allow_auto_keyboard = False
            break
        else:
            sys.exit()
    return username

def get_value(item):
    return item[1]

def level_leaderboard(username = "", reference = ""):
    clear()
    if username:
        leaderboard_data = reference.child("level_leaderboard").get()
        while True:
            clear()
            options_list = [level for level in leaderboard_data] + ["Return to main menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select("Choose from the following levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
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
            options_list = ["Choose other level", "Return"]
            input_clear()
            answer = options_list[survey.routines.select("",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Return":
                break
    else:
        print("This is only available for logged in users")
        survey.routines.select("",  options = ["Return"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def rank_leaderboard(username, reference):
    clear()
    leaderboard_data = reference.child("rank_leaderboard").get()
    leaderboard = dict(sorted(leaderboard_data.items(), key = get_value, reverse = True))
    print("Highest Ranks")
    count = 0
    for user in leaderboard:
        count += 1
        print(f"{count}: {user} with {leaderboard[user]} points" + ("(you)" if user == username else ""))
        if count > 10:
            break
    input_clear()
    survey.routines.select("",  options = ["Return"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def levels_mode(username, reference):
    while True:
        clear()
        options_list = ["Story", "Endless Mode", "Unlocked Levels", "Level Leaderboard", "Return"] 
        input_clear()
        playmode = options_list[survey.routines.select("Levels Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Story":
            if username:
                story_data = story_mode(reference.child(f"users/{username}/story_level").get())
                old_data = reference.child(f"users/{username}/story_data").get()
                if old_data is None:
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
        if playmode == "Unlocked Levels":
            if username:
                unlocked_levels(username, reference)
            else:
                unlocked_levels()
        elif playmode == "Level Leaderboard":
            if username:
                level_leaderboard(username, reference)
            else:
                level_leaderboard()
        else:
            break

def online_battle_mode(username, reference):
    while True:
        clear()
        options_list = ["Ranked Match", "Unranked Match", "Rank Leaderboard", "Return"] 
        input_clear()
        playmode = options_list[survey.routines.select("Online Battle Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Ranked Match": #add time limit
            room, opponent = find_match(username, reference.child("ranked_match"))

            match_result, rank_score = match(username, reference.child("ranked_match"), room, opponent, "ranked")

            old_rank = reference.child(f"users/{username}/rank").get()
            new_rank = max(old_rank + rank_score, 1000)
            reference.child(f"users/{username}/rank").set(new_rank)
            reference.child(f"rank_leaderboard/{username}").set(new_rank)
            input_clear()
            print(match_result)
            survey.routines.select(f"Old rank: {old_rank}, New rank: {new_rank}",  options = ["Continue"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        elif playmode == "Unranked Match":
            room, opponent = find_match(username, reference.child("unranked_match"))

            match_result = match(username, reference.child("unranked_match"), room, opponent, "unranked")

            input_clear()
            survey.routines.select(match_result + " ",  options = ["Continue"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        elif playmode == "Rank Leaderboard":
            rank_leaderboard(username, reference)
        else:
            break

def main_menu(username, reference):
    continue_game = True
    while True:
        clear()
        options_list = ["Levels", "Online Battle", "Settings", "Return to Login"] 
        input_clear()
        playmode = options_list[survey.routines.select(f"Welcome to Shroom Raider, {username}! ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Levels":
            levels_mode(username,reference)
        elif playmode == "Online Battle":
            if not username:
                print("This is only available for logged in users")
                input_clear()
                survey.routines.select(" ",  options = ["Return to main menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            else:
                online_battle_mode(username,reference)
        elif playmode == "Settings":
            settings(username, reference)
        elif playmode == "Return to Login":
            continue_game = False
            break
    return continue_game

def connected_to_internet():
    try:
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            print('Clossing socket')
            sock.close
        return True
    except OSError:
        pass
    return False

if __name__ == "__main__":
    # Initialize the parser for system input arguments
    parser = argparse.ArgumentParser(description = "Shroom Raider with Bonus Features")
    parser.add_argument("-f", type = str, dest="stage_file")
    parser.add_argument("-m", type = str, dest="string_of_moves")
    parser.add_argument("-o", type = str, dest="output_file")
    system_input = parser.parse_args()

    
    moves = system_input.string_of_moves
    output_file = system_input.output_file

    if output_file and not moves:
        print("Use -m to input your moves")
        sys.exit(1)
    if output_file or moves or system_input.stage_file:
        level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/spring/stage1.txt")
        allow_auto_keyboard = False
        gameloop(level_info, locations, moves, output_file)
    else:
        if connected_to_internet():
            cred = credentials.Certificate("utils/private_key.json")
            initialize_app(cred, {"databaseURL":"https://shroomraider-70f6a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
            reference = db.reference("/")
        else: 
            clear()
            print(Fore.RED + Style.BRIGHT + "Failed initiating a connection with Firebase. \nMake sure that you are connected to the internet \nand the private_key.json file is in the utils folder before running ")
            reference = ""
            options_list = [f"{"Continue":<10}| Only the 'Play Locally' option will be available)", f"{"Exit":<10}| Close the game"]
            input_clear()
            answer = survey.routines.select("\r",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 1: #Exit is chosen
                sys.exit()

        username = starting_menu(reference)

        while True:
            if not main_menu(username, reference):
                username = starting_menu(reference)
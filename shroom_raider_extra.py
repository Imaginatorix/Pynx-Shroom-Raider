import colorama
import socket
import pwinput
import survey
import os
import keyboard
import sys
import argparse
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement_extra import user_input
from utils.ui import show_screen
from utils.game_progress import shroom_level_parser_generator
from colorama import Fore, Style
from firebase_admin import credentials, db, initialize_app
from itertools import cycle
from threading import Thread
from time import sleep
from copy import deepcopy
from pathlib import Path

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

def spinner(controller, text="Loading"):
    frames = cycle(["|", "/", "-", "\\"])
    clear()
    while not controller["stop"]:
        sys.stdout.write(f"\r{text} {next(frames)}")
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write("\r")  # clear
    sys.stdout.flush()

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

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
            controller = {"stop": False}
            thread = Thread(target=spinner, args=(controller,))
            thread.start()
            allow_auto_keyboard = reference.child(f"users/{username}/allow_auto_keyboard").get()
            controller["stop"] = True
            thread.join()
            return username

def signup(reference):
    global allow_auto_keyboard
    controller = {"stop": False}
    thread = Thread(target=spinner, args=(controller,))
    thread.start()
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
                clear()
                print("Account has been created")
                options_list = [f"{"Auto":<9}| Automatically input keyboard strokes", f"{"Manual":<9}| Collect keyboard strokes and click enter to input"]
                input_clear()
                answer = survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
                if answer == 1:
                    allow_auto_keyboard = True
                else:
                    allow_auto_keyboard = False
                controller = {"stop": False}
                thread = Thread(target=spinner, args=(controller,))
                thread.start()
                reference.child("users").update({
                    username:{
                        "password": password,
                        "rank": 1000,
                        "story_level": "levels/spring/stage1.txt",
                        "allow_auto_keyboard": allow_auto_keyboard,
                        }
                    }
                )
                controller["stop"] = True
                thread.join()
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
        if output_file and not moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, " ")
            moves = ""
        elif moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, moves)
            moves = ""
        elif not allow_auto_keyboard:
            actions = user_input(level_info, locations, original_locations, original_level_info)
        else:
            keyboard_input = keyboard.read_key() 
            input_clear()    
            actions = user_input(level_info, locations, original_locations, original_level_info, keyboard_input)
        for current_locations, current_level_info in actions:
            level_info = current_level_info
            locations = current_locations 

            if not (current_locations and current_level_info):
                sleep(0.1)
                return "exit"
            
            if not output_file:
                show_screen(level_info, locations)
                sleep(0.15)

            if level_info["invalid_input"] and not output_file:
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
            else:
                moves_count += 1
                
            if level_info["level_reset"]:
                moves_count = 0

            if level_info["game_end"] and level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    clear()
                    show_screen(level_info, locations)
                break
            elif level_info["game_end"]:
                if not output_file:
                    clear()
                    show_screen(level_info, locations)
                    moves_count = -1
                break
        
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
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Return":<15}| Go back to levels menu"]
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
                options_list = ["spring - stage1"] + [Path(level).parts[1] + " - " + Path(level).stem for level in shroom_level_parser_generator()] + ["Return to levels menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select("Choose from the following unlocked levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if chosen_level == "Return to levels menu":
                break

        chosen_level_path = f"levels/{chosen_level.split(" - ")[0]}/{chosen_level.split(" - ")[1]}.txt"
        level_info, locations = parse_level(chosen_level_path)
        try:
            moves_count = gameloop(level_info, locations, moves, output_file)
        finally:
            keyboard.unhook_all()

        if type(moves_count) is str:
            options_list = [f"{"Try again":<15}| Restart the map and play again",f"{"Choose Level":<15}| Play a different level", f"{"Return":<15}| Go back to levels menu"]
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
            options_list = [f"{"Try again":<15}| Restart the map and play again", f"{"Choose Level":<15}| Play a different level", f"{"Return":<15}| Go back to main menu"]
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

def settings(username, reference):
    global allow_auto_keyboard
    while True:
        clear()
        options_list = [f"{"Input Method":<20}| Change how the game handles keyboard input", f"{"Account Information":<20}| See story progress, change password, or delete account", f"{"Return":<20}| Go back to main menu"]
        input_clear()
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
        else:
            break

def starting_menu(reference):
    global allow_auto_keyboard
    while True:
        clear()
        options_list = [f"{"Login":<14}| All gamemodes will be available and progress will be saved", f"{"Sign up":<14}| Create an account", f"{"Play Locally":<14}| Available gamemodes will be limited and progress won't be saved", f"{"Exit":<14}| Close the game"] if reference != "" else [f"{"Play Locally":<14}| Available gamemodes will be limited and progress won't be saved", f"{"Exit":<14}| Close the game"]
        input_clear()
        playmode = options_list[survey.routines.select('Welcome to Shroom Raider! ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == f"{"Login":<14}| All gamemodes will be available and progress will be saved":
            username = login(reference)
            if username:
                break
        elif playmode == f"{"Sign up":<14}| Create an account":
            username = signup(reference)
            if username:
                break
        elif playmode == f"{"Play Locally":<14}| Available gamemodes will be limited and progress won't be saved":
            username = ""
            options_list = [f"{"Auto":<9}| Automatically input keyboard strokes", f"{"Manual":<9}| Collect keyboard strokes and click enter to input"]
            input_clear()
            answer = survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
            if answer == 0:
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
    survey.routines.select("",  options = [f"{"Return":<10}| Go back to online battle menu"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def levels_mode(username, reference):
    while True:
        clear()
        options_list = [f"{"Story":<20}| Play through the storyline of Laro's adventure", f"{"Endless Mode":<20}| Keep playing through randomly generated maps", f"{"Unlocked Levels":<20}| Choose from the story levels that you've played through or all (if playing locally)", f"{"Level Leaderboard":<20}| See the top ranking players per level", f"{"Return":<20}| Go back to main menu"]       
        input_clear()
        playmode = survey.routines.select("Levels Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0:
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
        if playmode == 2:
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
        playmode = survey.routines.select("Online Battle Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))
        if playmode == 0: 
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
        elif playmode == 2:
            settings(username, reference)
        elif playmode == 3:
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

    global allow_auto_keyboard

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
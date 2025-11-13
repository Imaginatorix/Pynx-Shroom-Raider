import colorama
from colorama import Fore, Style
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement_extra import user_input, keyboard_tracker
from utils.ui import show_screen
from utils.game_progress import shroom_level_parser_generator
from time import sleep
from copy import deepcopy
import sys
import argparse
import firebase_admin
from firebase_admin import credentials, db
import pwinput
import survey
import os

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
global allow_gamepad

def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

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
            global allow_gamepad

            allow_auto_keyboard = reference.child(f"users/{username}/allow_auto_keyboard").get()
            allow_gamepad = reference.child(f"users/{username}/allow_gamepad").get()
            return username

def signup(reference):
    global allow_auto_keyboard
    global allow_gamepad
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
                options_list = ["Automatically input keyboard strokes", "Collect keyboard strokes and click enter to input"]
                input_clear()
                answer = options_list[survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
                if answer == "Automatically input keyboard strokes":
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
                    allow_gamepad = False
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
                return username
                
def gameloop(level_info, locations, moves = "", output_file = ""):
    colorama.init(autoreset=True)

    original_level_info = deepcopy(level_info)
    original_locations = deepcopy(locations)

    moves_count = 0

    if output_file:
        has_clear = "NO CLEAR"
    else:
        show_screen(level_info, locations)
    while True:
        if moves:
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
            if not (current_locations and current_level_info):
                return "exit"
            if current_level_info["invalid_input"]:
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                break
            else:
                moves_count += 1
            level_info = current_level_info
            locations = current_locations 

            if (level_info, locations) ==  (original_level_info, original_locations): #fix, still primative make a reset method
                moves_count = 0
                continue

            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You got all mushrooms!")
                break
            elif level_info["game_end"]:
                if not output_file:
                    print(Fore.RED + Style.BRIGHT + "You drowned!")
                    moves_count = -1
                break
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
        moves_count = gameloop(level_info, locations, moves, output_file)
        if type(moves_count) == str:
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
                options_list = ["spring - stage1"] + [level.split("\\")[1] + " - " + level.split("\\")[2][:-4] for level in shroom_level_parser_generator()] + ["Return to main menu"]
            input_clear()
            chosen_level = options_list[survey.routines.select(f"Choose from the following unlocked levels. ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if chosen_level == "Return to main menu":
                break
        
        chosen_level_path = f"levels/{chosen_level.split(" - ")[0]}/{chosen_level.split(" - ")[1]}.txt"
        level_info, locations = parse_level(chosen_level_path)
        moves_count = gameloop(level_info, locations, moves, output_file)

        if type(moves_count) == str:
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


def settings(username):
    while True:
        clear()
        options_list = ["Preferences", "Account Information", "Return"]
        input_clear()
        playmode = options_list[survey.routines.select('Settings Page ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Preferences":
            preferences(username)
        else:
            break


def starting_menu(reference):
    global allow_auto_keyboard
    global allow_gamepad
    while True:
        clear()
        options_list = ["Login", "Sign up", "Play Locally", "Exit"]
        input_clear()
        playmode = options_list[survey.routines.select('Welcome to Shroom Raider! ',  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Login":
            username = login(reference)
            if username != None:
                break
        elif playmode == "Sign up":
            username = signup(reference)
            if username != None:
                break
        elif playmode == "Play Locally":
            username = ""
            options_list = ["Automatically input keyboard strokes", "Collect keyboard strokes and click enter to input"]
            input_clear()
            answer = options_list[survey.routines.select("How do you want to input moves? ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
            if answer == "Automatically input keyboard strokes":
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


                    reference.child(f"users/{username}/story_level").set(shroom_level_parser_gee(next(reversed(story_data))))
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
    survey.routines.select("",  options = ["Return"],  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))

def levels_mode(username, reference):
    while True:
        clear()
        options_list = ["Story", "Endless Mode", "Unlocked Levels", "Level Leaderboard", "Return"] 
        input_clear()
        playmode = options_list[survey.routines.select(f"Levels Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
        if playmode == "Story":
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
        playmode = options_list[survey.routines.select(f"Online Battle Mode ",  options = options_list,  focus_mark = '> ',  evade_color = survey.colors.basic('yellow'))]
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
            settings(username)
        elif playmode == "Return to Login":
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

    if output_file and not moves:
        print("Use -m to input your moves")
        sys.exit(1)
    if output_file or moves or system_input.stage_file:
        level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/spring/stage1.txt")
        allow_auto_keyboard = False
        gameloop(level_info, locations, moves, output_file)
    else:
        try:
            cred = credentials.Certificate("utils/private_key.json")
            firebase_admin.initialize_app(cred, {"databaseURL":"https://shroomraider-70f6a-default-rtdb.asia-southeast1.firebasedatabase.app/"})
            reference = db.reference("/")
        except:
            reference = ""

        username = starting_menu(reference)

        while True:
            if not main_menu(username, reference):
                username = starting_menu(reference)
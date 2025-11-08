#import level size and origloc
#Level Map
import colorama
from colorama import Fore, Back, Style
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement import user_input
from utils.ui import show_screen
from time import sleep
from copy import deepcopy
import sys

colorama.init(autoreset=True)

if __name__ == "__main__": #reformat
    if len(sys.argv) < 2:
        level_info, locations = parse_level(f"levels/summer/stage5.txt")
    else:
        command = ""
        has_own_level = False
        for argument in sys.argv[1:]:
            if argument in ("-f","-m", "-o"):
                command = argument
                continue
            if command == "-f":
                level_info, locations = parse_level(argument)
                has_own_level = True
            elif command == "-m":
                sys_actions = argument
            elif command == "-o":
                output_file = argument
            else:
                if has_own_level:
                    print("here")
                    continue
                print(argument)
                print("Invalid input. Try again.")
                sys.exit()

original_level_info = deepcopy(level_info)
original_locations = deepcopy(locations)

while True:
    if len(sys.argv) > 3:
        actions = user_input(level_info, locations, original_locations, original_level_info, sys_actions)
        has_clear = "NO CLEAR"
    else:
        show_screen(level_info, locations)
        actions = user_input(level_info, locations, original_locations, original_level_info)
    if not actions:
        show_screen(level_info, locations)
        print("Invalid input. Try again.")
    else:
        for current_locations, current_level_info in actions: #fix this
            if current_level_info["invalid_input"]:
                show_screen(level_info, locations)
                print("Invalid input detected")
                break
            elif current_level_info["game_lost"]:
                show_screen(level_info, locations)
                if len(sys.argv) <= 3:
                    print(Fore.RED + Style.BRIGHT + "You've lost!")
            level_info = current_level_info
            locations = current_locations
            if locations["L"][0] in locations["+"]:
                locations["+"].remove(locations["L"][0])
                level_info["mushroom_collected"] += 1
            if len(sys.argv) <= 3:
                sleep(0.1)
                show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if len(sys.argv) > 3:
                    has_clear = "CLEAR"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You've won!")
                    level_info["game_won"] = True
                break
    if len(sys.argv) > 3:
        parse_output(output_file, locations, level_info, has_clear)
        break
    if level_info["game_won"] or level_info["game_lost"]:
        if len(sys.argv) <= 3:
            print(Style.BRIGHT + "Game ended!")
        break
        

#to be added: item and environment interactions
#change logic by splitting inputs into individual characters, check first if valid
#TODO: change name, add testing and fix rocks
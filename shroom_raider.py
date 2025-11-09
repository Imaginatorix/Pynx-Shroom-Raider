import colorama
from colorama import Fore, Back, Style
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement import user_input
from utils.ui import show_screen
from time import sleep
from copy import deepcopy
import sys
import argparse

if __name__ == "__main__":
    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser(description = "uhm")
    parser.add_argument("-f", type = str, dest="stage_file")
    parser.add_argument("-m", type = str, dest="string_of_moves")
    parser.add_argument("-o", type = str, dest="output_file")
    system_input = parser.parse_args()

    level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/spring/stage5.txt")
    moves = system_input.string_of_moves
    output_file = system_input.output_file

    if output_file and not moves:
        print("use -m to input your moves")
        sys.exit(1)
   

original_level_info = deepcopy(level_info)
original_locations = deepcopy(locations)

if output_file:
    has_clear = "NO CLEAR"
else:
    show_screen(level_info, locations)

while True:
    if moves:
        actions = user_input(level_info, locations, original_locations, original_level_info, moves)
        moves = ""
    else:
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
            level_info = current_level_info
            locations = current_locations 
            if locations["L"][0] in locations["+"]:
                locations["+"].remove(locations["L"][0])
                level_info["mushroom_collected"] += 1
            elif locations["L"][0] in locations["~"]:
                locations["~"].remove(locations["L"][0])
                level_info["game_lost"] = True
                if not output_file:
                    show_screen(level_info, locations)
                    print(Fore.RED + Style.BRIGHT + "You've lost!")
                break
            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You've won!")
                    level_info["game_won"] = True
                break
    if output_file:
        parse_output(output_file, locations, level_info, has_clear)
        break
    if level_info["game_won"] or level_info["game_lost"]:
        if not output_file:
            print(Style.BRIGHT + "Game ended!")
        break
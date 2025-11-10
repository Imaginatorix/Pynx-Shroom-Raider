import colorama
from colorama import Fore, Style
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement_extra import user_input, keyboard_tracker
from utils.ui import show_screen
from time import sleep
from copy import deepcopy
import sys
import argparse

def main(level_info, locations, moves = "", output_file = ""):
    colorama.init(autoreset=True)
    
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
            keyboard_input = keyboard_tracker()
            if keyboard_input in ("w","a","s","d","p", "!", "="):
                actions = user_input(level_info, locations, original_locations, original_level_info, keyboard_input)
                show_screen(level_info, locations)
            else:
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                continue
        for current_locations, current_level_info in actions:
            if current_level_info["invalid_input"]:
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                break
            level_info = current_level_info
            locations = current_locations 
            if locations["L"][0] in locations["+"]:
                locations["+"].remove(locations["L"][0])
                level_info["mushroom_collected"] += 1
            elif locations["L"][0] in locations["~"]:
                locations["~"].remove(locations["L"][0])
                if not output_file:
                    show_screen(level_info, locations)
                    print(Fore.RED + Style.BRIGHT + "You've lost!")
                    level_info["game_end"] = True
                break
            if not output_file:
                show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You've won!")
                    level_info["game_end"] = True
                break
        if output_file:
            parse_output(output_file, locations, level_info, has_clear)
            break
        else:
            sleep(0.1)
        if level_info["game_end"]:
            if not output_file:
                print(Style.BRIGHT + "Game ended!")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "uhm")
    parser.add_argument("-f", type = str, dest="stage_file")
    parser.add_argument("-m", type = str, dest="string_of_moves")
    parser.add_argument("-o", type = str, dest="output_file")
    system_input = parser.parse_args()

    level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/spring/stage5.txt")
    moves = system_input.string_of_moves
    output_file = system_input.output_file

    if output_file and not moves:
        print("Use -m to input your moves")
        sys.exit(1)
    
    main(level_info, locations, moves, output_file)
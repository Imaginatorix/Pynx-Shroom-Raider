import colorama
<<<<<<< HEAD
from colorama import Fore, Back, Style
=======
import argparse
import os
from colorama import Fore, Style 
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement import user_input
from utils.ui import show_screen
<<<<<<< HEAD
from time import sleep
from copy import deepcopy
import sys
import argparse

def main(level_info, locations, moves, output_file):
    """"
        Run the main game loop for Shroom Raider.
=======
from utils.validator import validate_level_info, validate_locations
from marshal import loads, dumps
from time import sleep

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# === MAIN GAME LOOP ===
def main(level_info: dict[str: set[tuple[int, int]]], locations: dict[str: set[tuple[int, int]]], moves: str, output_file: str) -> str:
    # Clear screen
    clear()

    # Check whether the map data is valid
    validate_locations(*level_info["size"], locations)
    validate_level_info(level_info)

    # Record original map stage
    original_level_info = loads(dumps(level_info))
    original_locations = loads(dumps(locations))
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa

    Args:
        level_info (dict): Information about the current level.
        locations (list): Current positions of objects in the level.
        moves (str): Player moves to execute.
        output_file (str): File path for saving results.

    Returns:
        None
    """
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
            clear()
            show_screen(level_info, locations)
        else:
            actions = user_input(level_info, locations, original_locations, original_level_info)
<<<<<<< HEAD
            if not actions:
                show_screen(level_info, locations)
        for current_locations, current_level_info in actions: #fix this
            if current_level_info["invalid_input"]:
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                break
=======
            clear()
            show_screen(level_info, locations)
        
        # Iterate through all map updates based on user's moves
        for current_locations, current_level_info in actions:
            # Updates old map info
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
            level_info = current_level_info
            locations = current_locations 
            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)
<<<<<<< HEAD
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if output_file:
                    has_clear = "CLEAR"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "You've won!")
                    level_info["game_end"] = True
                break
            elif level_info["game_end"]:
                if not output_file:
                    print(Fore.RED  + "𝚈𝚘𝚞'𝚟𝚎 𝚕𝚘𝚜𝚝!")
=======

            # Tell user an invalid input is given, only prints if no output file is given
            if level_info["invalid_input"] and not output_file:
                level_info["invalid_input"] = False
                sleep(0.1)
                show_screen(level_info, locations)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")

            # When the game ends, check if win or lose 
            if level_info["game_end"] and level_info["mushroom_collected"] == level_info["mushroom_total"]:
                has_clear = "CLEAR"
                break
            elif level_info["game_end"]:
                has_clear = "NO CLEAR"
>>>>>>> 4badb40c8db95e9a02b29413d059eff0168b00fa
                break
        if output_file:
            parse_output(output_file, locations, level_info, has_clear)
            break
        elif level_info["game_end"]:
            break

if __name__ == "__main__":
    """
    Entry point for the Shroom Raider game.

    Initializes colorama, parses command-line arguments, loads the level,
    and starts the main game loop.
    """


    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser(description = "uhm")
    parser.add_argument("-f", type = str, dest="stage_file")
    parser.add_argument("-m", type = str, dest="string_of_moves")
    parser.add_argument("-o", type = str, dest="output_file")
    system_input = parser.parse_args()

    level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/fall/stage1.txt")
    moves = system_input.string_of_moves
    output_file = system_input.output_file

    if output_file and not moves:
        print("Use -m to input your moves")
        sys.exit(1)
    
    main(level_info, locations, moves, output_file)
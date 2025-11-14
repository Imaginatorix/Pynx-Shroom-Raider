import colorama
import argparse
from colorama import Fore, Style 
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement import user_input
from utils.ui import show_screen
from time import sleep
from copy import deepcopy

# === MAIN GAME LOOP ===
def main(level_info, locations, moves, output_file):
    original_level_info = deepcopy(level_info)
    original_locations = deepcopy(locations)

    if not output_file:
        show_screen(level_info, locations)

    has_clear = "NO CLEAR"

    while True:
        if output_file and not moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, " ")
        elif moves:
            actions = user_input(level_info, locations, original_locations, original_level_info, moves)
            moves = ""
        else:
            actions = user_input(level_info, locations, original_locations, original_level_info)
        for current_locations, current_level_info in actions: #fix this
            level_info = current_level_info
            locations = current_locations 
            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)
            if level_info["invalid_input"]:
                if not output_file:
                    print(Fore.RED + Style.BRIGHT + "Invalid input detected")
                break
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if not output_file:
                    print(Fore.GREEN + Style.BRIGHT + "You've won!")
                has_clear = "CLEAR"
                level_info["game_end"] = True
                break
            elif level_info["game_end"]:
                if not output_file:
                    print(Fore.RED  + "𝚈𝚘𝚞'𝚟𝚎 𝚕𝚘𝚜𝚝!")
                break
        if output_file:
            parse_output(output_file, locations, level_info, has_clear)
            break
        elif level_info["game_end"]:
            break

if __name__ == "__main__":
    # Initialize colorama for adding colors to printed strings
    colorama.init(autoreset=True)

    # Initialize the parser for system input arguments
    parser = argparse.ArgumentParser(description = "Shroom Raider Base Game")
    # Arguments and their descriptions
    parser.add_argument("-f", type = str, dest="stage_file")
    parser.add_argument("-m", type = str, dest="string_of_moves")
    parser.add_argument("-o", type = str, dest="output_file")
    # Retrieves the flags given
    system_input = parser.parse_args()

    # Assign the necesserary variables to run a stage, if no system input arguments -> run a default map with no moves and output file
    level_info, locations = parse_level(system_input.stage_file if system_input.stage_file else "levels/fall/stage1.txt")
    moves = system_input.string_of_moves
    output_file = system_input.output_file

    # Start the game loop
    main(level_info, locations, moves, output_file)
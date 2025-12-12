import argparse
import colorama
import os
from colorama import Fore, Style 
from _refactor.parser_refactor import parse_level, parse_output
from _refactor.movement_refactor import user_input
from _refactor.map_data import MapData
from time import sleep
from utils.ui import show_screen

def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

# === MAIN GAME LOOP ===
def main(curr_map: MapData, moves: str, output_file: str) -> tuple[MapData, str]:
    # Clear screen
    clear()
    # Record original map stage
    orig_map = curr_map
    locations = curr_map.get_locations()
    level_info = curr_map.get_level_info()

    # Only print the ui if no output file is given
    if not output_file:
        show_screen(curr_map.get_level_info(), curr_map.get_locations())

    # By default, the clear state is set to NO CLEAR
    has_clear = "NO CLEAR"

    # Game loop -> only breaks if game ends or an output file is given
    while True:
        # Translates moves into updated locations and level_info data
        if output_file and not moves:
            # Has an output file but no moves
            actions = user_input(curr_map, orig_map, " ")
        elif moves:
            # No output file but has moves
            clear()
            show_screen(level_info, locations)
            actions = user_input(curr_map, orig_map, moves)
            # Delete old moves and allow users to input new moves
            moves = ""
        else:
            clear()
            show_screen(level_info, locations)
            actions = user_input(curr_map, orig_map)
            
        
        # Iterate through all map updates based on user's moves
        for new_map in actions:
            locations = new_map.get_locations()
            level_info = new_map.get_level_info()

            # Only print the ui if no output file is given
            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)

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
                break
        
        # Game loop ends if an output file is given or game has ended
        if output_file:
            break
        elif level_info["game_end"]:
            break
    
    clear()
    if not output_file:
        show_screen(level_info, locations)
    return curr_map, has_clear

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
    map_level = parse_level(system_input.stage_file if system_input.stage_file else "levels/fall/stage1.txt")
    moves: str = system_input.string_of_moves
    output_file: str = system_input.output_file

    # Start the game loop and assigns the clear status
    map_level, has_clear = main(map_level, moves, output_file)

    # Writes to an output file if available
    if output_file:
        parse_output(output_file, map_level, has_clear)
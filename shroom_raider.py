import colorama
import argparse
from colorama import Fore, Style 
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement import user_input
from utils.ui import show_screen
from time import sleep
from marshal import loads, dumps

# === MAIN GAME LOOP ===
def main(level_info: dict[str: set[tuple[int, int]]], locations: dict[str: set[tuple[int, int]]], moves: str, output_file: str) -> str:
    # Record original map stage
    original_level_info = loads(dumps(level_info))
    original_locations = loads(dumps(locations))

    # Only print the ui if no output file is given
    if not output_file:
        show_screen(level_info, locations)

    # By default, the clear state is set to NO CLEAR
    has_clear = "NO CLEAR"

    # Game loop -> only breaks if game ends or an output file is given
    while True:
        # Translates moves into updated locations and level_info data
        if output_file and not moves:
            # Has an output file but no moves
            actions = user_input(level_info, locations, original_locations, original_level_info, " ")
        elif moves:
            # No output file but has moves
            actions = user_input(level_info, locations, original_locations, original_level_info, moves)
            # Delete old moves and allow users to input new moves
            moves = ""
        else:
            actions = user_input(level_info, locations, original_locations, original_level_info)
        
        # Iterate through all map updates based on user's moves
        for current_locations, current_level_info in actions:
            # Updates old map info
            level_info = current_level_info
            locations = current_locations 

            # Only print the ui if no output file is given
            if not output_file:
                sleep(0.1)
                show_screen(level_info, locations)

            # Tell user an invalid input is given, only prints if no output file is given
            if level_info["invalid_input"] and not output_file:
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")

            # When the game ends, check if win or lose 
            if level_info["game_end"] and level_info["mushroom_collected"] == level_info["mushroom_total"]:
                has_clear = "CLEAR"
                break
            else:
                has_clear = "NO CLEAR"
                break
        
        # Game loop ends if an output file is given or game has ended
        if output_file:
            break
        elif level_info["game_end"]:
            break

    return has_clear

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

    # Start the game loop and assigns the clear status
    has_clear = main(level_info, locations, moves, output_file)

    # Writes to an output file if available
    if output_file:
        parse_output(output_file, locations, level_info, has_clear)
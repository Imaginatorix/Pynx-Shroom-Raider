import argparse
import colorama
from colorama import Fore, Style 
from _refactor.parser_refactor import parse_level, parse_output
from _refactor.movement_refactor import user_input
from utils.custom_types import LevelState
from time import sleep
from utils.ui import show_screen


# === MAIN GAME LOOP ===
def main(curr_level: LevelState, moves: str, output_file: str) -> tuple[LevelState, str]:

    # Only print the ui if no output file is given
    if not output_file:
        show_screen(curr_level)

    # By default, the clear state is set to NO CLEAR
    has_clear = "NO CLEAR"

    # Game loop -> only breaks if game ends or an output file is given
    while True:
        # Translates moves into updated locations and level_info data
        if output_file and not moves:
            # Has an output file but no moves
            actions = user_input(curr_level, " ")
        elif moves:
            # No output file but has moves
            show_screen(curr_level)
            actions = user_input(curr_level, moves)
            # Delete old moves and allow users to input new moves
            moves = ""
        else:
            show_screen(curr_level)
            actions = user_input(curr_level)
            
        
        # Iterate through all map updates based on user's moves
        for new_level_state in actions:

            # Only print the ui if no output file is given
            if not output_file:
                sleep(0.1)
                show_screen(new_level_state)

            # Tell user an invalid input is given, only prints if no output file is given
            if new_level_state.get_invalid_input() and not output_file:
                new_level_state.set_invalid_input(False)
                sleep(0.1)
                show_screen(new_level_state)
                print(Fore.RED + Style.BRIGHT + "Invalid input detected")

            # When the game ends, check if win or lose 
            if new_level_state.check_game_end() and new_level_state.check_win():
                has_clear = "CLEAR"
                break
            elif new_level_state.check_game_end():
                has_clear = "NO CLEAR"
                break
        
        # Game loop ends if an output file is given or game has ended
        if output_file:
            break
        elif new_level_state.check_game_end():
            break

    if not output_file:
        show_screen(curr_level)
    return curr_level, has_clear

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
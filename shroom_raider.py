import argparse
import colorama
from utils.parser import parse_level_from_file, save_state
from utils.movement import user_input
from utils.custom_types import LevelState
from time import sleep
from utils.ui import show_screen
from utils.validator import validate_state_internals
from utils.leaderboard import showleaderboard, updateleaderboard


# === MAIN GAME LOOP ===
def main(curr_level: LevelState,
         orig_level: LevelState,
         moves: str,
         output_file: str) -> tuple[LevelState, str, int]:
    """
    Main game loop. Updates the level state given to it based on the list of
    level states retrieved from user_input function. If it doesnt have an
    output file, calls the show_screen function to display the ui.

    Parameters
    ----------
    curr_level: LevelState
        Current level information.
    orig_level: LevelState
        Original level information.
    moves: str
        Moves passed when the main file is ran.
    output_file: str
        File location of the txt file where the
        last level state will be parsed into

    Returns
    -------
    tuple[LevelState, str]
        Last level state and win status after the game ends.
    """

    # Only print the ui if no output file is given
    if not output_file:
        show_screen(curr_level)

    # By default, the clear state is set to NO CLEAR
    is_clear: str = "NO CLEAR"

    move_count: int = 0

    # Game loop -> only breaks if game ends or an output file is given
    while True:
        # Translates moves into updated locations and level_info data
        if output_file and not moves:
            # Has an output file but no moves
            actions, move_count = user_input(
                curr_level, orig_level, move_count, " ")
        elif moves:
            # No output file but has moves
            show_screen(curr_level)
            curr_level.invalid_input = False
            actions, move_count = user_input(
                curr_level, orig_level, move_count, moves)
            # Delete old moves and allow users to input new moves
            moves = ""
        else:
            # Get new user input
            curr_level.invalid_input = False
            actions, move_count = user_input(
                curr_level, orig_level, move_count)

        if not actions:
            sleep(0.1)
            show_screen(curr_level)

        # Iterate through all map updates based on user's moves
        for new_level_state in actions:

            validate_state_internals(new_level_state)

            # Only print the ui if no output file is given
            if not output_file:
                sleep(0.1)
                show_screen(new_level_state)
            # When the game ends, check if win or lose
            if new_level_state.game_end:
                is_clear = ("CLEAR" if new_level_state.check_win()
                            else "NO CLEAR")
                break

        # Game loop ends if an output file is given or game has ended
        if output_file:
            break
        elif curr_level.game_end:
            break

    if not output_file:
        show_screen(curr_level)
    return curr_level, is_clear, move_count


if __name__ == "__main__":
    # Initialize colorama for adding colors to printed strings
    colorama.init(autoreset=True)

    # Initialize the parser for system input arguments
    parser = argparse.ArgumentParser(description="Shroom Raider Base Game")
    # Arguments and their descriptions
    parser.add_argument("-f", type=str, dest="stage_file")
    parser.add_argument("-m", type=str, dest="string_of_moves")
    parser.add_argument("-o", type=str, dest="output_file")
    parser.add_argument("-l", type=str, dest="leaderboard")
    # Retrieves the flags given
    system_input = parser.parse_args()

    # Assign the necesserary variables to run a stage
    # if no system input flags -> run default map with no moves and output file
    curr_level = parse_level_from_file(
                system_input.stage_file
                if system_input.stage_file else "levels/challenge/stage2.txt")
    moves: str = system_input.string_of_moves
    output_file: str = system_input.output_file

    if system_input.leaderboard and (moves or
                                     output_file or
                                     system_input.stage_file):
        raise TypeError("use ONLY -l flag to show leaderboard")
    elif system_input.leaderboard:
        showleaderboard(system_input.leaderboard)
    else:
        # Start the game loop and assigns the clear status
        curr_level, is_clear, move_count = main(
            curr_level, curr_level.get_state(), moves, output_file)

        # Writes to an output file if available
        if output_file:
            save_state(output_file, curr_level, is_clear)
        elif is_clear == "CLEAR":
            updateleaderboard(system_input.stage_file if
                              system_input.stage_file else "levels/stage0.txt",
                              move_count)

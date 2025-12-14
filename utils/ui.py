"""Terminal display utilities for rendering the game screen and player instructions."""

import itertools
import os
import shutil

import colorama
from colorama import Fore, Style
from wcwidth import wcswidth

import utils.settings as settings
from utils.custom_types import LevelState


colorama.init(autoreset=True)

# === CREATE SCREEN INSTRUCTIONS ===
def create_instructions(state: LevelState) -> list[str]:
    """
    Create the appropriate instructions for the current game state.

    Depending on the state, this function returns:
    - Standard gameplay instructions
    - A win message
    - A lose message

    Parameters
    ----------
    state : LevelState
        The state of the game

    Returns
    -------
    list[str]
        A list of formatted instruction lines to be displayed to the player.
    """
    # Header
    header = [
        "=====================",
        f"🍄 {Fore.BLUE}𝗦𝗛𝗥𝗢𝗢𝗠 {Style.RESET_ALL}{Fore.RED}𝗥𝗔𝗜𝗗𝗘𝗥{Style.RESET_ALL} 🍄",
        "=====================",
        "",
    ]

    # Item Descriptions
    description = [
        f"✅ {Fore.GREEN}GOAL{Style.RESET_ALL}: Collect all the mushrooms to proceed to the next level!",
        "",
        f"{Style.BRIGHT}Weapons/Tools:",
        f"🔥 {Style.BRIGHT}Flamethrower {Style.RESET_ALL}: Burn down connecting trees to clear the way.",
        "(It is a one-time-use tool.)",
        f"🪓 {Style.BRIGHT}Axe{Style.RESET_ALL}: Chop down trees blocking your path as you move forward.",
        "(It is a one-time-use tool.)",
        f"🪨  {Style.BRIGHT}Rock{Style.RESET_ALL}: This can be used to block the river and create a walkable tile.",
        "(It is a one-time-use element.)",
        "",
    ]

    # Default Instructions
    default_instructions = [
        f"{state._mushroom_collected} out of {state._mushroom_total} mushroom(s) collected"
        "",
        f"[W]{Style.BRIGHT} Move up",
        f"[A]{Style.BRIGHT} Move left",
        f"[S]{Style.BRIGHT} Move down",
        f"[D]{Style.BRIGHT} Move right",
        f"[!]{Style.BRIGHT} Reset",
        f"[E]{Style.BRIGHT} Exit",
        "",
        "No items here" if not state._covering.ui else f"{Fore.GREEN}[P] Pick up {state._covering.ui}" if not state._inventory else f"{Fore.RED}Cannot pick up {state._covering.ui}",
        "Not holding anything" if not state._inventory else f"{Fore.BLUE}Currently holding {state._inventory.ui}",
        "",
    ]

    # Win instructions
    win_message = [
        f"You collected all {state._mushroom_total} 🍄 mushroom(s)",
        f"{Fore.GREEN}You win!",
    ]

    # Lose instructions
    lose_message = [
        f"{Fore.RED}𝙸'𝚖 𝚜𝚘𝚛𝚛𝚢. 𝚃𝚛𝚢 𝚊𝚐𝚊𝚒𝚗 𝚗𝚎𝚡𝚝 𝚝𝚒𝚖𝚎!",
    ]
    
    
    if state._game_end:
        return header+win_message if state._mushroom_collected == state._mushroom_total else header+lose_message
    return header+description+default_instructions


# === CREATE SCREEN ===
def show_screen(state: LevelState, terminal_columns: int = -1) -> str:
    """
    Print and return the screen containing the map and its corresponding instructions.

    The layout adapts to the available terminal width. If the combined width of the
    map and instructions exceeds the terminal width, they are displayed vertically;
    otherwise, they are displayed side by side. The terminal is cleared before
    printing.
    
    Parameters
    ----------
    state : LevelState
        The current state of the game.
    terminal_columns: int, default=-1
        The width of the terminal in columns. If set to -1, the terminal width is detected automatically.

    Returns
    -------
    str
        The full string that is printed to the terminal.
    """

    # Function to clear terminal
    def clear():
       os.system('cls' if os.name == 'nt' else 'clear')
    
    # Check width of terminal
    if terminal_columns == -1:
        terminal_columns = shutil.get_terminal_size()[0]

    # Create what needs to be placed in screen
    ## The Map
    map_ui = state.grid_ui
    ## The Instructions
    instructions = create_instructions(state)

    # Calculate width to determine screen arrangement
    map_width = wcswidth(map_ui[0])
    instructions_width = max(tuple(wcswidth(line) for line in instructions))

    # Calculate what gets shown in the screen
    screen_gap = settings.SPACE*settings.MAP_INSTRUCTIONS_GAP
    display = []
    if map_width + instructions_width + wcswidth(screen_gap) > terminal_columns:
        # Print map_ui first, then instructions
        for map_row in map_ui:
            display.append(map_row)
        display.append('')

        for instructions_row in instructions:
            display.append(instructions_row)
    else:
        map_gap = ' '*map_width
        # Print both at the same time
        for map_row, instructions_row in itertools.zip_longest(map_ui, instructions):
            map_row = map_row if map_row else map_gap
            instructions_row = instructions_row if instructions_row else ''
            display.append(map_row + screen_gap + instructions_row)

    # Clear terminal before printing
    clear()
    output = '\n'.join(display)
    print(output)

    return output


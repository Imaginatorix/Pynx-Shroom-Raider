import colorama
import itertools
import utils.settings as settings
import shutil
import os
from wcwidth import wcswidth
from colorama import Fore, Back, Style
from utils.storyline import storyline
from utils.parser import parse_level
from utils.game_progress import progress
from utils.game_progress import get_next_stage
from utils.game_progress import save_progress



colorama.init(autoreset=True)
 
# === ASCII ===
# TILES
EMPTY_TILE_ASCII = '.'
LARO_CRAFT_TILE_ASCII = 'L'
TREE_TILE_ASCII = 'T'
MUSHROOM_TILE_ASCII = '+'
ROCK_TILE_ASCII = 'R'
WATER_TILE_ASCII = '~'
PAVED_TILE_ASCII = '_'
# ITEMS
AXE_ITEM_ASCII = 'x'
FLAMETHROWER_ITEM_ASCII = '*'


# === UI ===
# TILES
EMPTY_TILE_UI = settings.SPACE
LARO_CRAFT_TILE_UI = '🧑'
TREE_TILE_UI = '🌲'
MUSHROOM_TILE_UI = '🍄'
ROCK_TILE_UI = '🪨'
WATER_TILE_UI = '🟦'
PAVED_TILE_UI = '⬜'
# ITEMS
AXE_ITEM_UI = '🪓'
FLAMETHROWER_ITEM_UI = '🔥'


# === ASCII-UI MAP ===
ASCII_UI_CONVERSIONS = {
    # TILES
    LARO_CRAFT_TILE_ASCII: LARO_CRAFT_TILE_UI,
    EMPTY_TILE_ASCII: EMPTY_TILE_UI,
    TREE_TILE_ASCII: TREE_TILE_UI,
    MUSHROOM_TILE_ASCII: MUSHROOM_TILE_UI,
    ROCK_TILE_ASCII: ROCK_TILE_UI,
    WATER_TILE_ASCII: WATER_TILE_UI,
    PAVED_TILE_ASCII: PAVED_TILE_UI,
    # ITEMS
    AXE_ITEM_ASCII: AXE_ITEM_UI,
    FLAMETHROWER_ITEM_ASCII: FLAMETHROWER_ITEM_UI,
}


# === CREATE SCREEN MAP UI ===
def create_map_ui(size: tuple[int, int], locations: dict[str: list[tuple[int, int]]]) -> tuple[str]:
    r, c = size
    if r == 0 or c == 0:
        return [], None
    if r < 0 or c < 0:
        raise ValueError("Map size cannot be negative")
    if r > 30 or c > 30:
        raise ValueError("Map size cannot exceed 30 by 30")

    # Generate empty map
    map_ui = []
    for i in range(r):
        map_ui.append([""]*c)

    # Record overlays (specifically, those on character cell which information is lost upon UI creation)
    character_location = locations['L'][0]
    character_cell = None
    for c, coord in locations.items():
        for i, j in coord:
            if (i, j) == character_location and c != 'L':
                character_cell = ASCII_UI_CONVERSIONS[c]
            # Set cell to higher priority (for now, only character)
            if not map_ui[i][j] or c == 'L':
                map_ui[i][j] = ASCII_UI_CONVERSIONS[c]

    # Join row completely to a string
    for i in range(r):
        map_ui[i] = ''.join(map_ui[i])

    return map_ui, character_cell


# === CREATE SCREEN INSTRUCTIONS ===
def create_instructions(level_info: dict, character_cell: str) -> tuple[str]:
    # Header
    header = (
        "=====================",
        f"🍄 {Fore.BLUE}𝗦𝗛𝗥𝗢𝗢𝗠 {Style.RESET_ALL}{Fore.RED}𝗥𝗔𝗜𝗗𝗘𝗥{Style.RESET_ALL} 🍄",
        "=====================",
        "",
    )

    description = (
        f"✅ {Fore.GREEN}GOAL{Style.RESET_ALL}: Collect all the mushrooms to proceed to the next level!",
        "",
        f"{Style.BRIGHT}Weapons/Tools:",
        f"🔥 {Style.BRIGHT}Flamethrower {Style.RESET_ALL}: Burn down connecting trees to clear the way. (It is a one-time-use tool.)",
        f"🪓 {Style.BRIGHT}Axe{Style.RESET_ALL}: Chop down trees blocking your path as you move forward. (It is a one-time-use tool.)",
        f"🪨  {Style.BRIGHT}Rock{Style.RESET_ALL}: This can be used to block the river and create a walkable tile. (It is a one-time-use element.)",
        "",
    )

    # Default instructions
    default_instructions = (
        f"{level_info['mushroom_collected']} out of {level_info['mushroom_total']} mushroom(s) collected"
        "",
        f"[W]{Style.BRIGHT} Move up",
        f"[A]{Style.BRIGHT} Move left",
        f"[S]{Style.BRIGHT} Move down",
        f"[D]{Style.BRIGHT} Move right",
        f"[!]{Style.BRIGHT} Reset",
        "",
        "No items here" if not character_cell else f"{Fore.GREEN}[P] Pick up {character_cell}" if not level_info['inventory'] else f"{Fore.RED}Cannot pick up {character_cell}",
        "Not holding anything" if not level_info['inventory'] else f"{Fore.BLUE}Currently holding {ASCII_UI_CONVERSIONS[level_info['inventory']]}",
        "",
    )

    # Win instructions
    win_message = (
        f"You collected {level_info['mushroom_collected']} 🍄 out of {level_info['mushroom_total']} 🍄 mushroom(s)",
        f"{Fore.GREEN}You win!",
        ""
    )

    # Lose instructions
    lose_message = (
        f"{Fore.RED}𝙸'𝚖 𝚜𝚘𝚛𝚛𝚢. 𝚃𝚛𝚢 𝚊𝚐𝚊𝚒𝚗 𝚗𝚎𝚡𝚝 𝚝𝚒𝚖𝚎!",
    )
    
    season, stage_file = progress()
    storylines = storyline(os.path.join("levels", season, stage_file))


    if level_info['game_end']:
        return header+win_message if level_info["mushroom_collected"] == level_info["mushroom_total"] else header+lose_message
    return header+storylines+description+default_instructions




# === CREATE SCREEN ===
def show_screen(level_info: dict, locations: dict[str: list[tuple[int, int]]], terminal_columns: int|None = None) -> None:
    # Function to clear terminal
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Check width of terminal
    if not terminal_columns:
        terminal_columns = shutil.get_terminal_size()[0]

    # Create what needs to be placed in screen
    ## The Map
    map_ui, character_cell = create_map_ui(level_info["size"], locations)
    ## The Instructions
    instructions = create_instructions(level_info, character_cell)

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
    print(*display, sep='\n')
    return display


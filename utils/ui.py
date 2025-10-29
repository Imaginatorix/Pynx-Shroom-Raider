import itertools
import utils.settings as settings
import shutil
from wcwidth import wcswidth

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
    # Generate empty map
    map_ui = []
    for i in range(r):
        map_ui.append([""]*c)

    # Record overlays (specifically, those on character cell which information is lost upon UI creation)
    character_location = locations['L'][0]
    character_cell = []
    for c, coord in locations.items():
        for i, j in coord:
            if (i, j) == character_location and c != 'L':
                character_cell.append(ASCII_UI_CONVERSIONS[c])
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
        "=== SHROOM RAIDER ===",
        "Goal: Collect all mushrooms to proceed to the next level!",
        ""
    )

    # Default instructions
    default_instructions = (
        f"{level_info['mushroom_collected']} out of {level_info['mushroom_total']} mushroom(s) collected"
        "",
        "[W] Move up",
        "[A] Move left",
        "[S] Move down",
        "[D] Move right",
        "[!] Reset",
        "",
        "No items here" if not character_cell else f"[P] Pick up {''.join(character_cell)}",
        "Not holding anything" if not level_info['inventory'] else f"Currently holding {level_info['inventory']}",
        "",
    )

    # Win instructions
    win_message = (
        f"You collected {level_info['mushroom_collected']} out of {level_info['mushroom_total']} mushroom(s)",
        "You win!",
        ""
    )

    # Lose instructions
    lose_message = (
        "You lost!",
    )

    if level_info['game_end']:
        return header+win_message if level_info['game_win'] else header+lose_message
    return header+default_instructions


# === CREATE SCREEN ===
def show_screen(level_info: dict, locations: dict[str: list[tuple[int, int]]]) -> None:
    # Check width of terminal
    terminal_columns = shutil.get_terminal_size()[0]

    # Create what needs to be placed in screen
    ## The Map
    map_ui, character_cell = create_map_ui(level_info["size"], locations)
    ## The Instructions
    instructions = create_instructions(level_info, character_cell)

    # Calculate width to determine screen arrangement
    map_width = wcswidth(map_ui[0])
    instructions_width = max(tuple(wcswidth(line) for line in instructions))

    screen_gap = settings.SPACE*settings.MAP_INSTRUCTIONS_GAP
    if map_width + instructions_width + wcswidth(screen_gap) > terminal_columns:
        # Print map_ui first, then instructions
        for map_row in map_ui:
            print(map_row)
        print()

        for instructions_row in instructions:
            print(instructions_row)
    else:
        map_gap = ' '*map_width
        # Print both at the same time
        for map_row, instructions_row in itertools.zip_longest(map_ui, instructions):
            map_row = map_row if map_row else map_gap
            instructions_row = instructions_row if instructions_row else ''
            print(map_row + screen_gap + instructions_row)

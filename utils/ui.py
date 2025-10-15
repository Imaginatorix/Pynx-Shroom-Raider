import itertools
import settings
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
def create_map_ui(map_ascii: tuple[str]) -> tuple[str]:
    return tuple(
        ''.join(ASCII_UI_CONVERSIONS[char] for char in row)
        for row in map_ascii
    )


# === CREATE SCREEN INSTRUCTIONS ===
def create_instructions(
        current_mushrooms: int,
        total_mushrooms: int,
        on_floor: None|str = None,
        in_hand: None|str = None,
        game_end: bool = False,
        win: bool = False
    ) -> tuple[str]:

    # Header
    header = (
        "=== SHROOM RAIDER ===",
        "Goal: Collect all mushrooms to proceed to the next level!",
        ""
    )

    # Default instructions
    default_instructions = (
        f"{current_mushrooms} out of {total_mushrooms} mushroom(s) collected"
        "",
        "[W] Move up",
        "[A] Move left",
        "[S] Move down",
        "[D] Move right",
        "[!] Reset",
        "",
        "No items here" if not on_floor else f"[P] Pick up {on_floor}",
        "Not holding anything" if not in_hand else f"Currently holding {in_hand}",
        "",
    )

    # Win instructions
    win_message = (
        f"You collected {current_mushrooms} out of {total_mushrooms} mushroom(s)",
        "You win!",
        ""
    )

    # Lose instructions
    lose_message = (
        "You lost!",
    )

    if game_end:
        return header+win_message if win else header+lose_message
    return header+default_instructions


# === CREATE SCREEN ===
def show_screen(
        map_ascii: tuple[str],
        current_mushrooms: int,
        total_mushrooms: int,
        on_floor: None|str = None,
        in_hand: None|str = None,
        game_end: bool = False,
        win: bool = False
    ) -> None:

    # Check width of terminal
    terminal_columns = shutil.get_terminal_size()[0]

    # Create what needs to be placed in screen
    map_ui = create_map_ui(map_ascii)
    instructions = create_instructions(current_mushrooms, total_mushrooms, on_floor, in_hand, game_end, win)

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
        # Print both at the same time
        for map_row, instructions_row in itertools.zip_longest(map_ui, instructions):
            map_row = map_row if map_row else settings.SPACE*settings.MAP_INSTRUCTIONS_GAP
            instructions_row = instructions_row if instructions_row else settings.SPACE*settings.MAP_INSTRUCTIONS_GAP
            print(map_row + screen_gap + instructions_row)


map_ascii = (
"TTTTTTTTTTTTTTTTTT",
"T........T.......T",
"T........~.......T",
"T.x......T.......T",
"T..TT....T....+..T",
"T.T+T....T.......T",
"T.TT.....TTTTTTTTT",
"T........R.......T",
"T................T",
"T...........*....T",
"T...TT...........T",
"T.....T..........T",
"T......T.......TTT",
"TTTT...TTTT......T",
"T...T....~.T..R..T",
"T.L.T...TT.....T~T",
"T...TTT..T....T+.T",
"T........T....T..T",
"T........T....T..T",
"TTTTTTTTTTTTTTTTTT",
)

show_screen(map_ascii, 0, 10)

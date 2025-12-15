"""
Utilities for reading and saving the game states from and to memory.

Functions
---------
get_tile_locations
    Extract the grid coordinates of each tile type from an ASCII grid.
parse_level_from_file
    Parse a level definition from a text file into a LevelState object.
save_state
    Serialize the current level state and write it to a file.
"""

from utils.custom_types import LevelState, Tile
from utils.settings import MUSHROOM_TILE, NONE_TILE, PLAIN_TO_TILE, VALID_TILES
from utils.validator import validate_type, validate_locations

# === GET THE LOCATIONS OF THE GAME ELEMENTS ===
def get_tile_locations(grid: list[str]) -> dict[Tile, set]:
    """
    Extract the locations of all tiles in a grid.

    Given an ASCII grid representation of a level, this function maps each
    valid tile type to the set of coordinates at which it appears.

    Parameters
    ----------
    grid : list[str]
        A list of strings representing the level grid, where each character
        corresponds to a tile.

    Returns
    -------
    dict[Tile, set[tuple[int, int]]]
        A dictionary mapping each valid tile to a set of coordinates
        indicating where that tile appears in the grid.

    Raises
    ------
    TypeError
        If the grid does not conform to expected type.
    ValueError
        If the grid contains a character that does not correspond to a valid
        tile.
    """
    validate_type(grid, list[str], "grid")

    locations = {
        tile: set()
        for tile in VALID_TILES
    }

    row = -1
    col = -1
    for i, line in enumerate(grid):
        for j, c in enumerate(line.strip()):
            if c not in PLAIN_TO_TILE:
                print(c)
                raise ValueError("Tiles must be valid")
            locations[PLAIN_TO_TILE[c]].add((i, j))
            row = max(row, i+1)
            col = max(col, j+1)

    validate_locations((row, col), locations)

    return locations


# === PARSE GAME LEVEL ===
def parse_level_from_file(filename: str) -> LevelState:
    """
    Parse a level definition from a text file.

    The level file is expected to have the following format:
    - The first line contains two integers specifying the grid dimensions
      (rows and columns).
    - The remaining lines define the ASCII grid of the level.

    This function constructs and returns a `LevelState` instance based on the
    parsed data.

    Parameters
    ----------
    filename : str
        Path to the level definition file.

    Returns
    -------
    LevelState
        The initialized level state corresponding to the file contents.

    Raises
    ------
    ValueError
        If the grid contains invalid tile characters.
    IOError
        If the file cannot be opened or read.
    """
    
    with open(filename, 'r') as f:
        lines = f.readlines()

        # Get the first line of .txt file
        stage_size = lines[0].strip()

        # Get the rest line of .txt file
        grid = lines[1:]

    # Get the size as the row and column 
    r, c = map(int, stage_size.split())
    size = (r, c)
    validate_size(size)

    locations = get_tile_locations(grid)
    mushroom_total = len(locations[MUSHROOM_TILE])

    return LevelState(size, mushroom_total, locations, NONE_TILE, NONE_TILE)


# === SAVE CURRENT STATE TO A FILE ===
def save_state(filename: str, state: LevelState, has_cleared: str) -> None:
    """
    Save the current game state to a file.

    The output file contains:
    - A flag indicating whether the level has been cleared
    - The grid dimensions
    - The ASCII representation of the current grid

    Parameters
    ----------
    filename : str
        Path to the output file.
    state : LevelState
        The current level state to be saved.
    has_cleared : str
        A string flag indicating the clear status of the level.

    Returns
    -------
    None
        This function does not return a value.
    """
    
    size = state.size
    grid = state.grid_ascii

    with open(filename, 'w') as f:
        f.write(has_cleared+"\n")
        f.write(f"{size[0]} {size[1]}\n")
        f.write("\n".join(grid))

    return None

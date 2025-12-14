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

# === GET THE LOCATIONS OF THE GAME ELEMENTS ===
<<<<<<< HEAD
def get_tile_locations(grid):
    """Scans the textual grid representation, validates characters
    against the mapping in PLAIN_TO_TILE, and groups coordinates by tile type.

    Parameters
    ----------
        grid (list[str]): A list of strings representing the game grid, where
            each character corresponds to a tile.

    Returns
    -------
        dict[str, set[tuple[int, int]]]: A dictionary mapping each tile type
        in VALID_TILES to a set of (row, column) coordinate pairs.

    Raises
    ------
        ValueError: If the grid contains a character not found in
            PLAIN_TO_TILE.
    """

=======
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
    ValueError
        If the grid contains a character that does not correspond to a valid
        tile.
    """
    
>>>>>>> 8813525055aa539e197764595ca71010adad5a7b
    locations = {
        tile: set()
        for tile in VALID_TILES
    }

    for i, line in enumerate(grid):
        for j, c in enumerate(line.strip()):
            if c not in PLAIN_TO_TILE:
                raise ValueError("Grid contains an invalid tile!")
            locations[PLAIN_TO_TILE[c]].add((i, j))

    return locations


# === PARSE GAME LEVEL ===
<<<<<<< HEAD
def parse_level_from_file(filename):
    """Parse a level file and create the corresponding LevelState.

    The level file contain a first line with two integers
    specifying the grid size, followed by lines representing the stage layout.

    Parameters
    ----------
        filename : str
            Path to the level file.

    Returns
    -------
        LevelState: 
            The grid size, total number of mushrooms, and the mapping of tile locations.

    Raises
    ------
        ValueError:
            From 'get_tile_locations' if the file contains invalid tile characters.
    """

=======
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
    
>>>>>>> 8813525055aa539e197764595ca71010adad5a7b
    with open(filename, 'r') as f:
        lines = f.readlines()

        # Get the first line of .txt file
        stage_size = lines[0].strip()

        # Get the rest line of .txt file
        grid = lines[1:]

    # Get the size as the row and column 
    r, c = map(int, stage_size.split())
    size = (r, c)

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

<<<<<<< HEAD
def parse_output(filename, locations, level_info, has_clear):
    """Writes the level output file using the provided tile locations and data.

    The function reconstructs a textual grid from the given tile coordinates
    and writes it—along with level status information—to an output file.

    Parameters
    ----------
        filename : str 
            Path of the output file to write.
        locations : dict[str, list[tuple[int, int]]]
            Mapping of tile types to their coordinate lists.
        level_info : str
            The LevelState instance containing size information for the grid.
        has_clear : str
            A string indicating whether the level is cleared.

    Returns
    -------
        None
    """

    coordinates = {}
    for c in locations:
        if c != "L":
            for coordinate in locations[c]:
                coordinates[coordinate] = c
    coordinates[locations["L"][0]] = "L"
=======
>>>>>>> 8813525055aa539e197764595ca71010adad5a7b
    with open(filename, 'w') as f:
        f.write(has_cleared+"\n")
        f.write(f"{size[0]} {size[1]}\n")
        f.write("\n".join(grid))

    return None

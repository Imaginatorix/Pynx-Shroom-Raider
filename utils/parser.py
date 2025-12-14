from utils.custom_types import LevelState
from utils.settings import MUSHROOM_TILE, PLAIN_TO_TILE, VALID_TILES

# === GET THE LOCATIONS OF THE GAME ELEMENTS ===
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

    return LevelState(size, mushroom_total, locations)

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
    with open(filename, 'w') as f:
        f.write(has_clear+"\n")
        f.write(f"{level_info["size"][0]} {level_info["size"][1]}\n")
        for i in range(level_info["size"][0]):
            temp = ""
            for j in range(level_info["size"][1]-1):
                if (i,j) not in coordinates:
                    temp += "."
                else:
                    temp += coordinates[(i,j)]
            f.write(temp+("\n" if i != level_info["size"][0]-1 else ""))
    return
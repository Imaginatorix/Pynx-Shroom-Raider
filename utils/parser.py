from utils.custom_types import LevelState
from utils.settings import MUSHROOM_TILE, PLAIN_TO_TILE, VALID_TILES

# === GET THE LOCATIONS OF THE GAME ELEMENTS ===
def get_tile_locations(grid):
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
    with open(filename, 'r') as f:
        lines = f.readlines()

        # Get the first line of .txt file
        stage_size = lines[0].strip()

        # Get the rest line of .txt file
        grid = lines[1:]

    # Get the size as the width and height 
    r, c = map(int, stage_size.split())
    size = (r, c)

    locations = get_tile_locations(grid)
    mushroom_total = len(locations[MUSHROOM_TILE])

    return LevelState(size, mushroom_total, locations)

def parse_output(filename, locations, level_info, has_clear): #TODO: Update into class methods
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
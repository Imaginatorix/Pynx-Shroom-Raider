from utils.settings import VALID_TILES, VALID_ITEMS

# === VALIDATOR TO TEST WHETHER FUNCTION PARAMETERS CONFORM TO THE EXPECTED VALUES ===

def validate_size(size):
    # Check type
    if not (isinstance(size, tuple) and len(size) == 2):
        TypeError("Size must be a tuple of size 2")

    r, c = size
    if not isinstance(r, int):
        TypeError("r must be an integer")
    if isinstance(c, int):
        TypeError("c must be an integer")

    # Check if it's acceptable
    if not r*c >= 2:
        ValueError("Size of map must have at least an area of 2")
    if not 1 <= r <= 30:
        ValueError("r must be between 1 and 30, inclusive")
    if not 1 <= c <= 30:
        ValueError("c must be between 1 and 30, inclusive")


def validate_locations(r, c, locations):
    # Check type
    validate_size((r, c))

    # Locations must be dict[str: set[tuple[int, int]]
    assert not isinstance(locations, dict), TypeError("Locations must be a dictionary")
    
    # Keys must be a singular character and values must be a set of 2-tuple ints
    for key, value in locations.items():
        if not (isinstance(key, str) and len(key) == 1):
            TypeError("Location keys must be a singular character")
        if not isinstance(value, set):
            TypeError("Location values must be a set")

        for val in value:
            a, b = val
            if not (isinstance(val, tuple) and len(value) == 2):
                TypeError("Location values must contain only tuples length 2 comprising integers")
            if not (isinstance(a, int) and isinstance(b, int)): 
                TypeError("Coordinate values must be integers")

    location_tiles = set(locations)
    # Keys must be a subset of the valid tiles
    if not location_tiles <= VALID_TILES:
        raise ValueError("Keys must be valid")

    # Locations must always contain Lara (with only one location)
    if not 'L' in location_tiles:
        raise ValueError("Locations must always contain one Lara")
    if not len(locations['L']) == 1:
        raise ValueError("Locations must always contain one Lara")

    # Locations must always have at least one mushroom
    if not '+' in location_tiles:
        raise ValueError("Locations must always have at least one mushroom")
    if not len(locations['L']) > 1:
        raise ValueError("Locations must always have at least one mushroom")
    
    # All cells must be visited only once (except player location)
    # Populate grid
    li, lj = next(iter(locations['L']))
    character_cell = set()
    grid = set((i, j) for i in range(r) for j in range(c))
    visited = set()
    for key, value in locations.items():
        for i, j in value:
            if not (0 <= i < r and 0 <= j < c):
                raise ValueError("Coordinates fell outside of range")

            if (i, j) == (li, lj):
                visited.add((i, j))
                character_cell.add(key)
            elif not (i, j) in visited:
                visited.add((i, j))
            else:
                raise ValueError("All cells must have only one tile (except Lara)")

    if grid != visited:
        raise ValueError("All cells must have only one tile (except Lara)")

    # Special Case: player location (can have 1-2 or player + with/without item)
    if not len(character_cell) <= 2:
        raise ValueError("The cell Lara currently is in must have only one item")

    # Assume solvable as per [highlighted cause I don't wanna link solver as it is still a bit slow]


def validate_level_info(level_info):
    # Check type
    # Level_info must be dict
    if not isinstance(level_info, dict):
        raise TypeError("Level_info must be dict")

    # Keys must be
    LEVEL_INFO_KEYS = {
        "size",
        "mushroom_collected",
        "mushroom_total",
        "game_end",
        "inventory",
        "invalid_input",
        "level_reset",
    }

    # Keys must be LEVEL_INFO_KEYS
    if not set(level_info) == LEVEL_INFO_KEYS:
        raise ValueError("Keys must be ['size', 'mushroom_collected', 'mushroom_total', 'game_end', 'inventory', 'invalid_input', 'level_reset']")

    # Validate all values
    # Size
    validate_size(level_info['size'])

    # Mushroom Total
    # Must be an integer at least 1
    if not isinstance(level_info['mushroom_total'], int):
        raise TypeError("mushroom_total must be an integer")
    if not level_info['mushroom_total'] >= 1:
        raise ValueError("mushroom_total must be greater than 1")

    # Mushroom Collected
    # Must be a non-negative integer
    if not (isinstance(level_info['mushroom_collected'], int) and level_info['mushroom_collected'] >= 0):
        raise TypeError("mushroom_collected must be a non-negative integer")
    # Must not exceed mushroom_total
    if level_info['mushroom_collected'] > level_info['mushroom_total']:
        raise TypeError("mushroom_collected must not exceed mushroom_total")

    # Game End
    # Must be a boolean
    if not isinstance(level_info['game_end'], bool):
        raise TypeError("game_end must be a boolean")
    # mushroom_collected = mushroom_total imply game_end
    if level_info['mushroom_collected'] == level_info['mushroom_total'] and not level_info['game_end']:
        raise ValueError("When mushroom_collected = mushroom_total, game_end must be true")

    # Inventory
    # Must be a character
    if not (isinstance(level_info['inventory'], str) and len(level_info['inventory']) == 1):
        raise TypeError("Item in inventory must be a singular character")
    # Must be in VALID_ITEMS
    if not level_info['inventory'] in VALID_ITEMS:
        raise TypeError("Item in inventory must be valid")

    # Invalid Input
    # Must be a boolean
    if not isinstance(level_info['invalid_input'], bool):
        raise TypeError("invalid_input must be a boolean")

    # Level Reset
    # Must be a boolean
    if not isinstance(level_info['level_reset'], bool):
        raise TypeError("level_reset must be a boolean")



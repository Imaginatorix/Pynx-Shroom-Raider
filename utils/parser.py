def get_locations(grid):
    locations = {}
    for i, line in enumerate(grid):
        for j, c in enumerate(line.strip()):
            if not c in locations:
                locations[c] = []
            locations[c].append((i, j))
    return locations

def get_level_info(grid, locations):
    return {
        "size": (len(grid), len(grid[0])),
        "mushroom_collected": 0,
        "mushroom_total": len(locations['+']),
        "game_end": False,
        "inventory": None
    }

def parse_level(filename):
    with open(filename, 'r') as f:
        grid = f.readlines()
        locations = get_locations(grid)
    level_info = get_level_info(grid, locations)
    level_info["original_location"] = locations["L"]
    return (level_info, locations)



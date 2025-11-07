def get_locations(grid):
    locations = {
        ".": [],
        "T": [],
        "R": [],
        "_": [],
        "~": [],
        "x": [],
        "*": [],
        "+": [],
        "L": []
    }
    for i, line in enumerate(grid):
        for j, c in enumerate(line.strip()):
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
    return (level_info, locations)

def parse_output(filename, locations, level_info, has_clear):
    coordinates = {}
    for c in locations:
        if c != "L":
            for coordinate in locations[c]:
                coordinates[coordinate] = c
    coordinates[locations["L"][0]] = "L"
    with open(filename, 'w') as f:
        f.write(has_clear+"\n")
        for i in range(level_info["size"][0]):
            temp = ""
            for j in range(level_info["size"][1]-1):
                if (i,j) not in coordinates:
                    temp += "."
                else:
                    temp += coordinates[(i,j)]
            f.write(temp+("\n" if i != level_info["size"][0]-1 else ""))
    return
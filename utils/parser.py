# == GET THE LOCATIONS OF THE GAME ELEMENTS == 
def get_locations(grid):
    locations = {
        ".": set(),
        "T": set(),
        "R": set(),
        "_": set(),
        "~": set(),
        "x": set(),
        "*": set(),
        "+": set(),
        "L": set()
    }
    for i, line in enumerate(grid):
        for j, c in enumerate(line.strip()):
            locations[c].add((i, j))
    return locations

# == GAME LEVEL INFO == 
def get_level_info(size, grid, locations):
    return {
        "size": size,
        "mushroom_collected": 0,
        "mushroom_total": len(locations['+']),
        "game_end": False,
        "inventory": "",
        "invalid_input": False
    }

# == PARSE GAME LEVEL == 
def parse_level(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

        # Get the first line of .txt file
        size_of_stage = lines[0].strip()

        # Get the rest line of .txt file
        grid = lines[1:]

    # get the size as the width and height 
    width, height = map(int, size_of_stage.split())
    size = (height, width)

    
    locations = get_locations(grid)
    level_info = get_level_info(size, grid, locations)
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
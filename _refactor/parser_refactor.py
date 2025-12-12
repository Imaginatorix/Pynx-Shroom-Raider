from _refactor.map_data import MapData

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

    return MapData(size, grid)

def parse_output(filename, map_level, has_clear):
    locations = map_level.get_locations()
    level_info = map_level.get_level_info()
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
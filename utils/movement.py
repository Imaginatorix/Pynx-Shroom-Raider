from marshal import loads, dumps

# === REMOVES TREES AFFECTED BY FIRE===
def firespread(start: tuple, locations: dict[str: set[tuple[int, int]]]):
    kernel = ((-1,0),(0,-1),(1,0),(0,1))
    frontier = [start]
    n = 0

    # Keep removing trees until there are no more adjacent trees
    while n < len(frontier):
        i, j = frontier[n]
        for di, dj in kernel:
            new = (di + i, dj + j)
            if new in locations["T"]:
                frontier.append(new)
                locations["T"].remove(new)
                locations["."].add(new)
        n+=1

# === USE USER INPUT TO UPDATE MAP DATA ===
def user_input(level_info: dict[str: set[tuple[int, int]]], locations: dict[str: set[tuple[int, int]]], original_locations: dict[str: set[tuple[int, int]]], original_level_info: dict[str: set[tuple[int, int]]], sys_input: str = ""):
    # Checks if moves are given to the function
    if sys_input: 
        # Use the moves given as commands
        commands = tuple(ch for ch in sys_input.upper())
    else:
        # Get moves using the input function and use as commands
        commands = tuple(ch for ch in input("What will you do? ").upper())
    
    possible_inputs={"W":(-1,0), "A":(0,-1), "S":(1,0), "D":(0,1), "!":None, "P":None, "=":None}
    actions=[]

    # Create new copy of map data to modify
    _locations = loads(dumps(locations))
    _level_info = loads(dumps(level_info))

    # When commands are empty, mark as invalid input
    if not commands:
        _level_info["invalid_input"] = True
        actions.append((_locations, _level_info))
        return actions
    
    # Iterate through each character of commands
    for action in commands:

        # When action is invalid, stop the iteration
        if action not in possible_inputs:
            _level_info["invalid_input"] = True
            actions.append((_locations, _level_info))
            break
        elif action == "=":
            actions= "end"
            break
        elif action == "!":
            # Reverts the map data to the original map data
            _locations = loads(dumps(original_locations))
            _level_info = loads(dumps(original_level_info))
        elif action=="P":
            # Check if Laro is in an item tile or already has an item
            if next(iter(_locations["L"])) not in (*_locations["*"], *_locations["x"]) or _level_info["inventory"]:
                continue
            else:
                # Laro picks up the items and removes it from the map
                _level_info["inventory"] = ("*" if next(iter(_locations["L"])) in _locations["*"] else "x")
                _locations[_level_info["inventory"]].remove(next(iter(_locations["L"])))
        else:
            if next(iter(_locations["L"])) not in (*_locations["*"], *_locations["x"], *_locations["_"]):
                # Add an empty character in Laro's previous location
                _locations["."].add(next(iter(_locations["L"])))
            
            # Create new possible player location
            x,y = next(iter(_locations["L"]))
            i,j = possible_inputs[action]
            player_location = (x+i,y+j)
            
            if player_location in _locations["T"] and _level_info["inventory"] == "x":
                _locations["T"].remove(player_location)
                _level_info["inventory"] = ""
            if player_location in _locations["T"] and _level_info["inventory"] == "*":
                _level_info["inventory"] = ""
                firespread(player_location,_locations)
            if 0<=x+i<level_info["size"][0] and 0<=y+j<level_info["size"][1] and player_location not in _locations["T"]:
                if player_location in _locations["R"]:
                    new_rock = (x+i*2,y+j*2)
                    if new_rock in _locations["~"]:
                        _locations["~"].remove(new_rock)
                        _locations["_"].add(new_rock)
                        _locations["R"].remove(player_location)
                    elif new_rock in _locations["."]:
                        _locations["."].remove(new_rock)
                        _locations["R"].add(new_rock)
                        _locations["R"].remove(player_location)
                    elif new_rock in _locations["_"]: #requires more testing, primative fix
                        _locations["R"].add(new_rock)
                        _locations["R"].remove(player_location)
                    else:
                        continue
                elif player_location in _locations["~"]:
                    _locations["~"].remove(player_location)
                    _level_info["game_end"] = True
                elif player_location in _locations["+"]:
                    _locations["+"].remove(player_location)
                    _level_info["mushroom_collected"] += 1
                if _level_info["mushroom_collected"] == _level_info["mushroom_total"]:
                    _level_info["game_end"] = True
                _locations["L"] = {player_location}
            else:
                continue
            if next(iter(_locations["L"])) in _locations["."]:
                _locations["."] = set(_locations["."])
                _locations["."].remove(next(iter(_locations["L"])))
        actions.append((_locations, _level_info))
        _locations = loads(dumps(_locations))
        _level_info = loads(dumps(_level_info))
    return actions


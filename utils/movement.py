from copy import deepcopy

def firespread(start,locations):
    kernel = ((-1,0),(0,-1),(1,0),(0,1))
    frontier = [start]
    n = 0
    while n < len(frontier):
        i, j = frontier[n]
        for di, dj in kernel:
            new = (di + i, dj + j)
            if new in locations["T"]:
                frontier.append(new)
                locations["T"].remove(new)
                locations["."].add(new)
        n+=1

def user_input(level_info, locations, original_locations, original_level_info, sys_input = ""):
    if sys_input: 
        commands = tuple(ch for ch in sys_input.upper())
    else:
        commands = tuple(ch for ch in input("What will you do? ").upper())
    possible_inputs={"W":(-1,0), "A":(0,-1), "S":(1,0), "D":(0,1), "!":None, "P":None, "=":None}
    actions=[]
    _locations = deepcopy(locations)
    _level_info = deepcopy(level_info)
    if not commands:
        _level_info["invalid_input"] = True
        actions.append((_locations, _level_info))
        return actions
    for action in commands:
        if action not in possible_inputs:
            _level_info["invalid_input"] = True
            actions.append((_locations, _level_info))
            break
        elif action == "=":
            actions= "end"
            break
        elif action == "!":
            _level_info = deepcopy(original_level_info)
            _locations = deepcopy(original_locations)
        elif action=="P":
            if next(iter(_locations["L"])) not in (*_locations["*"], *_locations["x"]) or _level_info["inventory"]:
                continue
            _level_info["inventory"] = ("*" if next(iter(_locations["L"])) in _locations["*"] else "x")
            _locations[_level_info["inventory"]].remove(next(iter(_locations["L"])))
        else:
            if next(iter(_locations["L"])) not in (*_locations["*"], *_locations["x"], *_locations["_"]):
                _locations["."].add(next(iter(_locations["L"])))
            x,y = next(iter(_locations["L"]))
            i,j = possible_inputs[action]
            player_location = (x+i,y+j)
            if player_location in _locations["T"] and _level_info["inventory"] == "x":
                _locations["T"].remove(player_location)
                _level_info["inventory"] = ""
            if player_location in _locations["T"] and _level_info["inventory"] == "*":
                _level_info["inventory"] = ""
                firespread(player_location,_locations)
            if 0<=x+i<level_info["size"][0]-1 and 0<=y+j<level_info["size"][1]-1 and player_location not in _locations["T"]:
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
        _locations = deepcopy(_locations)
        _level_info = deepcopy(_level_info)
    return actions


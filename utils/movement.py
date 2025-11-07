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
                locations["."].append(new)
        n+=1

def user_input(size, inventory, locations, original_locations, sys_input = ""):
    if sys_input: 
        commands = tuple(ch for ch in sys_input.upper())
    else:
        commands = tuple(ch for ch in tuple(input("What will you do? ").upper()))
    possible_inputs={"W":(-1,0),"A":(0,-1),"S":(1,0),"D":(0,1),"!":None, "P":None,"E":None}
    if not commands:
        return
    actions=[]
    _locations = deepcopy(locations)
    for action in commands:
        if action not in possible_inputs:
            actions.append(({}, ""))
            break
        if action == "E":
            actions.append("End")
        elif action == "!":
            _locations=deepcopy(original_locations)
        elif action=="P":
            if _locations["L"][0] not in (*_locations["*"], *_locations["x"]) or inventory:
                actions.append(({}, ""))
                break
            inventory = ("*" if _locations["L"][0] in _locations["*"] else "x")
            _locations[inventory].remove(_locations["L"][0])
        else:
            if _locations["L"][0] not in (*_locations["*"], *_locations["x"], *_locations["_"]):
                _locations["."].append(_locations["L"][0])
            x,y = _locations["L"][0]
            i,j = possible_inputs[action]
            if (x+i,y+j) in _locations["T"] and inventory == "x":
                _locations["T"].remove((x+i,y+j))
                inventory = ""
            if (x+i,y+j) in _locations["T"] and inventory == "*":
                inventory = ""
                firespread((x+i,y+j),_locations)
            if 0<=x+i<size[0]-1 and 0<=y+j<size[1]-1 and (x+i,y+j) not in _locations["T"]:
                _locations["L"][0] = (x+i,y+j)
                try:
                    _locations["."].remove(_locations["L"][0])
                except ValueError:
                    pass
                if _locations["L"][0] in _locations["R"]:
                    new_rock = (x+i*2,y+j*2)
                    if new_rock in _locations["~"]:
                        _locations["~"].remove(new_rock)
                        _locations["_"].append(new_rock)
                        _locations["R"].remove(_locations["L"][0])
                    elif new_rock in _locations["."]:
                        _locations["R"].append(new_rock)
                        _locations["."].remove(new_rock)
                        _locations["R"].remove(_locations["L"][0])
                    else:
                        continue
                elif _locations["L"][0] in _locations["~"]:
                    _locations["~"].remove(_locations["L"][0])
                    actions.append((_locations, inventory))
                    actions.append(({}, "Game End"))
                    break
            else:
                continue
        actions.append((_locations, inventory))
        _locations = deepcopy(_locations)
    return actions


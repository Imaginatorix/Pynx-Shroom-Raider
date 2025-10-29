def user_input(size, inventory, original_location, locations):
    commands=tuple(ch for ch in tuple(input("What will you do? ").upper()) if ch !=" ")
    possible_inputs={"W":(-1,0),"A":(0,-1),"S":(1,0),"D":(0,1),"!":None, "P":None,"E":None}
    if not commands:
        return
    actions=[]
    for action in commands:
        if action not in possible_inputs:
            print("Invalid input detected")
            break
        if action == "E":
            actions.append("End")
        elif action == "!":
            locations["L"][0]=original_location
            inventory=""
        elif action=="P":
            if locations["L"][0] not in (*locations["*"], *locations["x"]):
                print("Invalid input detected")
                break
            if inventory:
                locations[inventory].append(locations["L"][0])
                inventory=("*" if locations["L"][0] in locations["*"] else "x")
                locations[inventory].remove(locations["L"][0])
            else:
                inventory=("*" if locations["L"][0] in locations["*"] else "x")
                locations[inventory].remove(locations["L"][0])
        else:
            if :
                locations["."].append(locations["L"][0])
            x,y = locations["L"][0]
            i,j = possible_inputs[action]
            if 0<=x+i<=size[0] and 0<=y+j<=size[1] and (x+i,y+j) not in locations["T"]:
                locations["L"][0] = (x+i,y+j)
                try:
                    locations["."].remove(locations["L"][0])
                except ValueError:
                    pass
            else:
                print("Invalid input detected")
                break
        actions.append((locations, inventory))
    return actions
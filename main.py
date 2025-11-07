#import level size and origloc
#Level Map
from utils.parser import parse_level
from utils.movement import user_input
from utils.ui import show_screen
from time import sleep
from copy import deepcopy


level_info, locations = parse_level(f"levels/spring/Level_1_easy.txt")
locations["_"]=[]
original_locations=deepcopy(locations)
show_screen(level_info, locations)

while True:
    actions = user_input(level_info["size"], level_info["inventory"], locations, original_locations)
    if not actions:
        show_screen(level_info, locations)
        print("Invalid input. Try again.")
    elif "End" in actions[0]:
        level_info["game_end"] = True
    else:
        for current_locations, inventory in actions:
            if not current_locations:
                if not inventory :
                    show_screen(level_info, locations)
                    print("Invalid input detected")
                else:
                    print("You've lost!")
                    level_info["game_end"] = True
                break
            level_info["inventory"] = inventory
            locations = current_locations
            if locations["L"][0] in locations["T"]:
                sleep(0.1)
                show_screen(level_info, locations)
                continue
            if locations["L"][0] in locations["+"]:
                locations["+"].remove(locations["L"][0])
                level_info["mushroom_collected"] += 1
            sleep(0.1)
            show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                print("You've won!")
                level_info["game_end"] = True
                break
            if level_info["game_end"]:
                break
    if level_info["game_end"]:
        print("Game ended!")
        break

#to be added: item and environment interactions
#change logic by splitting inputs into individual characters, check first if valid
#TODO: change name, add testing and fix rocks
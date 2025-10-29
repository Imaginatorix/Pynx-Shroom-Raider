#import level size and origloc
#Level Map
from utils.parser import parse_level
from utils.movement import user_input
from utils.ui import show_screen 

level_info, locations = parse_level(f"levels/spring/Level_1_easy.txt")
show_screen(level_info, locations)

while True:
    actions = user_input(level_info["size"], level_info["inventory"], level_info["original_location"], locations)
    if not actions:
        show_screen(level_info, locations)
        print("Invalid input. Try again.")
    elif "End" in actions[0]:
        level_info["game_end"] = True
    else:
        for current_locations, inventory in actions:
            level_info["inventory"] = inventory
            locations = current_locations
            if locations["L"][0] in locations["T"]:
                show_screen(level_info, locations)
                print("Invalid input. Try again.")
                continue
            if locations["L"][0] in locations["+"]:
                locations["+"].remove(locations["L"][0])
                level_info["mushroom_collected"] += 1
            show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                print("You've won !")
                level_info["game_end"] = True
                break
            if level_info["game_end"]:
                break
    if level_info["game_end"]:
        print("Game ended !")
        break

#to be added: item and environment interactions
#change logic by splitting inputs into individual characters, check first if valid
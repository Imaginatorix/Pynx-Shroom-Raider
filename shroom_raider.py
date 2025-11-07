#import level size and origloc
#Level Map
from utils.parser import parse_level
from utils.parser import parse_output
from utils.movement import user_input
from utils.ui import show_screen
from time import sleep
from copy import deepcopy
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        level_info, locations = parse_level(f"levels/spring/Level_2_difficult.txt")

    else:
        command = ""
        has_own_level = False
        for argument in sys.argv[1:]:
            if argument in ("-f","-m", "-o"):
                command = argument
                continue
            if command == "-f":
                level_info, locations = parse_level(argument)
                has_own_level = True
            elif command == "-m":
                sys_actions = argument
            elif command == "-o":
                output_file = argument
            else:
                if has_own_level:
                    print("here")
                    continue
                print(argument)
                print("Invalid input. Try again.")
                sys.exit()

        

locations["_"] = []
original_locations = deepcopy(locations)

while True:
    if len(sys.argv) > 3:
        actions = user_input(level_info["size"], level_info["inventory"], locations, original_locations, sys_actions)
        has_clear = "NO CLEAR"
    else:
        sys_actions = ""
        show_screen(level_info, locations)
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
                    if len(sys.argv) <= 3:
                        print("You've lost!")
                    level_info["game_end"] = True
                break
            level_info["inventory"] = inventory
            locations = current_locations
            if locations["L"][0] in locations["+"]:
                locations["+"].remove(locations["L"][0])
                level_info["mushroom_collected"] += 1
            if len(sys.argv) <= 3:
                sleep(0.1)
                show_screen(level_info, locations)
            if level_info["mushroom_collected"] == level_info["mushroom_total"]:
                if len(sys.argv) > 3:
                    has_clear = "CLEAR"
                else:
                    print("You've won!")
                level_info["game_end"] = True
                break
    if len(sys.argv) > 3:
        parse_output(output_file, locations, level_info, has_clear)
        break
    if level_info["game_end"]:
        if len(sys.argv) <= 3:
            print("Game ended!")
        break
        

#to be added: item and environment interactions
#change logic by splitting inputs into individual characters, check first if valid
#TODO: change name, add testing and fix rocks
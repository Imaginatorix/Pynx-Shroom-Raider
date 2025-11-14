from utils.parser import parse_level
# from utils.movement import user_input
# from utils.ui import show_screen, create_map_ui
# from time import sleep
# from copy import deepcopy

level_info, locations = parse_level(f"levels/temple/stage6.txt")
# print(level_info)
import pprint
pprint.pprint(locations, width=1000)

# print(create_map_ui(level_info['size'], locations))
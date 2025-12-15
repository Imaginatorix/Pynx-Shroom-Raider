# from utils.parser import parse_level_from_file, save_state

# cur = parse_level_from_file('./levels/fall/stage1.txt')
# save_state('./sample.txt', cur, "NO CLEAR")

from utils.validator import validate_type

validate_type("TEST", 10, str)

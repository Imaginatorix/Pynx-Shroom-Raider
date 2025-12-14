from utils.parser import parse_level_from_file, save_state

cur = parse_level_from_file('./levels/fall/stage1.txt')
save_state('./sample.txt', cur, "NO CLEAR")


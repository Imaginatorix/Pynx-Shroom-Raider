# from utils.parser import parse_level_from_file, save_state

# cur = parse_level_from_file('./levels/fall/stage1.txt')
# save_state('./sample.txt', cur, "NO CLEAR")

# from utils.validator import validate_type

# validate_type("TEST", 10, str)

from utils.parser import get_tile_locations

from pprint import pprint

print(
repr(
get_tile_locations(
    [
        "RRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
        "R...........................R",
        "R.x........................+R",
        "R........RRRRRRRRRRRRRRRRRRRR",
        "R+.R...R.................R.LR",
        "R.R..R.R.RRRRRRRRRRRRRR..R..R",
        "R........TTTTTTTTTTTTTT..RRRR",
        "R.R.RR......................R",
        "R...R....TTTTTTTTTTTTTTTTTTTR",
        "R..R.....TTTTTTTTTTTTTTTTTTTR",
        "RRR....TTT..................R",
        "R.....T~~~T.................R",
        "R.....T~~~T.......*.........R",
        "R.....T~~~T......TTTTTTTTTTTR",
        "R.x....TTT..+....T~~~~~~~~~~R",
        "RRRRRRRRRR.......T~~~~~~~~~~R",
        "RTTTTTTTTR.......TTTTTTTTTTTR",
        "R.+..T..TR..................R",
        "R....T..TR..............x...R",
        "RRRRRR..TR.RRRRRRRRRRRRRRRRRR",
        "R.....+.TR.RTTTTTTTTTTTTTT..R",
        "RTTTT...TR.RT...............R",
        "R........R.RT.....*.TTTTTTTTR",
        "R......RRR.RT.......TTTTTTTTR",
        "RRRRRR.....RT.......TTTTTTTTR",
        "R~~~~R.....RT...............R",
        "R~~~~R.....RRRRRRRRRRRR..+..R",
        "R.RRRRR....RRRRRRRRRRRR.....R",
        "R.....+....R....+...........R",
        "RRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    ],
)).replace(
    "Tile(name='Flamethrower', plain='*', ui='🔥', behaviour=<TileBehaviour.ITEM: 3>)", "FLAMETHROWER_ITEM"
).replace(
    "Tile(name='Tree', plain='T', ui='🌲', behaviour=<TileBehaviour.OBSTACLE: 5>)", "TREE_TILE"
).replace(
    "Tile(name='Rock', plain='R', ui='🪨', behaviour=<TileBehaviour.PUSHABLE: 7>)", "ROCK_TILE"
).replace(
    "Tile(name='Laro Craft', plain='L', ui='🧑', behaviour=<TileBehaviour.PLAYER: 6>)", "LARO_CRAFT_TILE"
).replace(
    "Tile(name='Mushroom', plain='+', ui='🍄', behaviour=<TileBehaviour.GOAL: 2>)", "MUSHROOM_TILE"
).replace(
    "Tile(name='Water', plain='~', ui='🟦', behaviour=<TileBehaviour.DANGER: 1>)", "WATER_TILE"
).replace(
    "Tile(name='Axe', plain='x', ui='🪓', behaviour=<TileBehaviour.ITEM: 3>)", "AXE_ITEM"
).replace(
    "Tile(name='Empty', plain='.', ui='\\u3000', behaviour=<TileBehaviour.WALKABLE: 8>)", "EMPTY_TILE"
).replace(
    "Tile(name='Pave', plain='_', ui='⬜', behaviour=<TileBehaviour.WALKABLE: 8>)", "PAVED_TILE"
))

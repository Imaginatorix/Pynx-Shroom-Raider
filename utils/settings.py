from utils.custom_types import Tile, TileBehaviour

MAP_INSTRUCTIONS_GAP = 5
SPACE = '\U00003000'

# === ASCII ===
# TILES
EMPTY_TILE = Tile('Empty', '.', SPACE, TileBehaviour.WALKABLE)
LARO_CRAFT_TILE = Tile('Laro Craft', 'L', '🧑', TileBehaviour.PLAYER)
TREE_TILE = Tile('Tree', 'T', '🌲', TileBehaviour.OBSTACLE)
MUSHROOM_TILE = Tile('Mushroom', '+', '🍄', TileBehaviour.GOAL)
ROCK_TILE = Tile('Rock', 'R', '🪨', TileBehaviour.PUSHABLE)
WATER_TILE = Tile('Water', '~', '🟦', TileBehaviour.DANGER)
PAVED_TILE = Tile('Pave', '_', '⬜', TileBehaviour.WALKABLE)
# ITEMS
AXE_ITEM = Tile('Axe', 'x', '🪓', TileBehaviour.ITEM)
FLAMETHROWER_ITEM = Tile('Flamethrower', '*', '🔥', TileBehaviour.ITEM)


# SET OF ALL VALID TILES
VALID_TILES = {
    EMPTY_TILE,
    LARO_CRAFT_TILE,
    TREE_TILE,
    MUSHROOM_TILE,
    ROCK_TILE,
    WATER_TILE,
    PAVED_TILE,
    AXE_ITEM,
    FLAMETHROWER_ITEM,
}


# PLAINTEXT TO TILE CONVERSION
PLAIN_TO_TILE = {
    tile.plain: tile
    for tile in VALID_TILES
}

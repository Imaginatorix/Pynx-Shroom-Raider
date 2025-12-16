"""
Constants used in the game including:

- MAP_INSTRUCTIONS_GAP: How far the map and the instructions are when printing to screen
- SPACE: The symbol used for empty space
- Tile and Item definitions for the game map
    Tiles:
        - EMPTY_TILE ('\U00003000')
        - LARO_CRAFT_TILE (🧑)
        - TREE_TILE (🌲)
        - MUSHROOM_TILE (🍄)
        - ROCK_TILE (🪨)
        - WATER_TILE (🟦)
        - PAVED_TILE (⬜)
    Items:
        - AXE_ITEM (🪓)
        - FLAMETHROWER_ITEM (🔥)
- VALID_TILES: The set of all usable tiles
- PLAIN_TO_TILE: Mapping from plaintext grid characters to their corresponding Tile objects.
"""

from utils.custom_types import Tile, TileBehaviour


# === PRINTING CONSTANTS ===
MAP_INSTRUCTIONS_GAP = 5
# === EMPTY SPACE CHARACTER (FOR UNIFORM WIDTH) ===
SPACE = '\U00003000'

# === TILE DEFINITIONS ===
# Tile definitions for all elements, player, and item types.
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
# NONE PLACEHOLDER
NONE_TILE: Tile = Tile('', '', '', TileBehaviour.NONE)


# SET OF ALL VALID TILES
# The set of all usable tiles.
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
# Mapping from plaintext grid characters to their corresponding Tile objects.
PLAIN_TO_TILE = {
    tile.plain: tile
    for tile in VALID_TILES
}

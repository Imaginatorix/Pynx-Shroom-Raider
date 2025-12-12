from __future__ import annotations
from dataclasses import dataclass
from validator import validate_size, validate_level_info, validate_locations

# ===== CUSTOM CLASSES USED THROUGHOUT THE GAME =====

# === TILE REPRESENTATION ===
@dataclass(frozen=True)
class Tile():
    """
    Representation of different tiles found in the game

    Parameters
    ----------
    name: str
        The name of the tile.
    plain : str
        Plaintext or ASCII representation of the tile to be read from a .txt file.
    ui : str
        UI representation of the tile to be printed on the shell.
    walkable : bool
        Whether the player can walk on top of it.

    Attributes
    ----------
    name: str
        The name of the tile.
    plain : str
        Plaintext or ASCII representation of the tile to be read from a .txt file.
    ui : str
        UI representation of the tile to be printed on the shell.
    walkable : bool
        Whether the player can walk on top of it.

    """
    name: str
    plain: str
    ui: str
    walkable: bool


# === LEVELSTATE REPRESENTATION ===
class LevelState():
    """
    Representation of state of the level

    Parameters
    ----------
    size : tuple[int, int]
        The size of the map.
    mushroom_collected: int
        The number of mushroom collected so far.
    mushroom_total : int
        The number of mushroom needed to be collected to win the game.
    game_end : bool
        Whether the game is already over.
    inventory : str
        The current item in the player's inventory.
    invalid_input : bool
        Whether the player has made an invalid input.
    level_reset : bool
        Whether the level has been resetted.
    locations : dict[Tile, set]
        Maps the Tile to the set of coordinates where it is found

    """

    def __init__(self,
                 size: tuple[int, int],
                 mushroom_collected: bool,
                 mushroom_total: bool,
                 game_end: bool,
                 inventory: str,
                 invalid_input: bool,
                 level_reset: bool,
                 locations: dict[Tile, set]
                ) -> None:

        # Validate input
        ...

        # Set into private attributes
        self._size = size
        self._mushroom_collected = mushroom_collected
        self._mushroom_total = mushroom_total
        self._game_end = game_end
        self._inventory = inventory
        self._invalid_input = invalid_input
        self._level_reset = level_reset
        self._locations = locations

    @classmethod
    def parse_level(cls, size: tuple[int, int], grid: list[list[Tile]], target_tile: Tile) -> LevelState:
        locations = {}
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c not in locations:
                    locations[c] = set()
                locations[c].add((i, j))

        mushroom_collected = False
        mushroom_collected = 0
        mushroom_total = len(locations[target_tile])
        game_end = False
        inventory = ""
        invalid_input = False
        level_reset = False

        return cls(size, mushroom_collected, mushroom_total, game_end, inventory, invalid_input, level_reset, locations)


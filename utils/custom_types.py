from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
# from validator import validate_size, validate_level_info, validate_locations

# ===== CUSTOM CLASSES USED THROUGHOUT THE GAME =====

# === TILE BEHAVIOUR ===
class TileBehaviour(Enum):
    """Enum to identify the behaviour of the tile"""
    DANGER = auto()
    GOAL = auto()
    ITEM = auto()
    OBSTACLE = auto()
    PLAYER = auto()
    PUSHABLE = auto()
    WALKABLE = auto()


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
    behaviour : TileBehaviour
        The behaviour of the tile when being interacted by the user

    Attributes
    ----------
    name: str
        The name of the tile.
    plain : str
        Plaintext or ASCII representation of the tile to be read from a .txt file.
    ui : str
        UI representation of the tile to be printed on the shell.
    behaviour : TileBehaviour
        The behaviour of the tile when being interacted by the user

    """
    name: str
    plain: str
    ui: str
    behaviour: TileBehaviour


# === LEVELSTATE REPRESENTATION ===
class LevelState():
    """
    Representation of state of the level

    Parameters
    ----------
    size : tuple[int, int]
        The size of the map.
    mushroom_total : int
        The number of mushroom needed to be collected to win the game.
    locations : dict[Tile, set]
        Maps the Tile to the set of coordinates where it is found.
    mushroom_collected: int, default=0
        The number of mushroom collected so far.
    game_end : bool, default=False
        Whether the game is already over.
    inventory : str, default=""
        The current item in the player's inventory.
    invalid_input : bool, default=False
        Whether the player has made an invalid input.
    level_reset : bool, default=False
        Whether the level has been resetted.

    """

    def __init__(self,
                 size: tuple[int, int],
                 mushroom_total: bool,
                 locations: dict[Tile, set],
                 mushroom_collected: bool = 0,
                 game_end: bool = False,
                 inventory: str = "",
                 invalid_input: bool = False,
                 level_reset: bool = False,
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

    def __repr__(self) -> str:
        """
        Returns grid representation of the level state.
        """
        r, c = self._size
        grid = [[None]*c for _ in range(r)]

        for c, coord in self._locations.items():
            for i, j in coord:
                if not grid[i][j] or c == 'L':
                    grid[i][j] = c.ui

        return '\n'.join([''.join(row) for row in grid])

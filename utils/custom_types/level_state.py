from __future__ import annotations

from .tile import Tile
from .tile_behaviour import TileBehaviour

# === LEVELSTATE REPRESENTATION ===
class LevelState():
    """
    TODO: Representation of state of the level

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
    covering: Tile, default=Tile(name='None', plain='?', ui='?', behaviour=TileBehaviour.NONE),
        The current item the player is on top of.
    inventory : Tile, default=Tile(name='None', plain='?', ui='?', behaviour=TileBehaviour.NONE)
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
                 covering: Tile | None = None,
                 inventory: Tile | None = None,
                 invalid_input: bool = False,
                 level_reset: bool = False,
                ) -> None:

        # Validate input
        ...

        # Set into private attributes
        self.size = size
        self.mushroom_collected = mushroom_collected
        self.mushroom_total = mushroom_total
        self.game_end = game_end
        self.covering = covering
        self.inventory = inventory
        self.invalid_input = invalid_input
        self.level_reset = level_reset
        self.locations = locations

        self.modified = True
        self.grid = None
        self.draw_grid()


    def draw_grid(self) -> str:
        """TODO: Returns grid representation of the level state."""
        if self.modified or self.grid is None:
            r, c = self.size
            grid = [['']*c for _ in range(r)]

            CHARACTER_TILE = [tile for tile in self.locations if tile.behaviour is TileBehaviour.PLAYER][0]
            WALKABLE_TILES = set(tile for tile in self.locations if tile.behaviour is TileBehaviour.WALKABLE)
            character_location = next(iter(self.locations[CHARACTER_TILE]))

            for c, coord in self.locations.items():
                for i, j in coord:
                    if (i, j) == character_location and c not in {(CHARACTER_TILE,)} | WALKABLE_TILES and c.behaviour is TileBehaviour.ITEM:
                        self.covering = c
                    # Set cell to higher priority (for now, only character)
                    if not grid[i][j] or c == CHARACTER_TILE:
                        grid[i][j] = c.ui

            self.modified = False
            self.grid = '\n'.join([''.join(row) for row in grid])

        return self.grid


    def __repr__(self) -> str:
        """TODO: Returns grid representation of the level state."""
        return self.draw_grid()


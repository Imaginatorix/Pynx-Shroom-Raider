from __future__ import annotations

from .tile import Tile
from .tile_behaviour import TileBehaviour
from copy import deepcopy

# TODO:
# TILES
EMPTY_TILE = Tile('Empty', '.', '\U00003000', TileBehaviour.WALKABLE)
LARO_CRAFT_TILE = Tile('Laro Craft', 'L', '🧑', TileBehaviour.PLAYER)
TREE_TILE = Tile('Tree', 'T', '🌲', TileBehaviour.OBSTACLE)
MUSHROOM_TILE = Tile('Mushroom', '+', '🍄', TileBehaviour.GOAL)
ROCK_TILE = Tile('Rock', 'R', '🪨', TileBehaviour.PUSHABLE)
WATER_TILE = Tile('Water', '~', '🟦', TileBehaviour.DANGER)
PAVED_TILE = Tile('Pave', '_', '⬜', TileBehaviour.WALKABLE)
# ITEMS
AXE_ITEM = Tile('Axe', 'x', '🪓', TileBehaviour.ITEM)
FLAMETHROWER_ITEM = Tile('Flamethrower', '*', '🔥', TileBehaviour.ITEM)



# === LEVELSTATE REPRESENTATION ===
class LevelState():
    """
    Encapsulates the current state of a level.

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
                 covering: Tile,
                 inventory: Tile,
                 mushroom_collected: bool = 0,
                 game_end: bool = False,
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
        self._covering = covering
        self._inventory = inventory
        self._invalid_input = invalid_input
        self._level_reset = level_reset
        self._locations = locations

        self._original_state = self.get_state()

        # self._modified = True

    # === GETTERS AND SETTERS FOR THE ATTRIBUTES OF LEVELSTATE ===

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @property
    def mushroom_collected(self) -> int:
        return self._mushroom_collected

    @property
    def mushroom_total(self) -> int:
        return self._mushroom_total

    @property
    def game_end(self) -> bool:
        """
        Returns if the game has ended.
        """
        return self._game_end

    @property
    def covering(self) -> Tile:
        return self._covering

    @property
    def inventory(self) -> Tile:
        """
        Returns the value of _inventory attribute.
        """
        return self._inventory

    @property
    def invalid_input(self) -> bool:
        """Returns the value of _invalid_input attribute."""
        return self._invalid_input

    @invalid_input.setter
    def invalid_input(self, val: bool) -> None:
        """
        Updates the _invalid_input attribute.

        Parameters
        ----------
        val: bool 
            The bool value that will be assigned to _invalid_input
        """ 
        self._invalid_input = val


    @property
    def level_reset(self) -> bool:
        return self._level_reset

    @property
    def locations(self) -> dict[Tile, set[tuple[int, int]]]:
        return self._locations

    @property
    def grid_ui(self) -> str:
        """TODO: Returns grid representation of the level state."""
        # if self.modified:
        r, c = self._size
        grid = [['']*c for _ in range(r)]

        CHARACTER_TILE = [tile for tile in self._locations if tile.behaviour is TileBehaviour.PLAYER][0]
        WALKABLE_TILES = set(tile for tile in self._locations if tile.behaviour is TileBehaviour.WALKABLE)
        character_location = next(iter(self._locations[CHARACTER_TILE]))

        for c, coord in self._locations.items():
            for i, j in coord:
                if (i, j) == character_location and c not in {CHARACTER_TILE,} | WALKABLE_TILES and c.behaviour is TileBehaviour.ITEM:
                    self._covering = c
                # Set cell to higher priority (for now, only character)
                if not grid[i][j] or c == CHARACTER_TILE:
                    grid[i][j] = c.ui
        
        return [''.join(row) for row in grid]

    @property
    def grid_ascii(self) -> str:
        """TODO: Returns grid representation of the level state."""
        # if self.modified:
        r, c = self._size
        grid = [['']*c for _ in range(r)]

        CHARACTER_TILE = [tile for tile in self._locations if tile.behaviour is TileBehaviour.PLAYER][0]
        WALKABLE_TILES = set(tile for tile in self._locations if tile.behaviour is TileBehaviour.WALKABLE)
        character_location = next(iter(self._locations[CHARACTER_TILE]))

        for c, coord in self._locations.items():
            for i, j in coord:
                if (i, j) == character_location and c not in {CHARACTER_TILE,} | WALKABLE_TILES and c.behaviour is TileBehaviour.ITEM:
                    self._covering = c
                # Set cell to higher priority (for now, only character)
                if not grid[i][j] or c == CHARACTER_TILE:
                    grid[i][j] = c.plain
        
        return [''.join(row) for row in grid]

    @property
    def tile_classification(self) -> dict[TileBehaviour, set]:
        tile_classification = {
            behaviour: set()
            for behaviour in TileBehaviour
        }

        for tile in self._locations:
            tile_classification[tile.behaviour].add(tile)
        
        return tile_classification

    # === END OF GETTERS AND SETTERS FOR THE ATTRIBUTES OF LEVELSTATE ====

    def reset_state(self) -> None:
        """
        Revert the LevelState object into its original state.
        """
        self = self._original_state.get_state() # TODO: Test pa


    def is_valid_item_tile(self) -> bool:
        """
        Returns if the player can pick up an item on the current tile
        """
        return self._inventory is None and self._covering is not None and self._covering.behaviour is TileBehaviour.ITEM


    def pick_item(self) -> None:
        """
        Updates the _inventory attribute based on the current tile.
        """
        player_location = next(iter(self._locations[LARO_CRAFT_TILE]))
        self._inventory = self._covering
        self._locations[self._inventory].remove(player_location)


    def next_player_location(self, action: tuple[int,int]) -> tuple[tuple[int, int], Tile]:
        """
        Return new player location and tile.

        Parameters
        ----------
        action: tuple[int, int] 
            Movement of the player

        Returns
        -------
        tuple[tuple[int, int], Tile]
            New player position and the next tile the player is on after moving.
        """ 
        new_location = next(iter(self._locations[LARO_CRAFT_TILE]))[0] + action[0], next(iter(self._locations[LARO_CRAFT_TILE]))[1] + action[1]
        new_tile = EMPTY_TILE
        for name, s in self._locations.items():
            if new_location in s and name is not LARO_CRAFT_TILE:
                 new_tile = name
        return new_location, new_tile


    def is_valid_movement(self, action: tuple[int,int]) -> bool:
        """
        Check if movement is possible.

        Parameters
        ----------
        action: tuple[int, int] 
            Movement of the player

        Returns
        -------
        bool
            True if movement is possible
        """ 
        new_player_location, next_tile = self.next_player_location(action)
        if not (0<=new_player_location[0]<self._size[0] and 0<=new_player_location[1]<self._size[1]):
            return False
        elif next_tile.behaviour is not TileBehaviour.OBSTACLE:
            return True
        elif next_tile.behaviour is TileBehaviour.OBSTACLE and self._inventory:
            return True
        else:
            return False
    

    def use_axe(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove single tree on the new player location.

        Parameters
        ----------
        new_player_location: tuple[int, int] 
            New position of the player
        """
        self._locations[TREE_TILE].remove(new_player_location)
        self._inventory = None
        self._covering = None


    def use_fire(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove affected trees on the new player location.

        Parameters
        ----------
        new_player_location: tuple[int, int] 
            New position of the player
        """
        self._inventory = None
        self._covering = None
        kernel = ((-1,0), (0,-1), (1,0), (0,1))
        frontier = [new_player_location]
        n = 0

        # Keep removing trees until there are no more adjacent trees
        while n < len(frontier):
            i, j = frontier[n]
            for di, dj in kernel:
                new = (di + i, dj + j)
                if new in self._locations[TREE_TILE]:
                    frontier.append(new)
                    self._locations[TREE_TILE].remove(new)
                    self._locations[EMPTY_TILE].add(new)
            n+=1


    def push_rock(self, curr_rock_location: tuple[int, int],action: tuple[int,int]) -> None:
        """
        Try to push a rock.

        Parameters
        ----------
        curr_rock_location: tuple[int, int] 
            Current position of the rock that will be pushed
        action: tuple[int, int] 
            Movement of the player

        Raises
        ------
        ValueError
            If the new rock position is invalid
        """
        new_rock_location = (next(iter(self._locations[LARO_CRAFT_TILE]))[0] + action[0]*2, 
                             next(iter(self._locations[LARO_CRAFT_TILE]))[1] + action[1]*2)
        
        if new_rock_location in self._locations[EMPTY_TILE]:
            # Remove empty tile in new position
            self._locations[ROCK_TILE].add(new_rock_location)
            self._locations[ROCK_TILE].remove(curr_rock_location)
            self._locations[EMPTY_TILE].remove(new_rock_location)
        elif new_rock_location in self._locations[PAVED_TILE]:
            self._locations[ROCK_TILE].add(new_rock_location)
            self._locations[ROCK_TILE].remove(curr_rock_location)
        elif new_rock_location in self._locations[WATER_TILE]:
            # Remove water tile in new position and add paved tile
            self._locations[WATER_TILE].remove(new_rock_location)
            self._locations[ROCK_TILE].remove(curr_rock_location)
            self._locations[PAVED_TILE].add(new_rock_location)
        else:
            raise ValueError
   

    def game_end(self) -> None:
        """
        Updates the _game_end attribute to True.
        """
        self._game_end = True

    def game_lose(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove the water tile on new player location and call game_end method
        """
        self._locations[WATER_TILE].remove(new_player_location)
        self.game_end()


    def collect_mushroom(self, new_player_location: tuple[int, int]) -> None:
        """
        Removes the retrieved mushroom and increase the _mushroom_collected attribute.
        """
        self._locations[MUSHROOM_TILE].remove(new_player_location)
        self._mushroom_collected += 1


    def check_win(self) -> bool:
        """
        Returns if the player has won.
        """
        return self._mushroom_collected == self._mushroom_total


    def set_player_location(self, new_player_location: tuple[int, int]) -> None:
        """
        Updates the _locations[LARO_CRAFT_TILE] attribute to new player position.
        """
        if not self._covering:
            self._locations[EMPTY_TILE].add(next(iter(self._locations[LARO_CRAFT_TILE])))
        try:
            self._locations[EMPTY_TILE].remove(new_player_location)
        except KeyError:
            pass
        self._locations[LARO_CRAFT_TILE] = {new_player_location}


    def get_state(self) -> LevelState:
        """Returns a duplicate of the level state."""
        return deepcopy(self)


    def __repr__(self) -> str:
        """Returns grid-like string representation of the level state separated by endlines."""
        return '\n'.join(self.grid)

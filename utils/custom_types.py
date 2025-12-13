from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import utils.settings as TILES

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

    def get_state(self) -> LevelState:
        """
        Returns a duplicate of the level state.
        """
        clone = LevelState.__new__(LevelState)
        clone._locations = {k: set(v) for k, v in self._locations.items()}
        return clone # TODO: test

    def __init__(self,
                 size: tuple[int, int],
                 mushroom_total: bool,
                 locations: dict[Tile, set],
                 mushroom_collected: int = 0,
                 game_end: bool = False,
                 inventory: Tile = TILES.EMPTY_ITEM,
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
        self._original_state = self.get_state()

    def __repr__(self) -> str:
        """
        Returns grid representation of the level state.
        """
        r, c = self._size
        grid = [[""]*c for _ in range(r)]

        for t, coord in self._locations.items():
            for i, j in coord:
                if not grid[i][j] or t == 'L':
                    grid[i][j] = t.ui

        return '\n'.join([''.join(row) for row in grid])
    
    def set_invalid_input(self, val: bool) -> None:
        """
        Updates the _invalid_input attribute.

        Parameters
        ----------
        val: bool 
            The bool value that will be assigned to _invalid_input
        """ 
        self._invalid_input = val

    def get_invalid_input(self) -> bool:
        """
        Returns the value of _invalid_input attribute.
        """
        return self._invalid_input

    def get_inventory(self) -> Tile:
        """
        Returns the value of _inventory attribute.
        """
        return self._inventory
    
    def reset_state(self) -> None:
        """
        Revert the LevelState object into its original state.
        """
        self = self._original_state.get_state() # TODO: Test pa
    
    def is_valid_item_tile(self) -> bool:
        """
        Returns if the player can pick up an item on the current tile
        """
        return self._inventory is TILES.EMPTY_ITEM and next(iter(self._locations[TILES.LARO_CRAFT_TILE])) in self._locations[TILES.AXE_ITEM] | self._locations[TILES.FLAMETHROWER_ITEM]

    def pick_item(self) -> None:
        """
        Updates the _inventory attribute based on the current tile.
        """
        player_location = next(iter(self._locations[TILES.LARO_CRAFT_TILE]))
        self._inventory = TILES.AXE_ITEM if player_location in self._locations[TILES.AXE_ITEM] else TILES.FLAMETHROWER_ITEM
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
        new_location = next(iter(self._locations[TILES.LARO_CRAFT_TILE]))[0] + action[0], next(iter(self._locations[TILES.LARO_CRAFT_TILE]))[1] + action[1]
        new_tile = TILES.EMPTY_TILE
        for name, s in self._locations.items():
            if new_location in s and s is not TILES.LARO_CRAFT_TILE:
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
        new_player_location, _ = self.next_player_location(action)
        return ((new_player_location not in self._locations[TILES.TREE_TILE] or 
                self._inventory != TILES.EMPTY_ITEM) and
                0<=new_player_location[0]<self._size[0] and 0<=new_player_location[1]<self._size[1])
    
    def use_axe(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove single tree on the new player location.

        Parameters
        ----------
        new_player_location: tuple[int, int] 
            New position of the player
        """
        self._locations[TILES.TREE_TILE].remove(new_player_location)
        self._inventory = TILES.EMPTY_ITEM

    def use_fire(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove affected trees on the new player location.

        Parameters
        ----------
        new_player_location: tuple[int, int] 
            New position of the player
        """
        self._inventory = TILES.EMPTY_ITEM
        kernel = ((-1,0),(0,-1),(1,0),(0,1))
        frontier = [new_player_location]
        n = 0

        # Keep removing trees until there are no more adjacent trees
        while n < len(frontier):
            i, j = frontier[n]
            for di, dj in kernel:
                new = (di + i, dj + j)
                if new in self._locations[TILES.TREE_TILE]:
                    self._locations[TILES.TREE_TILE].remove(new)
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
        new_rock_location = (next(iter(self._locations[TILES.LARO_CRAFT_TILE]))[0] + action[0]*2, 
                             next(iter(self._locations[TILES.LARO_CRAFT_TILE]))[1] + action[1]*2)
        
        # Push rock
        self._locations[TILES.ROCK_TILE].add(new_rock_location)
        self._locations[TILES.ROCK_TILE].remove(curr_rock_location)
        
        if new_rock_location in self._locations[TILES.EMPTY_TILE]:
            # Remove empty tile in new position
            self._locations[TILES.EMPTY_TILE].remove(new_rock_location)
        elif new_rock_location in self._locations[TILES.PAVED_TILE]:
            pass
        elif new_rock_location in self._locations[TILES.WATER_TILE]:
            # Remove water tile in new position and add paved tile
            self._locations[TILES.WATER_TILE].remove(new_rock_location)
            self._locations[TILES.ROCK_TILE].remove(new_rock_location)
            self._locations[TILES.PAVED_TILE].add(new_rock_location)
        else:
            # Revert change if new position in other tiles
            self._locations[TILES.ROCK_TILE].remove(new_rock_location)
            self._locations[TILES.ROCK_TILE].add(new_rock_location)
            raise ValueError
   
    def game_end(self) -> None:
        """
        Updates the _game_end attribute to True.
        """
        self._game_end == True

    def game_lose(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove the water tile on new player location and call game_end method
        """
        self._locations[TILES.WATER_TILE].remove(new_player_location)
        self.game_end()

    def collect_mushroom(self, new_player_location: tuple[int, int]) -> None:
        """
        Removes the retrieved mushroom and increase the _mushroom_collected attribute.
        """
        self._locations[TILES.MUSHROOM_TILE].remove(new_player_location)
        self._mushroom_collected += 1

    def check_win(self) -> bool:
        """
        Returns if the player has won.
        """
        return self._mushroom_collected == self._mushroom_total
    
    def check_game_end(self) -> bool:
        """
        Returns if the game has ended.
        """
        return self._game_end

    def set_player_location(self, new_player_location: tuple[int, int]) -> None:
        """
        Updates the _locations[TILES.LARO_CRAFT_TILE] attribute to new player position.
        """
        self._locations[TILES.EMPTY_TILE].add(next(iter(self._locations[TILES.LARO_CRAFT_TILE])))
        try:
            self._locations[TILES.EMPTY_TILE].remove(new_player_location)
        except KeyError:
            pass
        self._locations[TILES.LARO_CRAFT_TILE] = {new_player_location}
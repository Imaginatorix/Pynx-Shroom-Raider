from __future__ import annotations

from .tile import Tile
from .tile_behaviour import TileBehaviour
from copy import deepcopy


# === LEVELSTATE REPRESENTATION ===
class LevelState():
    def __init__(self,
                 size: tuple[int, int],
                 mushroom_total: int,
                 locations: dict[Tile, set],
                 covering: Tile,
                 inventory: Tile,
                 mushroom_collected: int = 0,
                 game_end: bool = False,
                 invalid_input: bool = False,
                ) -> None:
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
        """
        # Set into private attributes
        self._size = size
        self._mushroom_collected = mushroom_collected
        self._mushroom_total = mushroom_total
        self._game_end = game_end
        self._covering = covering
        self._inventory = inventory
        self._invalid_input = invalid_input
        self._locations = locations

        # Other Attributes used within internal methods
        # === SET UP TILE ===
        self.TILE_DISPLAY_PRIORITY = {
            TileBehaviour.NONE: 0,
            TileBehaviour.WALKABLE: 1,
            TileBehaviour.DANGER: 2,
            TileBehaviour.ITEM: 3,
            TileBehaviour.GOAL: 4,
            TileBehaviour.PUSHABLE: 5,
            TileBehaviour.PLAYER: 6,
            TileBehaviour.OBSTACLE: 7,
        }

        # TILES
        self.EMPTY_TILE = Tile('Empty', '.', '\U00003000', TileBehaviour.WALKABLE)
        self.LARO_CRAFT_TILE = Tile('Laro Craft', 'L', '🧑', TileBehaviour.PLAYER)
        self.TREE_TILE = Tile('Tree', 'T', '🌲', TileBehaviour.OBSTACLE)
        self.MUSHROOM_TILE = Tile('Mushroom', '+', '🍄', TileBehaviour.GOAL)
        self.ROCK_TILE = Tile('Rock', 'R', '🪨', TileBehaviour.PUSHABLE)
        self.WATER_TILE = Tile('Water', '~', '🟦', TileBehaviour.DANGER)
        self.PAVED_TILE = Tile('Pave', '_', '⬜', TileBehaviour.WALKABLE)
        # ITEMS
        self.AXE_ITEM = Tile('Axe', 'x', '🪓', TileBehaviour.ITEM)
        self.FLAMETHROWER_ITEM = Tile('Flamethrower', '*', '🔥', TileBehaviour.ITEM)
        # NONE PLACEHOLDER
        self.NONE_TILE = Tile('', '', '', TileBehaviour.NONE)

    # === GETTERS AND SETTERS FOR THE ATTRIBUTES OF LEVELSTATE ===

    @property
    def size(self) -> tuple[int, int]:
        """Returns the size of map (row, col)."""
        return self._size

    @property
    def mushroom_collected(self) -> int:
        """Returns how many mushroom the player has retrieved."""
        return self._mushroom_collected

    @property
    def mushroom_total(self) -> int:
        """Returns how many mushroom is in the map."""
        return self._mushroom_total

    @property
    def game_end(self) -> bool:
        """Returns if the game has ended."""
        return self._game_end
    
    @game_end.setter
    def game_end(self, val: bool) -> None:
        """Updates the _game_end attribute."""
        self._game_end = val

    @property
    def inventory(self) -> Tile:
        """Returns the value of _inventory attribute."""
        return self._inventory

    @property
    def invalid_input(self) -> bool:
        """Returns the value of _invalid_input attribute."""
        return self._invalid_input

    @invalid_input.setter
    def invalid_input(self, val: bool) -> None:
        """Updates the _invalid_input attribute.""" 
        self._invalid_input = val
    
    @property
    def covering(self) -> Tile:
        """Returns the tile the player is on."""
        return self._covering
    
    @covering.setter
    def covering(self, val: Tile) -> None:
        """Updates the _covering attribute."""
        self._covering = val

    @property
    def locations(self) -> dict[Tile, set[tuple[int, int]]]:
        """Returns the _locations dictionary containing all locations of tiles."""
        return self._locations

    @property
    def grid_ui(self) -> list[str]:
        """Returns ASCII grid representation of the level state."""
        # if self.modified:
        r, c = self._size
        grid = [['']*c for _ in range(r)]
        grid_tile = [[self.NONE_TILE]*c for _ in range(r)]

        for tile, coord in self._locations.items():
            for i, j in coord:
                # Set cell to higher priority (for now, only character)
                if not grid[i][j] or self.TILE_DISPLAY_PRIORITY[tile.behaviour] > self.TILE_DISPLAY_PRIORITY[grid_tile[i][j].behaviour]:
                    grid_tile[i][j] = tile
                    grid[i][j] = tile.ui
        
        return [''.join(row) for row in grid]

    @property
    def grid_ascii(self) -> list[str]:
        """Returns UI grid representation of the level state."""
        # if self.modified:
        r, c = self._size
        grid = [['']*c for _ in range(r)]
        grid_tile = [[self.NONE_TILE]*c for _ in range(r)]

        for tile, coord in self._locations.items():
            for i, j in coord:
                # Set cell to higher priority (for now, only character)
                if not grid[i][j] or self.TILE_DISPLAY_PRIORITY[tile.behaviour] > self.TILE_DISPLAY_PRIORITY[grid_tile[i][j].behaviour]:
                    grid_tile[i][j] = tile
                    grid[i][j] = tile.plain

        return [''.join(row) for row in grid]

    # === END OF GETTERS AND SETTERS FOR THE ATTRIBUTES OF LEVELSTATE ====

    def is_valid_item_tile(self) -> bool:
        """Returns if the player can pick up an item on the current tile"""
        return self._inventory.behaviour is TileBehaviour.NONE and self._covering.behaviour is TileBehaviour.ITEM


    def pick_item(self) -> None:
        """Updates the _inventory attribute based on the current tile."""
        player_location = next(iter(self._locations[self.LARO_CRAFT_TILE]))
        self._inventory = self._covering
        self._covering = self.NONE_TILE
        self._locations[self._inventory].remove(player_location)
        self._locations[self.EMPTY_TILE].add(player_location)


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
        new_location = next(iter(self._locations[self.LARO_CRAFT_TILE]))[0] + action[0], next(iter(self._locations[self.LARO_CRAFT_TILE]))[1] + action[1]
        new_tile = self.EMPTY_TILE
        for name, s in self._locations.items():
            if new_location in s and name is not self.LARO_CRAFT_TILE:
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
        elif next_tile.behaviour is TileBehaviour.OBSTACLE and self._inventory.behaviour is TileBehaviour.ITEM:
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
        self._locations[self.TREE_TILE].remove(new_player_location)
        self._inventory = self.NONE_TILE
        self._covering = self.NONE_TILE


    def use_fire(self, new_player_location: tuple[int, int]) -> None:
        """
        Remove affected trees on the new player location.

        Parameters
        ----------
        new_player_location: tuple[int, int] 
            New position of the player
        """
        self._inventory = self.NONE_TILE
        self._covering = self.NONE_TILE
        kernel = ((-1,0), (0,-1), (1,0), (0,1))
        frontier = [new_player_location]
        n = 0

        # Keep removing trees until there are no more adjacent trees
        while n < len(frontier):
            i, j = frontier[n]
            for di, dj in kernel:
                new = (di + i, dj + j)
                if new in self._locations[self.TREE_TILE]:
                    frontier.append(new)
                    self._locations[self.TREE_TILE].remove(new)
                    self._locations[self.EMPTY_TILE].add(new)
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
        new_rock_location = (next(iter(self._locations[self.LARO_CRAFT_TILE]))[0] + action[0]*2, 
                             next(iter(self._locations[self.LARO_CRAFT_TILE]))[1] + action[1]*2)
        if new_rock_location in self._locations[self.WATER_TILE]:
            # Remove water tile in new position and add paved tile
            self._locations[self.WATER_TILE].remove(new_rock_location)
            self._locations[self.ROCK_TILE].remove(curr_rock_location)
            self._locations[self.PAVED_TILE].add(new_rock_location)
        elif new_rock_location in self._locations[self.PAVED_TILE]:
            self._locations[self.ROCK_TILE].add(new_rock_location)
            self._locations[self.ROCK_TILE].remove(curr_rock_location)
        elif new_rock_location in self._locations[self.EMPTY_TILE]:
            # Remove empty tile in new position
            self._locations[self.ROCK_TILE].add(new_rock_location)
            self._locations[self.ROCK_TILE].remove(curr_rock_location)
            self._locations[self.EMPTY_TILE].remove(new_rock_location)
        else:
            raise ValueError
   
    def game_lose(self, new_player_location: tuple[int, int]) -> None:
        """Remove the water tile on new player location and call game_end method"""
        self._locations[self.WATER_TILE].remove(new_player_location)
        self._game_end = True

    def collect_mushroom(self, new_player_location: tuple[int, int]) -> None:
        """Removes the retrieved mushroom and increase the _mushroom_collected attribute."""
        self._locations[self.MUSHROOM_TILE].remove(new_player_location)
        self._mushroom_collected += 1


    def check_win(self) -> bool:
        """Returns if the player has won."""
        return self._mushroom_collected == self._mushroom_total


    def set_player_location(self, new_player_location: tuple[int, int]) -> None:
        """Updates the _locations[LARO_CRAFT_TILE] attribute to new player position."""
        if (self._covering.behaviour is not TileBehaviour.ITEM and 
            next(iter(self._locations[self.LARO_CRAFT_TILE])) not in self._locations[self.PAVED_TILE]):
            self._locations[self.EMPTY_TILE].add(next(iter(self._locations[self.LARO_CRAFT_TILE])))
        try:
            self._locations[self.EMPTY_TILE].remove(new_player_location)
        except KeyError:
            pass
        self._locations[self.LARO_CRAFT_TILE] = {new_player_location}

    # === STATE OPERATORS ===

    def get_state(self) -> LevelState:
        """Returns a duplicate of the level state."""
        return deepcopy(self)

    def reset_state(self, orig_state: LevelState) -> None:
        """Resets the level state to its original state."""
        self.__dict__ = deepcopy(orig_state.__dict__)

    # === END OF STATE OPERATORS ===

    def __repr__(self) -> str:
        """Returns grid-like string representation of the level state separated by endlines."""
        return '\n'.join(self.grid_ui)

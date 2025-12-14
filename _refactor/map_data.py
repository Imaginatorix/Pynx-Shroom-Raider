from __future__ import annotations
from typing import TypedDict, Tuple, cast

class LevelInfo(TypedDict):
    """
    A class representing the type-hinting of level_info dict.
    """
    size: Tuple[int, int]
    mushroom_collected: int
    mushroom_total: int
    game_end: bool
    inventory: str
    invalid_input: bool
    level_reset: bool

class MapData: # TODO: change to LevelState, remove level info and place it as properties of levelstate, tiles, levelstate object ipass, locations is still a dict and its keys are dataclass Tiles, remove clear, locations keys are tile dataclass opbjects
    """
    A class representing map states.

    Attributes:
        locations (dict): Current location of elements in a level.
        level_info (dict): Game state information.
    """
    def __init__(self, size: tuple[int, int], grid: list[str]) -> None:
        """
        Initialize a MapData object.

        Parameters:
            size (tuple): Size of map level.
            grid (list): Raw map level data.
        """
        self.locations: dict[str, set[tuple[int, int]]] = {
        ".": set(),
        "T": set(),
        "R": set(),
        "_": set(),
        "~": set(),
        "x": set(),
        "*": set(),
        "+": set(),
        "L": set()
    }
        for i, line in enumerate(grid):
            for j, c in enumerate(line.strip()):
                self.locations[c].add((i, j))

        self.level_info: LevelInfo = {
        "size": size,
        "mushroom_collected": 0,
        "mushroom_total": len(self.locations['+']),
        "game_end": False,
        "inventory": "",
        "invalid_input": False,
        "level_reset": False
        }

        super().__init__()
    
    def get_locations(self) -> dict[str, set[tuple[int, int]]]:
        """
        Retrieve the locations dict of the MapData.

        Returns:
            dict: Current map element locations.
        """
        return self.locations
    
    def get_level_info(self) -> LevelInfo:
        """
        Retrieve the level_info dict of the MapData.

        Returns:
            dict: Current game state information.
        """
        return self.level_info
    
    def update_data(self, new_locations: dict[str, set[tuple[int, int]]], new_level_info: LevelInfo) -> MapData:
        """
        Update the MapData Object with new information.

        Parameters:
            new_locations (dict): Current location of elements in a level.
            new_level_info (dict): Game state information.

        Returns:
            MapData: Updated MapData object.
        """
        self.locations = new_locations
        self.level_info = new_level_info
        new_map = MapData.__new__(MapData)
        new_map.locations = {k: set(v) for k, v in self.locations.items()}
        new_map.level_info = cast(LevelInfo,{k: v for k, v in self.level_info.items()})
        return new_map
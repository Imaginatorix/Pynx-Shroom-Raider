"""
Core game state and tile abstractions.

This package defines fundamental classes used throughout the game, including
tile representations, tile behavior logic, and the overall level state.

Classes
-------
TileBehaviour
    Enumeration of different behaviors associated with a tile.
Tile
    Immutable representation of different tiles found in the game.
LevelState
    Encapsulates the current state of a level.
"""

from .tile_behaviour import TileBehaviour
from .tile import Tile
from .level_state import LevelState

# ===== CUSTOM CLASSES USED THROUGHOUT THE GAME =====

__all__ = ["TileBehaviour", "Tile", "LevelState"]

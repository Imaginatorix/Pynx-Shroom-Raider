from __future__ import annotations
from enum import Enum, auto


# === TILE BEHAVIOUR ===
class TileBehaviour(Enum):
    """
    Enumeration of different behaviors associated with a tile.

    Attributes
    ----------
    DANGER : auto()
        Tile is dangerous or deadly.
    GOAL : auto()
        Tile is a goal tile that contributes to game end.
    ITEM : auto()
        Tile represents an item that can be picked up.
    NONE : auto()
        Tile with no special behavior. Placeholder for NoneType.
    OBSTACLE : auto()
        Tile blocks movement.
    PLAYER : auto()
        Tile represents the player or moveable entity.
    PUSHABLE : auto()
        Tile that can be pushed or moved by the player.
    WALKABLE : auto()
        Tile can be walked on.
    """
    DANGER = auto()
    GOAL = auto()
    ITEM = auto()
    NONE = auto()
    OBSTACLE = auto()
    PLAYER = auto()
    PUSHABLE = auto()
    WALKABLE = auto()

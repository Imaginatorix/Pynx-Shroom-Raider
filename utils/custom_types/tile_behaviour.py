from __future__ import annotations

from enum import Enum, auto

# === TILE BEHAVIOUR ===
class TileBehaviour(Enum):
    """TODO: Enum to identify the behaviour of the tile"""
    DANGER = auto()
    GOAL = auto()
    ITEM = auto()
    NONE = auto()
    OBSTACLE = auto()
    PLAYER = auto()
    PUSHABLE = auto()
    WALKABLE = auto()

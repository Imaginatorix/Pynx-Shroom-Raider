"""Immutable representation of different tiles found in the game."""

from __future__ import annotations

from dataclasses import dataclass
from .tile_behaviour import TileBehaviour

# === TILE REPRESENTATION ===
@dataclass(frozen=True)
class Tile():
    """
    Immutable representation of different tiles found in the game.

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

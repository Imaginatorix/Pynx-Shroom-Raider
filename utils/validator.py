"""
Runtime validation utilities for game state and configuration.

It includes:
- Atomic validators for checking types and ranges
- Domain-specific validators for ensuring assumptions are followed and the internal variables
of `LevelState` objects are consistent
"""

from numbers import Number
from typing import Any, TypeAlias, Union
from typing import get_args, get_origin

from utils.custom_types import LevelState, Tile, TileBehaviour

# === VALIDATOR TOOLS TO TEST WHETHER FUNCTION PARAMETERS CONFORM TO THE EXPECTED VALUES ===

# === ATOMIC VALIDATORS (REUSABLE) ===

TypeHint: TypeAlias = Any

def format_hint(hint: TypeHint) -> str:
    """
    Format a runtime type hint into a readable string.

    Parameters
    ----------
    hint : TypeHint
        A runtime type hint.

    Returns
    -------
    str
        A formatted string representation of the type hint.
    """
    origin = get_origin(hint)
    args = get_args(hint)

    if origin is None:
        return hint.__name__

    return f"{origin.__name__}[{', '.join(format_hint(a) for a in args)}]"


# == VALIDATE TYPE ==
def validate_type(value: Any, hint: TypeHint, variable_name: str = "value") -> None:
    """
    Validate that `value` conforms to the runtime-interpreted type hint `hint`.

    Parameters
    ----------
    value : Any
        The runtime value to validate.
    hint : TypeHint
        A runtime-interpreted type hint describing the expected structure
        of `value`.
    variable_name : str, default="value"
        Name of the variable being validated. This is used only for generating
        informative error messages.

    Returns
    -------
    None
        This function does not return a value.

    Raises:
        TypeError: if value does not match hint.
    """
    def _validate_type(value: Any, hint: TypeHint) -> bool:
        origin = get_origin(hint)
        args = get_args(hint)

        # Union [T1 | T2 | ... | Tn]
        if origin is Union:
            return any(_validate_type(value, a) for a in args)

        # tuple[T1, T2, ..., Tn]
        if origin is tuple:
            if not isinstance(value, tuple) or len(value) != len(args):
                return False
            return all(_validate_type(v, a) for v, a in zip(value, args))

        # list[T], set[T]
        if origin in (list, set):
            if not isinstance(value, origin):
                return False
            (elem_type,) = args
            return all(_validate_type(v, elem_type) for v in value)

        # dict[K, V]
        if origin is dict:
            if not isinstance(value, dict):
                return False
            k_type, v_type = args
            return all(
                _validate_type(k, k_type) and _validate_type(v, v_type)
                for k, v in value.items()
            )

        # Base Case
        if not isinstance(value, hint):
            return False
        return True


    if not _validate_type(value, hint):
        raise TypeError(f"{variable_name} must be {format_hint(hint)}")


# == VALIDATE RANGE (INCLUSIVE) ==
def validate_range(value: Number, minimum: Number = float("-inf"), maximum: Number = float("inf"), variable_name="value"):
    """
    Validate that a numeric value lies within an inclusive range.

    Parameters
    ----------
    value : numbers.Number
        The numeric value to validate.
    minimum : numbers.Number, default=float("-inf")
        The inclusive lower bound. Defaults to negative infinity.
    maximum : numbers.Number, default=float("inf")
        The inclusive upper bound. Defaults to positive infinity.
    variable_name : str, default="value"
        Name of the variable being validated, used for error messages.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    ValueError
        If `value` lies outside the inclusive range
        `[minimum, maximum]`.
    """
    if not (minimum <= value <= maximum):
        raise ValueError(f"{variable_name} must be in between {minimum} and {maximum} (inclusive).")


# === END OF ATOMIC VALIDATORS (REUSABLE) ===

# === DOMAIN VALIDATORS ===

def validate_state_internals(state: LevelState) -> None:
    """
    Validate the internal consistency of the current state.

    This function performs both structural and semantic validation of a
    `LevelState` object. It checks individual fields for correct types and
    valid ranges, and enforces cross-field invariants.

    The function raises an exception immediately upon detecting any
    inconsistency.

    Parameters
    ----------
    state : LevelState
        The level state object whose internal fields are to be validated.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `state` or any of its fields has an invalid type.
    ValueError
        If the internal values of `state` violate game invariants or logical
        constraints.
    """
    # Check type
    if not isinstance(state, LevelState):
        raise TypeError("state must be LevelState")

    size = state.size
    mushroom_collected = state.mushroom_collected
    mushroom_total = state.mushroom_total
    game_end = state.game_end
    covering = state.covering
    inventory = state.inventory
    invalid_input = state.invalid_input
    level_reset = state.level_reset
    locations = state.locations

    # Check each internal
    validate_size(size)
    validate_mushroom_collected(mushroom_collected)
    validate_mushroom_total(mushroom_total)
    validate_game_end(game_end)
    validate_covering(covering)
    validate_inventory(inventory)
    validate_invalid_input(invalid_input)
    validate_level_reset(level_reset)
    validate_locations(size, locations)

    # Cross-field checks
    r, c = size
    # Mushroom Counts
    if mushroom_collected > mushroom_total:
        raise ValueError("mushroom_collected must not exceed mushroom_total")
    if mushroom_total > r*c-1:
        raise ValueError("mushroom_total must not exceed the available space in the map")

    MUSHROOM_TILE = [tile for tile in locations if tile.behaviour is TileBehaviour.GOAL][0] # As of now, only one goal is supported
    if mushroom_total-mushroom_collected != len(locations[MUSHROOM_TILE]):
        raise ValueError("There is not enough mushroom to end the game.")

    # Game End
    if mushroom_collected == mushroom_total and not game_end:
        raise ValueError("When mushroom_collected = mushroom_total, game_end must be true.")


# == VALIDATE SIZE ==
def validate_size(size: tuple[int, int]) -> None:
    """
    Validate the dimensions of a level grid.

    Parameters
    ----------
    size : tuple[int, int]
        A `(rows, columns)` pair describing the grid dimensions.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `size` is not a tuple of two integers.
    ValueError
        If the grid dimensions or total area are invalid.
    """
    # Check type
    validate_type(size, tuple[int, int], "size")

    r, c = size
    # Check if it's valid values
    validate_range(r, minimum=1, maximum=30, variable_name="r")
    validate_range(c, minimum=1, maximum=30, variable_name="c")
    validate_range(r*c, minimum=2, variable_name="map area (r*c)")


# == VALIDATE MUSHROOM COLLECTED ==
def validate_mushroom_collected(mushroom_collected: int) -> None:
    """
    Validate the number of mushrooms collected.

    Parameters
    ----------
    mushroom_collected : int
        The number of mushrooms collected so far.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `mushroom_collected` is not an integer.
    ValueError
        If `mushroom_collected` is negative.
    """
    # Check type
    validate_type(mushroom_collected, int, "mushroom_collected")
    # Check if it's valid values
    validate_range(mushroom_collected, minimum=0, variable_name="mushroom_collected")


# == VALIDATE MUSHROOM TOTAL ==
def validate_mushroom_total(mushroom_total: int) -> None:
    """
    Validate the total number of mushrooms in the level.

    Parameters
    ----------
    mushroom_total : int
        The total number of mushrooms available in the level.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `mushroom_total` is not an integer.
    ValueError
        If `mushroom_total` is less than one.
    """
    # Check type
    validate_type(mushroom_total, int, "mushroom_total")
    # Check if it's valid values
    validate_range(mushroom_total, minimum=1, variable_name="mushroom_total")


# == VALIDATE GAME END ==
def validate_game_end(game_end: bool) -> None:
    """
    Validate the game_end flag.

    Parameters
    ----------
    game_end : bool
        Whether the game has ended.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `game_end` is not a boolean.
    """
    # Check type
    validate_type(game_end, bool, "game_end")


# == VALIDATE COVERING ==
def validate_covering(covering: Tile) -> None:
    """
    Validate the tile currently covering the player.

    Parameters
    ----------
    covering : Tile
        The tile representing what lies beneath the player.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `covering` is not a `Tile` instance.
    """
    # Check type
    validate_type(covering, Tile, "covering")


# == VALIDATE INVENTORY ==
def validate_inventory(inventory: Tile) -> None:
    """
    Validate the player's inventory tile.

    Parameters
    ----------
    inventory : Tile
        The tile currently held in the player's inventory.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `inventory` is not a `Tile` instance.
    """
    # Check type
    validate_type(inventory, Tile, "inventory")


# == VALIDATE INVALID INPUT ==
def validate_invalid_input(invalid_input: bool) -> None:
    """
    Validate the invalid_input flag.

    Parameters
    ----------
    invalid_input : bool
        Whether the last player input was invalid.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `invalid_input` is not a boolean.
    """
    # Check type
    validate_type(invalid_input, bool, "invalid_input")


# == VALIDATE LEVEL RESET ==
def validate_level_reset(level_reset: bool) -> None:
    """
    Validate the level_reset flag.

    Parameters
    ----------
    level_reset : bool
        Whether the level has been reset.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If `level_reset` is not a boolean.
    """
    # Check type
    validate_type(level_reset, bool, "level_reset")


# == VALIDATE LOCATIONS ==
def validate_locations(size: tuple[int, int], locations: dict[Tile, set[tuple[int, int]]]) -> None:
    """
    Validate tile locations within the level grid.

    Ensures that all grid coordinates are covered and that all coordinates
    lie within bounds.

    Parameters
    ----------
    size : tuple of int
        The `(rows, columns)` dimensions of the grid.
    locations : dict[Tile, tuple[int, int]]
        Mapping from tile types to the set of grid coordinates they occupy.

    Returns
    -------
    None
        This function does not return a value.

    Raises
    ------
    TypeError
        If the input types are invalid.
    ValueError
        If the coordinates do not correctly fill the grid.
    """
    # Check type
    validate_size(size)
    validate_type(locations, dict[Tile, set[tuple[int, int]]], "locations")

    # Locations must have only one Lara
    CHARACTER_TILES = [tile for tile in locations]
    CHARACTER_TILE = CHARACTER_TILES[0]
    if len(CHARACTER_TILES) != 1 and len(locations[CHARACTER_TILE]):
        raise ValueError("Game must have only one player.")
    
    # All cells must be visited only once (except player location)
    r, c = size
    # Populate grid
    grid = set((i, j) for i in range(r) for j in range(c))
    visited = set()
    for coordinates in locations.values():
        for i, j in coordinates:
            if not (0 <= i < r and 0 <= j < c):
                raise ValueError("Coordinates must completely fill the grid range")

            if (i, j) not in visited:
                visited.add((i, j))

    if grid != visited:
        raise ValueError("Coordinates must completely fill the grid range")

    # Assume solvable as per [highlighted cause I don't wanna link solver as it is still a bit slow]


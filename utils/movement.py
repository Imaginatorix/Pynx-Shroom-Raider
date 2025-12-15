"""Convert user input into interactions and movement within the game."""

from utils.custom_types import LevelState, TileBehaviour
from utils.settings import (TREE_TILE,
                            MUSHROOM_TILE,
                            ROCK_TILE,
                            WATER_TILE,
                            NONE_TILE,
                            AXE_ITEM,
                            FLAMETHROWER_ITEM)


POSSIBLE_INPUTS: dict[str, tuple[int, int]] = {"W": (-1, 0),
                                               "A": (0, -1),
                                               "S": (1, 0),
                                               "D": (0, 1),
                                               "!": (0, 0),
                                               "P": (0, 0)}


# === USE USER INPUT TO UPDATE MAP DATA ===
def user_input(curr_level: LevelState,
               orig_level: LevelState,
               move_count: int,
               sys_input: str = "") -> tuple[list[LevelState], int]:
    """
    Retrieves user input using the input function or from the moves passed when
    the main file is ran. Uses the input to update map information.

    Parameters
    ----------
    curr_level: LevelState
        Current level information.
    orig_level: LevelState
        Original level information.
    move_count: int
        Number of moves the user has inputted.
    sys_input: str, optional
        Moves passed when the main file is ran. Defaults to ""

    Returns
    -------
    List[LevelState]
        List of updated LevelState objects.
    """

    # Asks user to input if no moves are given to the function
    if not sys_input:
        sys_input = input("What will you do? ")

    commands: tuple[str, ...] = tuple(ch for ch in sys_input.upper())

    actions: list[LevelState] = []

    # When commands are empty, mark as invalid input
    if not commands:
        curr_level.invalid_input = True
        actions.append(curr_level.get_state())
        return actions, move_count

    # Iterate through each character of commands
    for action in commands:

        # When action is invalid, stop the iteration
        if action not in POSSIBLE_INPUTS:
            curr_level.invalid_input = True
            actions.append(curr_level.get_state())
            break

        # Revert to original state of the level
        elif action == "!":
            curr_level.reset_state(orig_level)
            move_count = -1

        # Try to pick up an item
        elif action == "P" and curr_level.is_valid_item_tile():
            curr_level.pick_item()

        # User input is a movement command
        elif curr_level.is_valid_movement(POSSIBLE_INPUTS[action]):

            player_move = POSSIBLE_INPUTS[action]
            player_inv = curr_level.inventory

            # Retrieve new player location and tile object after moving
            # TODO: add the dot tile after next tile
            _player_loc, _tile = curr_level.next_player_location(player_move)

            if _tile == TREE_TILE and player_inv == AXE_ITEM:
                # Remove a tree and clear inventory
                curr_level.use_axe(_player_loc)

            elif _tile == TREE_TILE and player_inv == FLAMETHROWER_ITEM:
                # Spread a fire and clear inventory
                curr_level.use_fire(_player_loc)

            elif (_tile == ROCK_TILE or
                  _player_loc in curr_level.locations[ROCK_TILE]):
                # Try to push the rock
                try:
                    curr_level.push_rock(_player_loc, player_move)
                except ValueError:
                    continue

            elif _tile == WATER_TILE:
                # End the game -> lose
                curr_level.game_lose(_player_loc)
                curr_level.set_player_location(_player_loc)
                break

            elif _tile == MUSHROOM_TILE:
                # Collect the mushroom
                curr_level.collect_mushroom(_player_loc)

            if curr_level.check_win():
                # End the game -> win
                curr_level.game_end = True
                curr_level.set_player_location(_player_loc)
                break

            # Update Laro's location
            curr_level.set_player_location(_player_loc)

            if _tile.behaviour == TileBehaviour.ITEM:
                curr_level.covering = _tile
            else:
                curr_level.covering = NONE_TILE

        else:
            continue

        move_count += 1
        actions.append(curr_level.get_state())
    if curr_level.game_end:
        move_count += 1
        actions.append(curr_level.get_state())
    return actions, move_count

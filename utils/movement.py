from utils.custom_types import LevelState
import utils.settings as TILES

POSSIBLE_INPUTS: dict[str, tuple[int,int]] = {"W":(-1,0), "A":(0,-1), "S":(1,0), "D":(0,1), "!":(0,0), "P":(0,0)}

# === USE USER INPUT TO UPDATE MAP DATA ===
def user_input(curr_level: LevelState, sys_input: str = "") -> list[LevelState]:
    """ 
    Retrieves user input using the input function or from the moves passed when the main file is ran.
    Uses the input to update map information.

    Parameters
    ----------
    curr_level: LevelState 
        Current level information.
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

    commands: tuple[str,...] = tuple(ch for ch in sys_input.upper())

    actions: list[LevelState] = []

    # When commands are empty, mark as invalid input
    if not commands:
        curr_level.invalid_input = True
        actions.append(curr_level.get_state())
        return actions
    
    # Iterate through each character of commands
    for action in commands:

        # When action is invalid, stop the iteration
        if action not in POSSIBLE_INPUTS:
            curr_level.invalid_input = True
            actions.append(curr_level.get_state())
            break

        # Revert to original state of the level
        elif action == "!":
            curr_level.reset_state()

        # Try to pick up an item
        elif action == "P" and curr_level.is_valid_item_tile():
            curr_level.pick_item()
        
        # User input is a movement command
        elif curr_level.is_valid_movement(POSSIBLE_INPUTS[action]):
            
            # Retrieve the new possible player location and tile object after moving
            # TODO: add the dot tile after next tile
            new_player_location, next_tile = curr_level.next_player_location(POSSIBLE_INPUTS[action])
            
            if next_tile is TILES.TREE_TILE and curr_level.inventory is TILES.AXE_ITEM:
                # Remove a tree and clear inventory
                curr_level.use_axe(new_player_location)

            elif next_tile is TILES.TREE_TILE and curr_level.inventory is TILES.FLAMETHROWER_ITEM:
                # Spread a fire and clear inventory
                curr_level.use_fire(new_player_location)

            elif next_tile is TILES.ROCK_TILE:
                # Try to push the rock
                try:
                    curr_level.push_rock(new_player_location, POSSIBLE_INPUTS[action])
                except ValueError:
                    continue
                

            elif next_tile is TILES.WATER_TILE:
                # End the game -> lose
                curr_level.game_lose(new_player_location)
            
            elif next_tile is TILES.MUSHROOM_TILE:
                # Collect the mushroom
                curr_level.collect_mushroom(new_player_location)
            
            if curr_level.check_win():
                # End the game -> win
                curr_level.game_end()
            
            # Update Laro's location
            curr_level.set_player_location(new_player_location)
        else:
            continue
        
        actions.append(curr_level.get_state())
    return actions
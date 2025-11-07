from copy import deepcopy
from dict_hash import dict_hash
import utils.parser as parser
import utils.movement as movement

# === ALGORITHM TO FIND OPTIMAL SOLUTION, IF IT EXISTS ===
def find_solution(filename: str, limit: int|float = float("inf")) -> str:
    initial_level_info, initial_locations = parser.parse_level(filename)

    frontier = [(initial_level_info, initial_locations, "")]
    visited = set()
    visited.add((dict_hash(initial_level_info), dict_hash(initial_locations)))

    kernel = 'wasd'
    n = 0
    # Breadth-First Search
    while n < len(frontier):
        level_info, locations, moves = frontier[n]

        # Try each possible move
        for move in kernel:
            next_level_info, next_locations = movement.user_input(level_info, locations, move)
            visited.add((dict_hash(next_level_info), dict_hash(next_locations)))

            # If that move ended game and it is a win, return series of moves
            if next_level_info["game_end"] and next_level_info["mushroom_collected"] == next_level_info["mushroom_total"]:
                return moves+move

            # If game state not yet explore and not yet ended and is still within limits, continue game
            elif not (dict_hash(level_info), dict_hash(locations)) in visited and not next_level_info["game_end"] and len(moves)+1 < limit:
                frontier.append((next_level_info, next_locations, moves+move))

        n += 1


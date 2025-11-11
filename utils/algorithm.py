from dict_hash import dict_hash

# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import utils.parser as parser
import utils.movement as movement
import utils.ui as ui

# === ALGORITHM TO FIND OPTIMAL SOLUTION, IF IT EXISTS ===

def solution_search(filename: str, limit: int|float = float("inf")) -> str:
    """
    TODO: An interaction-based game stte BFS to speed up solution seaerch
    """
    def next_actions(level_info: dict, locations: dict[str: set[tuple[int, int]]]):
        ...

    initial_level_info, initial_locations = parser.parse_level(filename)

    frontier = [(initial_level_info, initial_locations, "")]
    visited = set()
    visited.add((dict_hash(initial_level_info), dict_hash(initial_locations)))

    kernel = 'WASDP'
    longest_move = 0
    n = 0
    # Breadth-First Search
    while n < len(frontier):
        level_info, locations, moves = frontier[n]
        if len(moves) > longest_move:
            print(f"Calculating depth {len(moves)}...")
            longest_move = len(moves)

        # Try each possible move
        for move in kernel:
            next_state = movement.user_input(level_info, locations, locations, level_info, move)
            if not next_state:
                continue
            next_locations, next_level_info = next_state[-1]
            next_state_hash = (dict_hash(next_level_info), dict_hash(next_locations))
            # ui.show_screen(next_level_info, next_locations)

            # If that move ended game and it is a win, return series of moves
            if next_level_info["game_end"] and next_level_info["mushroom_collected"] == next_level_info["mushroom_total"]:
                return moves+move

            # If game state not yet explore and not yet ended and is still within limits, continue game
            elif not next_state_hash in visited and not next_level_info["game_end"] and len(moves)+1 < limit:
                frontier.append((next_level_info, next_locations, moves+move))
                visited.add(next_state_hash)

        n += 1


def shortest_path():
    ...

print(solution_search("levels/spring/stage4.txt"))


# Make higher level directories visible
import sys
from os import path, listdir
from datetime import date
sys.path.append(path.abspath("."))

from dict_hash import dict_hash
from random import randrange, choice, choices, shuffle, random
from datetime import date
from os import makedirs
from collections import deque
import traceback

import utils.parser as parser
import utils.movement as movement

# === ALGORITHM TO FIND OPTIMAL SOLUTION, IF IT EXISTS ===

def solution_search(filename: str, limit: int|float = float("inf")) -> str:
    """
    TODO: An interaction-based game state BFS to speed up solution seaerch
    NOTE: Could be A*
    """
    def next_interactions(level_info: dict, locations: dict[str: set[tuple[int, int]]]):
        # Possible interactions
        # Push a rock
        # Pick up item (if no item yet)
        # Use item (if you have no item)
        # Collect mushroom
        ...

    initial_level_info, initial_locations = parser.parse_level(filename)

    frontier = deque()
    frontier.append((initial_level_info, initial_locations, ""))
    visited = set()
    visited.add((dict_hash(initial_level_info), dict_hash(initial_locations)))

    kernel = 'WASDP'
    longest_move = 0
    # Breadth-First Search
    while frontier:
        level_info, locations, moves = frontier.popleft()
        if len(moves) > longest_move:
            #print(f"Calculating depth {len(moves)}...")
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
            elif next_state_hash not in visited and not next_level_info["game_end"] and len(moves)+1 < limit:
                frontier.append((next_level_info, next_locations, moves+move))
                visited.add(next_state_hash)


def neighbors(i, j, r, c):
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = i+di, j+dj
        if 0 <= ni < r and 0 <= nj < c:
            yield ni, nj


def diagonal(i, j, r, c):
    for di, dj in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        ni, nj = i+di, j+dj
        if 0 <= ni < r and 0 <= nj < c:
            yield ni, nj


def partition_map(r: int, c: int, num_seeds: int):
    grid = [[None]*c for _ in range(r)]

    # Empty spaces
    empty_spaces = set()
    seed_placements = set()
    for i in range(r):
        for j in range(c):
            if i%2 == 0 and j%2 == 0:
                seed_placements.add((i, j))
            empty_spaces.add((i, j))

    # Create seeds (at least 2 zones)
    seeds = [None]*num_seeds
    zone_ids = list(range(1, num_seeds+1))

    # Assign zone ids
    NONE = 0
    grid = [[NONE]*c for _ in range(r)]

    # Ensure at least zone_count seeds and that they must be at least distance 3 from each other
    borders = {zone_id: set() for zone_id in zone_ids}
    for i_seed in range(num_seeds):
        si, sj = choice(list(seed_placements))
        zone_id = zone_ids[i_seed]
        seeds[i_seed] = (si, sj)
        # Save neighbors
        for ni, nj in neighbors(si, sj, r, c):
            grid[ni][nj] = zone_id
            borders[zone_id].add((ni, nj))
            if (ni, nj) in empty_spaces:
                empty_spaces.remove((ni, nj))

        seed_placements.remove((si, sj))
        empty_spaces.remove((si, sj))


    while sum((len(edges) for edges in borders.values())) > 0:
        # Pick random zone that is not empty
        non_empty_zones = [zone_id for zone_id in borders if len(borders[zone_id]) > 0]
        zone_id = choice(non_empty_zones)
        i, j = borders[zone_id].pop()

        # Pick random neighbor to swallow (until it has swallowed something)
        possible_swallow = [(ni, nj) for ni, nj in neighbors(i, j, r, c) if grid[ni][nj] in {NONE, zone_id}]
        shuffle(possible_swallow)
        for si, sj in possible_swallow:
            # If it has anything that is neither same zone nor is empty, don't swallow it
            if any((grid[ni][nj] not in {NONE, zone_id} for ni, nj in neighbors(si, sj, r, c))):
                continue
            # And if the thing to be swallowed has a diagonal that is neither same zone nor is empty, don't swallow it
            stopped = False
            for ni, nj in neighbors(si, sj, r, c):
                for nni, nnj in neighbors(ni, nj, r, c):
                    if grid[nni][nnj] not in {NONE, zone_id}:
                        stopped = True
                        break
                if stopped:
                    break
            if stopped:
                continue
            # And if all of them are already zone_id
            if all((grid[ni][nj] == zone_id for ni, nj in neighbors(si, sj, r, c))):
                continue

            # Swallow it
            for ai, aj in set(neighbors(si, sj, r, c)):
                if grid[ai][aj] == zone_id:
                    continue
                borders[zone_id].add((ai, aj))
                grid[ai][aj] = zone_id
            grid[si][sj] = zone_id
            
            # time.sleep(1)
            # pprint2(grid, has_swallowed)
            # print()
            break

    # Clean-up and populate final boundary
    boundary = {zone_id: set() for zone_id in zone_ids}
    territory = {zone_id: set() for zone_id in zone_ids}
    adjacency_graph = {zone_id: set() for zone_id in zone_ids}
    for i in range(r):
        for j in range(c):
            if grid[i][j] == NONE:
                # If surrounded by 1 one type of zone, it belongs in same zone
                if len(set((grid[ni][nj] for ni, nj in neighbors(i, j, r, c)))) == 1:
                    ni, nj = next(neighbors(i, j, r, c))
                    grid[i][j] = grid[ni][nj]

                adjacent = set()
                for ni, nj in neighbors(i, j, r, c):
                    if grid[ni][nj] != NONE:
                        adjacent.add(grid[ni][nj])
                        boundary[grid[ni][nj]].add((i, j))

                for a in adjacent:
                    for b in adjacent - {a}:
                        adjacency_graph[a].add(b)
            else:
                territory[grid[i][j]].add((i, j))
    
    return grid, set(zone_ids), adjacency_graph, territory, boundary


def random_solution_tree(zone_ids, adjacency_graph, nonadjacency_probability=0.01, branching_factor=0.25):
    def edge(a, b):
        return tuple(sorted([a, b]))

    spanning_tree = {zone_id: set() for zone_id in zone_ids}
    edges = set()
    nonadjacent_edges = set()

    # Set root
    current = choice(list(zone_ids))

    visited = set()
    # Random walk
    while zone_ids - visited:
        nonadjacent_flag = False
        # Either walk to an adjacent node or non-adjacent node
        if random() < nonadjacency_probability:
            sampling_list = list(zone_ids - adjacency_graph[current] - {current} - visited)
            nonadjacent_flag = True
        else:
            sampling_list = list(adjacency_graph[current] - {current} - visited)

        if not sampling_list:
            # Jump randomly
            if visited:
                current = choice(list(visited))
            continue

        next_zone = choice(sampling_list)

        # Record
        spanning_tree[current].add(next_zone)
        spanning_tree[next_zone].add(current)
        edges.add(edge(current, next_zone))
        if nonadjacent_flag:
            nonadjacent_edges.add(edge(current, next_zone))

        # Remove connected to root
        visited |= {current, next_zone}

        # Prepare next loop
        if random() >= branching_factor:
            current = next_zone

    return spanning_tree, edges, nonadjacent_edges


def assign_zone_roles(zone_ids, solution_tree, edges, nonadjacent_edges, mushroom_factor=0.05):
    # Assign edges
    edge_assignments = {e: None for e in edges}

    # Enumerate all connected edges (unmentioned are automatically uncrossable = water)
    for e in edges:
        if e in nonadjacent_edges:
            edge_assignments[e] = "Fire Boundary"
        else:
            # Randomly assign
            edge_types = ("Tree Boundary", "Water Boundary")
            edge_assignments[e] = choice(edge_types)

    # Assign zones
    # L = Lara starting position
    # + = Mushroom
    # else, is temporary zone indicator
    # And, if it is a key zone, it also contains one of the following: x, R, *
    zone_assignments = {zone_id: "" for zone_id in zone_ids}
    visited = set()

    # Pick random root as position of Lara
    root = choice(list(zone_ids))
    zone_assignments[root] = "L"

    # For key zone assignment
    prev_zone = {zone_id: set() for zone_id in zone_ids}

    # Traverse solution tree
    frontier = [(root, set())] # (v, traversed)
    while frontier:
        current, traversed = frontier.pop()
        # Leaf is guaranteed to be mushroom
        if len(solution_tree[current] - visited) == 0:
            zone_assignments[current] = "+"
        # Else, randomly assign as either mushroom or temporary zone
        else:
            if random() < mushroom_factor:
                zone_assignments[current] = "+"
        
        visited.add(current)
        prev_zone[current] |= traversed
        for v in solution_tree[current] - visited:
            frontier.append((v, traversed | {current}))

    def came_first(a, b):
        if a in prev_zone[b]:
            return a
        else:
            return b

    # For each zone, include what keys can be found based on boundary
    for e, e_type in edge_assignments.items():
        # Put the key in a zone previous of the first part of the boundary
        first = came_first(*e)
        key_zone = choice(list(prev_zone[first] | {first}))

        if e_type == "Tree Boundary":
            zone_assignments[key_zone] += "x"
        elif e_type == "Water Boundary":
            zone_assignments[key_zone] += "R"*randrange(1, 4)
        # elif e_type == "Fire Boundary":
        #     zone_assignments[key_zone] += "*"
    
    return zone_assignments, edge_assignments


def draw_assignments(r, c, zone_assignments, edge_assignments, territory, boundary):
    grid = [["."]*c for _ in range(r)]

    # Draw boundaries first
    for e, e_type in edge_assignments.items():
        # Fire Boundary
        # Water and Tree Boundary
        if e_type in {"Water Boundary", "Tree Boundary"}:
            a, b = e
            ab_boundaries = boundary[a] & boundary[b]

            for i, j in ab_boundaries:
                grid[i][j] = "~" if e_type == "Water Boundary" else "T"
        else:
            a, b = e
            ab_boundaries = boundary[a] & boundary[b]

            for i, j in ab_boundaries:
                grid[i][j] = "~"

    # Draw zones
    for zone_id, elements in zone_assignments.items():
        zone_territory = set(territory[zone_id])
        for element in elements:
            if zone_territory:
                i, j = choice(list(zone_territory))
                zone_territory -= {(i, j)}
                grid[i][j] = element

    # from pprint import pprint
    # pprint(grid)
    return grid


def generate_raw_maps(r: int, c: int, limit: int, raw_maps_directory: str, output_directory: str) -> None:
    def add_border(r, c, grid, border):
        # Set border
        new_grid = [[None]*c for _ in range(r)]
        # border = choice(OBSTACLES)
        for i in range(r):
            for j in range(c):
                if not (i == 0 or i == r-1):
                    if j == 0 or j == c-1:
                        new_grid[i][j] = border
                        # row += border
                    else:
                        new_grid[i][j] = f"{grid[i-1][j-1]}"
                        # row = f"{grid[i-1][j-1]}"
                else:
                    new_grid[i][j] = border
                    # row += border
            # print(row)
        return new_grid

    def write_map(filename, r, c, grid):
        grid_lines = [''.join(row) for row in grid]
        with open(filename, 'w') as f:
            print(f"{r} {c}", file=f)
        with open(filename, 'a') as f:
            for grid_line in grid_lines:
                print(grid_line, file=f)

    # Counter for invalid states
    INVALID_COUNTER = 50
    OBSTACLES = ('~', 'T', 'R')

    generated = 0
    while generated < limit:
        attempts = 0
        produced = False
        while attempts < INVALID_COUNTER:
            try:
                # Set distinct zones
                subgrid, zone_ids, adjacency_graph, territory, boundary = partition_map(r-2, c-2, randrange(2, max(3, ((r-2)*(c-2))//3)))
                # Set a randomized solution
                solution_tree, edges, nonadjacent_edges = random_solution_tree(zone_ids, adjacency_graph)
                # Assign zone roles
                zone_assignments, edge_assignments = assign_zone_roles(zone_ids, solution_tree, edges, nonadjacent_edges)
                # Draw to grid
                new_subgrid = draw_assignments(r-2, c-2, zone_assignments, edge_assignments, territory, boundary)

                # Add border
                # print_grid(new_subgrid, choices(OBSTACLES, weights=[0.45, 0.10, 0.45])[0])
                proposed_grid = add_border(r, c, new_subgrid, choices(OBSTACLES, weights=[0.45, 0.10, 0.45])[0])
                # Write file
                today = date.today()
                # Raw directory
                directory_name = path.join(raw_maps_directory, str(today))
                makedirs(directory_name, exist_ok=True)
                filename = path.join(directory_name, f"{generated}.txt")
                write_map(filename, r, c, proposed_grid)
                #print("Generated a raw map...")

                # Check if it is solvable
                if solution_search(filename) is None:
                    raise Exception("Unsolvable maze")
                
                # Write it in the output_directory
                directory_name = path.join(output_directory, str(today))
                makedirs(directory_name, exist_ok=True)
                filename = path.join(directory_name, f"{generated}.txt")
                write_map(filename, r, c, proposed_grid)
                #print("Generated a valid map...")

                # Include in final generated
                produced = True
                break
            except Exception as e:
                #print(traceback.print_exception(*sys.exc_info()))
                attempts += 1

        if not produced:
            raise SystemError("An error has occured in the generation process...")
        generated += 1

    return generated


def generate_map(r: None|int = None, c: None|int = None, limit: int = 100, output_directory: None|str = None) -> None:
    # Generate random if not provided
    if r is None:
        r = randrange(5, 7)
    if c is None:
        c = randrange(5, 7)
    
    if r < 3:
        raise ValueError("Grid must have a value of at least 3x3")
    if c < 3:
        raise ValueError("Grid must have a value of at least 3x3")

    print(f"Generating {r}x{c} map...")

    # Important directories
    raw_maps_directory = f"generated_maps/raw2/{r}_{c}"
    output_directory = f"generated_maps/final2/{r}_{c}"
    # Generate raw maps
    num_generated = generate_raw_maps(r, c, limit, raw_maps_directory, output_directory)
    # Filter maps according to 'Good Game' Heurstic

    print()
    all_items = listdir(path.join(output_directory, str(date.today())))
    random_file_name = choice(all_items)
    random_file_path = path.join(path.join(output_directory, str(date.today())), random_file_name)
    

    #print(f"Generated {num_generated} map(s) at {output_directory}")

    return random_file_path


if __name__ == "__main__":
    # print(solution_search("levels/spring/stage4.txt"))
    for r in range(5, 10):
        for c in range(5, 10):
            generate_map(r, c, 10)

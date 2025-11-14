from collections import deque
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

from pprint import pprint
import time

def pprint2(arr, red):
    for i in range(len(arr)):
        row = ""
        for j in range(len(arr[0])):
            if (i, j) in red:
                row += f"{bcolors.FAIL}{arr[i][j]}{bcolors.ENDC}"
            else:
                row += f"{arr[i][j]}"
        print(row)

r, c = 10, 10
grid = [[None]*c for _ in range(r)]

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

# Create seeds (one must be player's zone)
NUM_SEEDS = 3
seeds = [None]*NUM_SEEDS
zone_ids = list(range(1, NUM_SEEDS+1))

# Assign zone ids
NONE = 0
grid = [[NONE]*c for _ in range(r)]

# Ensure at least zone_count seeds and that they must be at least distance 3 from each other
borders = {zone_id: set() for zone_id in zone_ids}
for i_seed in range(NUM_SEEDS):
    si, sj = (random.randrange(0, r, 2), random.randrange(0, c, 2))
    zone_id = zone_ids[i_seed]
    seeds[i_seed] = (si, sj)
    # Save neighbors
    for ni, nj in neighbors(si, sj, r, c):
        grid[ni][nj] = zone_id
        borders[zone_id].add((ni, nj))


while sum((len(edges) for edges in borders.values())) > 0:
    # Pick random zone that is not empty
    non_empty_zones = [zone_id for zone_id in borders if len(borders[zone_id]) > 0]
    zone_id = random.choice(non_empty_zones)
    i, j = borders[zone_id].pop()

    # Pick random neighbor to swallow (until it has swallowed something)
    possible_swallow = [(ni, nj) for ni, nj in neighbors(i, j, r, c) if grid[ni][nj] in {NONE, zone_id}]
    random.shuffle(possible_swallow)
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

        has_swallowed = set(neighbors(si, sj, r, c)) | {(si, sj)}

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
for i in range(r):
    for j in range(c):
        if grid[i][j] == NONE:
            # If surrounded by 1 one type of zone, it belongs in same zone
            if len(set((grid[ni][nj] for ni, nj in neighbors(i, j, r, c)))) == 1:
                ni, nj = next(neighbors(i, j, r, c))
                grid[i][j] = grid[ni][nj]

            for ni, nj in neighbors(i, j, r, c):
                if grid[ni][nj] != NONE:
                    borders[grid[ni][nj]].add((i, j))
        else:
            territory[grid[i][j]].add((i, j))

pprint(grid)

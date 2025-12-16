import random
import sys

# Set random seed
random.seed(11.11) # Tribute to CS11 Gods
RANDOM_TEST_CASES = 50

# === Valid/Normal Cases (Regular input values within acceptable limits) ===
VALID = [
    (10, 10),
    (1, 2),
    (2, 1),
]
for _ in range(RANDOM_TEST_CASES):
    # Randomized valid sizes
    VALID.append((random.randrange(1, 31), random.randrange(1, 31)))


# === Boundary Cases (Values at the boundaries of the acceptable limits) ===
## Blank Case
BLANK = [
    (0, 0),
]
## Other Edge Cases
EDGE = [
    (1, 1),
    (30, 30),
]
EDGE_EXPECTED = [
    "ValueError",
    None,
]

# === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
## Huge Cases
HUGE = [
    (30, 30)
]

# === Invalid/Error Cases (Values that fall outside the valid range) ===
## Type Errors
TYPE_ERRORS = [
    (20, 20, 10),
    [20, 20],
    {20, 20},
    frozenset([20, 20]),
    ("10", 10),
    [2, 3],
    (2, -1, 3),
    (),
    2,
    (2,),
    set((3,)),
    frozenset((3,)),
    {},
    "sdf",
]
## Value Errors
VALUE_ERRORS = [
    (2, -1),
    (-1, 1),
    (-1, -1),
    (1, 31),
    (31, 1),
    (31, 31),
]
for _ in range(RANDOM_TEST_CASES):
    # Randomized negative cases
    VALUE_ERRORS.append((random.randrange(-sys.maxsize-1, 0), random.randrange(1, sys.maxsize)))
    VALUE_ERRORS.append((random.randrange(1, sys.maxsize), random.randrange(-sys.maxsize-1, 0)))
    VALUE_ERRORS.append((random.randrange(-sys.maxsize-1, 0), random.randrange(-sys.maxsize-1, 0)))
    # Randomized excess cases
    VALUE_ERRORS.append((random.randrange(31, sys.maxsize), random.randrange(1, sys.maxsize)))
    VALUE_ERRORS.append((random.randrange(1, sys.maxsize), random.randrange(31, sys.maxsize)))
    VALUE_ERRORS.append((random.randrange(31, sys.maxsize), random.randrange(31, sys.maxsize)))

# ===== FORMAT USED FOR UNIT TESTING =====

# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest
import random

# Import things to test
from utils.ui import create_instructions

RANDOM_TEST_CASES = 250

# === TESTING CREATE_INSTRUCTIONS FUNCTION FROM UTILS/UI.PY ===

def test_create_instructions_valid_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Valid/Normal Cases (Regular input values within acceptable limits) ===
    # No items
    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 2,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "",
            "invalid_input": False
        },
        character_cell = ""
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"2 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "No items here",
        "Not holding anything",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "x",
            "invalid_input": False
        },
        character_cell = ""
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"3 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "No items here",
        "Currently holding 🪓",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 4,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = ""
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"4 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "No items here",
        "Currently holding 🔥",
        "",
    )

    # Can pick up
    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 2,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "",
            "invalid_input": False
        },
        character_cell = "x"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"2 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "[P] Pick up 🪓",
        "Not holding anything",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "",
            "invalid_input": False
        },
        character_cell = "*"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"3 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "[P] Pick up 🔥",
        "Not holding anything",
        "",
    )

    # Cannot pick up
    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 2,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "x",
            "invalid_input": False
        },
        character_cell = "x"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"2 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🪓",
        "Currently holding 🪓",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "x",
            "invalid_input": False
        },
        character_cell = "*"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"3 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🔥",
        "Currently holding 🪓",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 2,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = "x"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"2 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🪓",
        "Currently holding 🔥",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = "*"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"3 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🔥",
        "Currently holding 🔥",
        "",
    )

    # Randomized valid cases
    # No item
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(sys.maxsize+1)
        mushroom_collected = random.randrange(mushroom_total)
        inventory = random.choice(('x', '*'))
        sample_level_info = {
            "size": (r, c),
            "mushroom_collected": mushroom_collected,
            "mushroom_total": mushroom_total,
            "game_end": False,
            "inventory": inventory,
            "invalid_input": False
        }

        assert create_instructions(
            level_info = sample_level_info,
            character_cell = ""
        ) == (
            "=====================",
            f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
            "=====================",
            "",
            f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
            "",
            f"{mushroom_collected} out of {mushroom_total} mushroom(s) collected"
            "",
            f"[W] Move up",
            f"[A] Move left",
            f"[S] Move down",
            f"[D] Move right",
            f"[!] Reset",
            "",
            "No items here",
            "Currently holding 🪓" if inventory == "x" else "Currently holding 🔥",
            "",
        )
    
    # Can pick up
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(sys.maxsize+1)
        mushroom_collected = random.randrange(mushroom_total)
        ground = random.choice(('x', '*'))
        sample_level_info = {
            "size": (r, c),
            "mushroom_collected": mushroom_collected,
            "mushroom_total": mushroom_total,
            "game_end": False,
            "inventory": "",
            "invalid_input": False
        }

        assert create_instructions(
            level_info = sample_level_info,
            character_cell = ground
        ) == (
            "=====================",
            f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
            "=====================",
            "",
            f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
            "",
            f"{mushroom_collected} out of {mushroom_total} mushroom(s) collected"
            "",
            f"[W] Move up",
            f"[A] Move left",
            f"[S] Move down",
            f"[D] Move right",
            f"[!] Reset",
            "",
            "[P] Pick up 🪓" if ground == 'x' else "[P] Pick up 🔥",
            "Not holding anything",
            "",
        )

    # Cannot pick up
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(sys.maxsize+1)
        mushroom_collected = random.randrange(mushroom_total)
        inventory = random.choice(('x', '*'))
        ground = random.choice(('x', '*'))
        sample_level_info = {
            "size": (r, c),
            "mushroom_collected": mushroom_collected,
            "mushroom_total": mushroom_total,
            "game_end": False,
            "inventory": inventory,
            "invalid_input": False
        }

        assert create_instructions(
            level_info = sample_level_info,
            character_cell = ground
        ) == (
            "=====================",
            f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
            "=====================",
            "",
            f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
            "",
            f"{mushroom_collected} out of {mushroom_total} mushroom(s) collected"
            "",
            f"[W] Move up",
            f"[A] Move left",
            f"[S] Move down",
            f"[D] Move right",
            f"[!] Reset",
            "",
            "Cannot pick up 🪓" if ground == 'x' else "Cannot pick up 🔥",
            "Currently holding 🪓" if inventory == "x" else "Currently holding 🔥",
            "",
        )


def test_create_instructions_boundary_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    # Win and Lose case
    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 10,
            "mushroom_total": 10,
            "game_end": True,
            "inventory": "x",
            "invalid_input": False
        },
        character_cell = "+"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"You collected 10 out of 10 mushroom(s)",
        "You win!",
        ""
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 10,
            "mushroom_total": 10,
            "game_end": True,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = "+"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"You collected 10 out of 10 mushroom(s)",
        "You win!",
        ""
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": True,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = "*"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        "You lost!",
        ""
    )

    # Randomized edge cases
    # Randomized win cases
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(sys.maxsize+1)
        inventory = random.choice(('x', '*'))
        sample_level_info = {
            "size": (r, c),
            "mushroom_collected": mushroom_total,
            "mushroom_total": mushroom_total,
            "game_end": True,
            "inventory": inventory,
            "invalid_input": False
        }

        assert create_instructions(
            level_info = sample_level_info,
            character_cell = "+"
        ) == (
            "=====================",
            f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
            "=====================",
            "",
            f"You collected {mushroom_total} out of {mushroom_total} mushroom(s)",
            "You win!",
            ""
        )

    # Randomized lost cases
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(sys.maxsize+1)
        mushroom_collected = random.randrange(mushroom_total)
        inventory = random.choice(('x', '*'))
        sample_level_info = {
            "size": (r, c),
            "mushroom_collected": mushroom_collected,
            "mushroom_total": mushroom_total,
            "game_end": True,
            "inventory": inventory,
            "invalid_input": False
        }

        assert create_instructions(
            level_info = sample_level_info,
            character_cell = "+"
        ) == (
            "=====================",
            f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
            "=====================",
            "",
            "You lost!",
            ""
        )


@pytest.mark.timeout(0.2)
def test_create_instructions_corner_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Huge Print Statements
    # Cannot pick up
    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 2,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "x",
            "invalid_input": False
        },
        character_cell = "x"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"2 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🪓",
        "Currently holding 🪓",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "x",
            "invalid_input": False
        },
        character_cell = "*"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"3 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🔥",
        "Currently holding 🪓",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 2,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = "x"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"2 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🪓",
        "Currently holding 🔥",
        "",
    )

    assert create_instructions(
        level_info = {
            "size": (10, 10),
            "mushroom_collected": 3,
            "mushroom_total": 10,
            "game_end": False,
            "inventory": "*",
            "invalid_input": False
        },
        character_cell = "*"
    ) == (
        "=====================",
        f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
        "=====================",
        "",
        f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
        "",
        f"3 out of 10 mushroom(s) collected"
        "",
        f"[W] Move up",
        f"[A] Move left",
        f"[S] Move down",
        f"[D] Move right",
        f"[!] Reset",
        "",
        "Cannot pick up 🔥",
        "Currently holding 🔥",
        "",
    )

    # Randomized huge print statements
    # Cannot pick up
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(sys.maxsize+1)
        mushroom_collected = random.randrange(mushroom_total)
        inventory = random.choice(('x', '*'))
        ground = random.choice(('x', '*'))
        sample_level_info = {
            "size": (r, c),
            "mushroom_collected": mushroom_collected,
            "mushroom_total": mushroom_total,
            "game_end": False,
            "inventory": inventory,
            "invalid_input": False
        }

        assert create_instructions(
            level_info = sample_level_info,
            character_cell = ground
        ) == (
            "=====================",
            f"🍄 𝗦𝗛𝗥𝗢𝗢𝗠 𝗥𝗔𝗜𝗗𝗘𝗥 🍄",
            "=====================",
            "",
            f"✅ GOAL: Collect all the mushrooms to proceed to the next level!",
            "",
            f"{mushroom_collected} out of {mushroom_total} mushroom(s) collected"
            "",
            f"[W] Move up",
            f"[A] Move left",
            f"[S] Move down",
            f"[D] Move right",
            f"[!] Reset",
            "",
            "Cannot pick up 🪓" if ground == 'x' else "Cannot pick up 🔥",
            "Currently holding 🪓" if inventory == "x" else "Currently holding 🔥",
            "",
        )


def test_create_instructions_invalid_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Type Errors
    # Wrong level_info
    with pytest.raises(TypeError, match="Level_info must be a dictionary."):
        assert create_instructions(
            level_info = (
                "size", (10, 10),
                "mushroom_collected", 3,
                "mushroom_total", 10,
                "game_end", False,
                "inventory", "*",
                "invalid_input", False
            ),
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Level_info must be a dictionary."):
        assert create_instructions(
            level_info = [
                "size", (10, 10),
                "mushroom_collected", 3,
                "mushroom_total", 10,
                "game_end", False,
                "inventory", "*",
                "invalid_input", False
            ],
            character_cell = ""
        )
    
    with pytest.raises(TypeError, match="Level_info must be a dictionary."):
        assert create_instructions(
            level_info = [
                ("size", (10, 10)),
                ("mushroom_collected", 3),
                ("mushroom_total", 10),
                ("game_end", False),
                ("inventory", "*"),
                ("invalid_input", False)
            ],
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Level_info must be a dictionary."):
        assert create_instructions(
            level_info = (
                ("size", (10, 10)),
                ("mushroom_collected", 3),
                ("mushroom_total", 10),
                ("game_end", False),
                ("inventory", "*"),
                ("invalid_input", False)
            ),
            character_cell = ""
        )

    # Size must be tuple[int, int]
    with pytest.raises(TypeError, match="Size must be tuple[int, int]"):
        assert create_instructions(
            level_info = {
                "size": [10, 10],
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Size must be tuple[int, int]"):
        assert create_instructions(
            level_info = {
                "size": (10, 10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Size must be tuple[int, int]"):
        assert create_instructions(
            level_info = {
                "size": (10, "str"),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Size must be tuple[int, int]"):
        assert create_instructions(
            level_info = {
                "size": ((10, 10), ["str"]),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    # Mushroom collected (total) must be int
    with pytest.raises(TypeError, match="Mushroom_collected must be int"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": "10",
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Mushroom_collected must be int"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": "abc",
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Mushroom_collected must be int"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": "",
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Mushroom_total must be int"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": "",
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Mushroom_total must be int"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": "abc",
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Mushroom_total must be int"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": "10",
                "game_end": True,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    # Game_end must be boolean
    with pytest.raises(TypeError, match="Game_end must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": 1,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Game_end must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": 0,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Game_end must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": "",
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Game_end must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": "yes",
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Game_end must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": None,
                "inventory": "*",
                "invalid_input": False
            },
            character_cell = ""
        )

    # Inventory must be str of length 1
    with pytest.raises(ValueError, match="Inventory must be a string with length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "HELLO",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(ValueError, match="Inventory must be a string with length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": 123,
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(ValueError, match="Inventory must be a string with length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": (1, 23),
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(ValueError, match="Inventory must be a string with length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": [1, 23],
                "invalid_input": False
            },
            character_cell = ""
        )

    # Invalid input must be boolean
    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": 0
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": 1
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": None
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": ""
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": "yes"
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": []
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": [1, 23]
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": (1, 23)
            },
            character_cell = ""
        )

    with pytest.raises(TypeError, match="Invalid_input must be boolean"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": ()
            },
            character_cell = ""
        )

    # Character_cell must be string of length 0 or 1
    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = "HELLo"
        )

    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = 1
        )

    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = [1, 23]
        )

    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ()
        )

    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = []
        )

    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = (1, 23)
        )

    with pytest.raises(ValueError, match="Character_cell must be string of length 0 or 1"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": True,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = 1.00 # manifesting
        )

    # NOTE: Invalid keys are in a separate test case (specifically on test_validator)

    ## Value Errors
    with pytest.raises(ValueError, match="Collected mushrooms = total mushrooms must mean game_end"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 10,
                "mushroom_total": 10,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )

    # Randomized
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(1, r*c+1)

        with pytest.raises(ValueError, match="Collected mushrooms = total mushrooms must mean game_end"):
            assert create_instructions(
                level_info = {
                    "size": (r, c),
                    "mushroom_collected": mushroom_total,
                    "mushroom_total": mushroom_total,
                    "game_end": False,
                    "inventory": "",
                    "invalid_input": False
                },
                character_cell = ""
            )
        
    # Mushroom total is greater than total area
    with pytest.raises(ValueError, match="Mushroom total is greater than total area"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 1,
                "mushroom_total": 1000,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )
        
    # Randomized
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(r*c+1, sys.maxsize+1)

        with pytest.raises(ValueError, match="Mushroom total is greater than total area"):
            assert create_instructions(
                level_info = {
                    "size": (r, c),
                    "mushroom_collected": 1,
                    "mushroom_total": mushroom_total,
                    "game_end": False,
                    "inventory": "",
                    "invalid_input": False
                },
                character_cell = ""
            )

    # Collected mushrooms must not exceed total mushrooms
    with pytest.raises(ValueError, match="Collected mushrooms must not exceed total mushrooms"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": 11,
                "mushroom_total": 10,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )

    # Randomized
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(1, r*c+1)

        with pytest.raises(ValueError, match="Collected mushrooms must not exceed total mushrooms"):
            assert create_instructions(
                level_info = {
                    "size": (r, c),
                    "mushroom_collected": random.randrange(mushroom_total+1, sys.maxsize+1),
                    "mushroom_total": mushroom_total,
                    "game_end": False,
                    "inventory": "",
                    "invalid_input": False
                },
                character_cell = ""
            )

    # Mushroom collected / total must be greater than or equal to 0
    with pytest.raises(ValueError, match="Mushroom collected must be greater than or equal to 0"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": -1,
                "mushroom_total": 10,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(ValueError, match="Mushroom collected must be greater than or equal to 0"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": -1,
                "mushroom_total": 1,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(ValueError, match="Mushroom total must be greater than 0"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": -10,
                "mushroom_total": -1,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )

    with pytest.raises(ValueError, match="Mushroom total must be greater than 0"):
        assert create_instructions(
            level_info = {
                "size": (10, 10),
                "mushroom_collected": -10,
                "mushroom_total": 0,
                "game_end": False,
                "inventory": "",
                "invalid_input": False
            },
            character_cell = ""
        )

    # Randomized
    for _ in range(RANDOM_TEST_CASES):
        r, c = random.randrange(1, 31), random.randrange(1, 31)
        mushroom_total = random.randrange(-sys.maxsize, 1)

        with pytest.raises(ValueError, match="Mushroom total must be greater than 0"):
            assert create_instructions(
                level_info = {
                    "size": (r, c),
                    "mushroom_collected": random.randrange(-sys.maxsize, mushroom_total),
                    "mushroom_total": mushroom_total,
                    "game_end": False,
                    "inventory": "",
                    "invalid_input": False
                },
                character_cell = ""
            )

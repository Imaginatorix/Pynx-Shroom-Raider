# ===== FORMAT USED FOR UNIT TESTING =====

# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest
import random

# Import things to test
# from ... import ...

RANDOM_TEST_CASES = 250

# === TESTING <FUNCTION NAME> FUNCTION FROM <FILENAME>.PY ===

def test_function_name_valid_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Valid/Normal Cases (Regular input values within acceptable limits) ===
    assert ...

    # Randomized valid cases
    for _ in range(RANDOM_TEST_CASES):
        assert ...


def test_function_name_boundary_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Blank Case
    assert ...

    # Randomized blank cases
    for _ in range(RANDOM_TEST_CASES):
        assert ...

    ## Other Edge Cases
    assert ...

    # Randomized edge cases
    for _ in range(RANDOM_TEST_CASES):
        assert ...


def test_function_name_corner_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Huge Cases
    assert ...

    # Randomized huge cases
    for _ in range(RANDOM_TEST_CASES):
        assert ...

    ## Difficult Cases
    assert ...

    # Randomized difficult cases
    for _ in range(RANDOM_TEST_CASES):
        assert ...


def test_function_name_invalid_cases():
    # Set random seed
    random.seed(11.11) # Tribute to CS11 Gods

    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Type Errors
    with pytest.raises(TypeError, match="test"):
        assert ...
        raise TypeError("test")
    
    # Randomized type errors
    for _ in range(RANDOM_TEST_CASES):
        with pytest.raises(ValueError, match="test"):
            assert ...
            raise ValueError("test")

    ## Value Errors
    with pytest.raises(ValueError, match="test"):
        assert ...
        raise ValueError("test")
    
    # Randomized value errors
    for _ in range(RANDOM_TEST_CASES):
        with pytest.raises(ValueError, match="test"):
            assert ...
            raise ValueError("test")

    ## Other Errors
    with pytest.raises(KeyError, match="test"):
        assert ...
        raise KeyError("test")
    
    # Randomized other errors
    for _ in range(RANDOM_TEST_CASES):
        with pytest.raises(KeyError, match="test"):
            assert ...
            raise KeyError("test")



# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest

# Import things to test
import re

from utils.validator import validate_size

# === TESTING VALIDATE_SIZE FUNCTION FROM UTILS/VALIDATOR.PY ===

def test_validate_size_valid_cases(valid_size):
    # === Valid/Normal Cases (Regular input values within acceptable limits) ===
    try:
        validate_size(valid_size)
    except Exception as e:
        assert False, e


def test_validate_size_boundary_cases_blank(blank_size):
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Blank Case
    with pytest.raises(ValueError, match=r"^(r|c) must be in between 1 and 30 \(inclusive\)\.$"):
        assert validate_size(blank_size)


def test_validate_size_boundary_cases_edge(edge_size, edge_size_expected):
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Other Edge Cases
    if edge_size_expected == "ValueError":
        with pytest.raises(ValueError, match=re.escape("map area (r*c) must be in between 2 and inf (inclusive).")):
            assert validate_size(edge_size)
    else:
        try:
            validate_size(edge_size)
        except Exception as e:
            assert False, e


@pytest.mark.timeout(1)
def test_validate_size_corner_cases_huge(huge_size):
    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Huge Cases
    try:
        validate_size(huge_size)
    except Exception as e:
        assert False, e


def test_validate_size_invalid_cases_type_errors(type_errors_size):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Type Errors
    with pytest.raises(TypeError, match=re.escape("size must be tuple[int, int]")):
        assert validate_size(type_errors_size)


def test_validate_size_invalid_cases_value_errors(value_errors_size):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Value Errors
    with pytest.raises(ValueError, match=r"^(r|c) must be in between 1 and 30 \(inclusive\)\.$"):
        assert validate_size(value_errors_size)


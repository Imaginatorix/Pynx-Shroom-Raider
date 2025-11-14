# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest
import re

# Import things to test
from utils.validator import validate_locations

# === TESTING VALIDATE_LOCATIONS FUNCTION FROM UTILS/VALIDATOR.PY ===

def test_validate_locations_valid_cases(valid_location):
    # === Valid/Normal Cases (Regular input values within acceptable limits) ===
    r = max((i for val in valid_location.values() for i, j in val))+1
    c = max((j for val in valid_location.values() for i, j in val))+1
    try:
        validate_locations(r, c, valid_location)
    except Exception as e:
        assert False, e


def test_validate_locations_boundary_cases_blank(blank_location):
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Blank Case
    with pytest.raises(ValueError, match="r and c must be between 1 and 30, inclusive"):
        assert validate_locations(0, 0, blank_location)


def test_validate_locations_boundary_cases_edge(edge_location, expected):
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Other Edge Cases
    if expected == "ValueError":
        with pytest.raises(ValueError, match="r and c must be between 1 and 30, inclusive"):
            assert validate_locations(0, 0, edge_location)
    else:
        try:
            r = max((i for val in edge_location.values() for i, j in val))+1
            c = max((j for val in edge_location.values() for i, j in val))+1
            validate_locations(r, c, edge_location)
        except Exception as e:
            assert False, e


@pytest.mark.timeout(1)
def test_validate_locations_corner_cases_huge(huge_location):
    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Huge Cases
    try:
        r = max((i for val in huge_location.values() for i, j in val))+1
        c = max((j for val in huge_location.values() for i, j in val))+1
        validate_locations(r, c, huge_location)
    except Exception as e:
        assert False, e


def test_validate_locations_invalid_cases_type_errors(nonconform_location):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Type Errors
    with pytest.raises(TypeError, match=re.escape("Locations must be dict[str: list[tuple[int, int]]] and key must be a singular character")):
        assert validate_locations(30, 30, nonconform_location)


def test_validate_locations_invalid_cases_value_errors(improper_location):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Value Errors
    with pytest.raises(ValueError, match="Coordinates must completely fill the grid range"):
        r = max((i for val in improper_location.values() for i, j in val))-2
        c = max((j for val in improper_location.values() for i, j in val))-2
        assert validate_locations(r, c, improper_location)


def test_validate_locations_invalid_cases_other_errors(mutated_location):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Other Errors
    with pytest.raises(ValueError, match="Keys must be valid"):
        r = max((i for val in mutated_location.values() for i, j in val))+1
        c = max((j for val in mutated_location.values() for i, j in val))+1
        assert validate_locations(r, c, mutated_location)


def test_validate_locations_invalid_cases_other_errors_lost_lara(lost_lara_location):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Other Errors
    with pytest.raises(ValueError, match="Locations must always contain one Lara"):
        r = max((i for val in lost_lara_location.values() for i, j in val))+1
        c = max((j for val in lost_lara_location.values() for i, j in val))+1
        assert validate_locations(r, c, lost_lara_location)


def test_validate_locations_invalid_cases_other_errors_lost_mushroom(lost_mushroom_location):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Other Errors
    with pytest.raises(ValueError, match="Locations must always have at least one mushroom"):
        r = max((i for val in lost_mushroom_location.values() for i, j in val))+1
        c = max((j for val in lost_mushroom_location.values() for i, j in val))+1
        assert validate_locations(r, c, lost_mushroom_location)

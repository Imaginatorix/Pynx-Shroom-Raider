# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest

# Import things to test
import re

from utils.parser import get_tile_locations

# === TESTING GET_TILE_LOCATIONS FUNCTION FROM UTILS/PARSER.PY ===

def test_get_tile_locations_valid_cases(valid_grid, valid_locations):
    # === Valid/Normal Cases (Regular input values within acceptable limits) ===
    assert get_tile_locations(valid_grid) == valid_locations


def test_get_tile_locations_boundary_cases_blank(blank_grid):
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Blank Case
    with pytest.raises(ValueError, match=re.escape("r must be in between 1 and 30 (inclusive).")):
        assert get_tile_locations(blank_grid)


def test_get_tile_locations_boundary_cases_edge(edge_grid, edge_locations):
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Other Edge Cases
    if edge_locations == "ValueError":
        with pytest.raises(ValueError, match=re.escape("map area (r*c) must be in between 2 and inf (inclusive).")):
            assert get_tile_locations(edge_grid)
    else:
        assert get_tile_locations(edge_grid) == edge_locations


@pytest.mark.timeout(1)
def test_get_tile_locations_corner_cases_huge(huge_grid, huge_locations):
    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Huge Cases
    assert get_tile_locations(huge_grid) == huge_locations


def test_get_tile_locations_invalid_cases_type_errors(type_errors_grid):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Type Errors
    with pytest.raises(TypeError, match=re.escape("grid must be list[str]")):
        assert get_tile_locations(type_errors_grid)


def test_get_tile_locations_invalid_cases_value_errors(value_errors_grid_improper):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Value Errors
    with pytest.raises(ValueError, match="Coordinates must completely fill the grid range"):
        assert get_tile_locations(value_errors_grid_improper)


def test_get_tile_locations_invalid_cases_other_errors(value_errors_grid_mutated):
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Other Errors
    with pytest.raises(ValueError, match="Tiles must be valid"):
        assert get_tile_locations(value_errors_grid_mutated)

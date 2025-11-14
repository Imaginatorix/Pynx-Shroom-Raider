# # Make higher level directories visible
# import sys
# from os import path
# sys.path.append(path.abspath("."))

# import pytest

# # Import things to test
# from utils.parser import get_locations

# # === TESTING GET_LOCATIONS FUNCTION FROM UTILS/PARSER.PY ===

# def test_get_locations_valid_cases(valid_grid_locations, expected):
#     # === Valid/Normal Cases (Regular input values within acceptable limits) ===
#     assert get_locations(valid_grid_locations) == expected


# def test_get_locations_boundary_cases_blank(blank_grid):
#     # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
#     ## Blank Case
#     with pytest.raises(ValueError, match="Size of map must have at least an area of 2"):
#         assert get_locations(blank_grid)


# def test_get_locations_boundary_cases_edge(edge_grid, expected):
#     # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
#     ## Other Edge Cases
#     if expected == "ValueError":
#         with pytest.raises(ValueError, match="Size of map must have at least an area of 2"):
#             assert get_locations(edge_grid)
#     else:
#         assert get_locations(edge_grid) == expected


# @pytest.mark.timeout(1)
# def test_get_locations_corner_cases_huge(huge_grid, expected):
#     # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
#     ## Huge Cases
#     assert get_locations(huge_grid) == expected


# def test_get_locations_invalid_cases_type_errors(nonconform_grid):
#     # === Invalid/Error Cases (Values that fall outside the valid range) ===
#     ## Type Errors
#     with pytest.raises(TypeError, match="Grid must be list of strings"):
#         assert get_locations(nonconform_grid)


# def test_get_locations_invalid_cases_value_errors(improper_grid):
#     # === Invalid/Error Cases (Values that fall outside the valid range) ===
#     ## Value Errors
#     with pytest.raises(ValueError, match="Grid must have consistent rows and columns"):
#         assert get_locations(improper_grid)


# def test_get_locations_invalid_cases_other_errors(mutated_grid):
#     # === Invalid/Error Cases (Values that fall outside the valid range) ===
#     ## Other Errors
#     with pytest.raises(ValueError, match="Tiles must be valid"):
#         assert get_locations(mutated_grid)


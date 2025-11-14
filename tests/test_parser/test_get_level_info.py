# # Make higher level directories visible
# import sys
# from os import path
# sys.path.append(path.abspath("."))

# import pytest

# # Import things to test
# from utils.parser import get_level_info

# # === TESTING GET_LEVEL_INFO FUNCTION FROM UTILS/PARSER.PY ===

# def test_get_level_info_valid_cases(valid_size, valid_locations):
#     # === Valid/Normal Cases (Regular input values within acceptable limits) ===
#     assert get_level_info(valid_size, valid_locations) == {
#         "size": valid_size,
#         "mushroom_collected": 0,
#         "mushroom_total": len(valid_locations['+']),
#         "game_end": False,
#         "inventory": "",
#         "invalid_input": False,
#         "level_reset": False,
#     }


# def test_get_level_info_boundary_cases_blank(blank_size):
#     # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
#     ## Blank Case
#     with pytest.raises(ValueError, match="Size of map must have at least an area of 2"):
#         assert get_level_info(blank_size)


# def test_get_level_info_boundary_cases_edge(edge_size, edge_locations, expected):
#     # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
#     ## Other Edge Cases
#     if expected == "ValueError":
#         with pytest.raises(ValueError, match="Size of map must have at least an area of 2"):
#             assert get_level_info(edge_size)
#     else:
#         assert get_level_info(edge_size) == {
#         "size": edge_size,
#         "mushroom_collected": 0,
#         "mushroom_total": len(edge_locations['+']),
#         "game_end": False,
#         "inventory": "",
#         "invalid_input": False,
#         "level_reset": False,
#     }


# @pytest.mark.timeout(1)
# def test_get_level_info_corner_cases_huge(huge_size):
#     # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
#     ## Huge Cases
#     assert get_level_info(huge_size) == expected


# def test_get_level_info_invalid_cases_type_errors(nonconform_grid):
#     # === Invalid/Error Cases (Values that fall outside the valid range) ===
#     ## Type Errors
#     with pytest.raises(TypeError, match="Grid must be list of strings"):
#         assert get_level_info(nonconform_grid)


# def test_get_level_info_invalid_cases_value_errors(improper_grid):
#     # === Invalid/Error Cases (Values that fall outside the valid range) ===
#     ## Value Errors
#     with pytest.raises(ValueError, match="Grid must have consistent rows and columns"):
#         assert get_level_info(improper_grid)


# def test_get_level_info_invalid_cases_other_errors(mutated_grid):
#     # === Invalid/Error Cases (Values that fall outside the valid range) ===
#     ## Other Errors
#     with pytest.raises(ValueError, match="Tiles must be valid"):
#         assert get_level_info(mutated_grid)


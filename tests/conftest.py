# === GENERATE TEST CASES FOR ALL TESTS ===
from pytest import Metafunc

import data_generator.grid as grid_data
import data_generator.size as size_data
import data_generator.locations as locations_data

PARAMS = {
    # GRIDS
    "valid_grid": grid_data.VALID,
    "blank_grid": grid_data.BLANK,
    "edge_grid": grid_data.EDGE,
    "huge_grid": grid_data.HUGE,
    "type_errors_grid": grid_data.TYPE_ERRORS,
    "value_errors_grid_improper": grid_data.VALUE_ERRORS_IMPROPER,
    "value_errors_grid_mutated": grid_data.VALUE_ERRORS_MUTATED,
    # LOCATIONS
    "valid_locations": locations_data.VALID,
    "blank_locations": locations_data.BLANK,
    "edge_locations": locations_data.EDGE,
    "huge_locations": locations_data.HUGE,
    "type_errors_locations": locations_data.TYPE_ERRORS,
    # SIZE
    "valid_size": size_data.VALID,
    "blank_size": size_data.BLANK,
    "edge_size": size_data.EDGE,
    "edge_size_expected": size_data.EDGE_EXPECTED,
    "huge_size": size_data.HUGE,
    "type_errors_size": size_data.TYPE_ERRORS,
    "value_errors_size": size_data.VALUE_ERRORS,
}


def pytest_generate_tests(metafunc: Metafunc):
    names = tuple(n for n in PARAMS if n in metafunc.fixturenames)

    if len(names) >= 1:
        metafunc.parametrize(
            names,
            zip(*(PARAMS[n] for n in names)),
        )

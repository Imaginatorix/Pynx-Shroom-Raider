# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest

# Import things to test
# from ... import ...

# === TESTING <FUNCTION NAME> FUNCTION FROM <FILENAME>.PY ===

def test_function_name_valid_cases():
    # === Valid/Normal Cases (Regular input values within acceptable limits) ===
    assert ...


def test_function_name_boundary_cases_blank():
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Blank Case
    assert ...


def test_function_name_boundary_cases_edge():
    # === Boundary Cases (Values at the boundaries of the acceptable limits) ===
    ## Other Edge Cases
    assert ...


@pytest.mark.timeout(1)
def test_function_name_corner_cases_huge():
    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Huge Cases
    assert ...


@pytest.mark.timeout(1)
def test_function_name_corner_cases_difficult():
    # === Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system) ===
    ## Difficult Cases
    assert ...


def test_function_name_invalid_cases_type_errors():
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Type Errors
    with pytest.raises(TypeError, match="test"):
        assert ...
        raise TypeError("test")


def test_function_name_invalid_cases_value_errors():
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Value Errors
    with pytest.raises(ValueError, match="test"):
        assert ...
        raise ValueError("test")


def test_function_name_invalid_cases_other_errors():
    # === Invalid/Error Cases (Values that fall outside the valid range) ===
    ## Other Errors
    with pytest.raises(KeyError, match="test"):
        assert ...
        raise KeyError("test")



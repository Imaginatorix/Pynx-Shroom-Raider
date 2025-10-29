# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))
sys.path.append(path.abspath("./utils"))

from utils.ui import show_screen
import pytest

# === TESTING SHOW_SCREEN FUNCTION FROM UTILS/UI.PY ===

def test_show_screen():
    # Valid/Normal Cases (Regular input values within acceptable limits)
    assert ...

    # Boundary Cases (Values at the boundaries of the acceptable limits)
    ## Black Case
    assert ...
    ## Other Edge Cases
    assert ...

    # Corner Cases (Values that represent extreme or unusual scenarios that could affect the unit or even the system)
    ## Huge Cases
    assert ...
    ## Difficult Cases
    assert ...

    # Invalid/Error Cases (Values that fall outside the valid range)
    ## Type Errors
    with pytest.raises(TypeError, match="test"):
        assert ...
        raise TypeError("test")
    ## Value Errors
    with pytest.raises(ValueError, match="test"):
        assert ...
        raise ValueError("test")
    ## Other Errors
    with pytest.raises(KeyError, match="test"):
        assert ...
        raise KeyError("test")



# === ADD EXTRA TEST CASES HERE (OR IN A SEPARATE FILE IN THE SAME DIRECTORY) ===

# Make higher level directories visible
import sys
from os import path
sys.path.append(path.abspath("."))

import pytest

# Import things to test
# from shroom_raider import ...

def test_my_test_cases():
    assert ...


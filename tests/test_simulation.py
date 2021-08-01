'''
Test cases for the simulation module
'''

# this is so py.test can be run from both the main directory as well
# as the test/ subdir
import sys
sys.path.append(".")
sys.path.append("..")


import simulation as s

import pytest
import numpy as np


@pytest.mark.parametrize(
    "n_deli,n_pick,x_max,y_max",
    [
        (10, 5, 20, 20),
        (10, 0, 20, 20),
        (0, 0, 20, 20),
        (10, 5, 20, 10),
        (200, 100, 200, 100)
    ])
def test_generate_events(n_deli, n_pick, x_max, y_max):
    deli, pick = s.generate_events(n_deli, n_pick, x_max, y_max, 42)

    assert deli.shape == (3, n_deli)
    assert pick.shape == (3, n_pick)

    for e in [deli, pick]:
        x = e[0]
        assert (x > -x_max).all()
        assert (x < +x_max).all()

        y = e[1]
        assert (y > -y_max).all()
        assert (y < +y_max).all()

        c = e[2]
        assert (c > 0).all()


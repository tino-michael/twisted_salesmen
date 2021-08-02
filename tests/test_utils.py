'''
Test cases for the utilities module
'''

# this is so py.test can be run from both the main directory as well
# as the test/ subdir
import sys
sys.path.append(".")
sys.path.append("..")

import pytest
import numpy as np

from routing.utils import distance_weights


@pytest.mark.parametrize(
    "xs,ys,origin,expected",
    [
        ([0, 1, 3, 10], [0, 0, 4, 10], (0, 0), [1, 1, 0.2, 200**-0.5]),
        ([0, 1, 3, 10], [0, 0, 4, 10], (1, -1), [2**-0.5, 1, 29**-0.5, 202**-0.5])
    ])
def test_distance_weights(xs, ys, origin, expected):
    '''
    Tests that the weight function does the right thing
    '''
    a = np.array([xs, ys])
    res = distance_weights(a, origin)

    assert (res == expected).all()


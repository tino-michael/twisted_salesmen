'''
This tests the route validation function which calculates the length of the route and whether
there is exactly one pickup event.
'''

import sys
import numpy as np
import pytest
sys.path.append(".")
sys.path.append("..")

from routing.route_validator import validate_length_one_pickup


@pytest.mark.parametrize(
    "e_type,expected",
    [
        (['d', 'd', 'd', 'd'], False),
        (['d', 'p', 'd', 'd'], True),
        (['p', 'd', 'd', 'd'], True),
        (['p', 'p', 'p', 'p'], False),
        (['p', 'p', 'd', 'd'], False)
    ])
def test_route_validator_one_pickup(e_type, expected):
    '''
    This tests if the validator correctly picks up on the number of pickup events on-route
    '''
    route = range(4)
    deli = np.arange(12).reshape(3, -1)
    _, result = validate_length_one_pickup(route, e_type, deli, deli)

    assert result == expected


@pytest.mark.parametrize(
    "xs,ys,expected",
    [
        ([1, 1, 0], [0, 1, 1], 4),
        ([1, 1, -1, -1, 1, 1], [0, 1, 1, -1, -1, 0], 10)
    ])
def test_route_validator_length(xs, ys, expected):
    '''
    This tests if the validator correctly calculates the length of the route,
    including from depot and back
    '''
    route = np.arange(len(xs))
    deli = np.array([xs, ys, np.zeros_like(xs)])
    e_type = ['d'] * len(xs)

    length, _ = validate_length_one_pickup(route, e_type, deli, deli)

    assert length == expected


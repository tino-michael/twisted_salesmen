'''
This module takes care of simulating delivery and pickup events
'''

import numpy as np


def generate_sub_events(n_evts, x_max, y_max, rng):
    '''
    Generates a set of events with positions and capacities

    The events will be distributed in a box from (-x_max, -y_max)
    to (x_max, y_max) around the origin.

    The capacities are generated using a Poisson distribution so that
    most events will have a capacity around 20 and the maximum will be
    around 60.

    Parameter
    ---------
    n_evts:
        number of events to be generated
    x_max:
        maximum x distance from the origin (in either direction)
    y_max:
        maximum y distance from the origin (in either direction)
    '''

    # generate the locations of the events
    pos_x = rng.uniform(-x_max, x_max, n_evts)
    pos_y = rng.uniform(-y_max, y_max, n_evts)

    # generate the capacities of the events so that there are many smaller ones
    # and only a few very large ones using a poisson distribution
    cap = rng.poisson(2.5, n_evts) * 10
    # zero-capacity events make no sense, so bump them up to 5 at least
    cap[cap == 0] = 5

    # this arranges the generated data in tuples of [x, y, c] belonging to one event
    return np.array([pos_x, pos_y, cap])


def generate_events(n_deli, n_pick, x_max, y_max, seed=None):
    '''
    Generates delivery and pickup events within a region around the depot at (0,0).

    Deliveries and pickups are in the same area but can have different numbers.
    Generates two seperate sets reusing the same seeded random number generator.

    Parameter
    ---------
    n_del:
        number of delivery events to be generated
    n_pick:
        number of pickup events to be generated
    x_max:
        maximum x distance from the origin (in either direction)
    y_max:
        maximum y distance from the origin (in either direction)
    '''

    rng = np.random.default_rng(seed)

    deliveries = generate_sub_events(n_deli, x_max, y_max, rng)
    pickups = generate_sub_events(n_pick, x_max, y_max, rng)

    return deliveries, pickups

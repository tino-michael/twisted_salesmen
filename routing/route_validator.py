'''
This Module provides validator functions for a given route
'''
import numpy as np

def validate_length_one_pickup(route, e_type, deli, pick):
    '''
    This function calculate the length of the given route -- including from and back to depot --
    and validates that there is exactly one pickup event contained

    Parameter
    ---------
    route:
        sorted event index list defining the route
    e_type:
        list of 'p' or 'd' characters defining whether event is delivery or pickup

    deli, pick:
        ndarrays with shape (3, n) defining the x and y coordinates and capacities for all
        delivery and pickup events, respectively
    '''
    # events have a third component -- capacity --
    # so manually calculate distance from the first two only
    def dist(one, two):
        return ((one[0] - two[0])**2 + (one[1] - two[1])**2)**.5

    route_length = 0
    origin = np.array([0, 0])
    last = origin

    for idx, typ in zip(route, e_type):
        if typ == 'p':
            evt = pick[:, idx]
            route_length += dist(last, evt)
            last = evt
        elif typ == 'd':
            evt = deli[:, idx]
            route_length += dist(last, evt)
            last = evt

    route_length += dist(last, origin)

    one_pickup = (e_type.count('p') == 1)

    return route_length, one_pickup

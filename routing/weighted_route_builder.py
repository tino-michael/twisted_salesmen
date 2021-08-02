import numpy as np

from .utils import distance_weights_exp


def select_next_event(route, events, capacity):
    '''
    Given an existing partial route and a pool of events, selects the next event.

    Events already visited and not "fitting" into the van are dropped.
    From the remaining events a random one is drawn with draw weight given by the distance-weight
    function.

    Return:
    -------
    selected:
        the index of the selected event

    Raises:
    -------
    RuntimeError:
        if no event is left after the initial pruning (already visited + capacity constraints)
    '''
    # enumerate all events; keep track of them via their index
    event_ids = np.arange(events.shape[1])

    # remove events that would no longer fit into the van
    candidate_ids = event_ids[events[2] <= capacity]

    # remove ids already visited
    candidate_ids = np.setdiff1d(candidate_ids, route)

    # if no candidates are left, there is nothing else to be done
    # raise `RuntimeError` and use it as exit condition in the loop outside
    if candidate_ids.size == 0:
        raise RuntimeError

    # these events are candidates to visit next
    candidates = events[:, candidate_ids]

    # calculate the distance to all candidate events either from last visited event
    # or from the depot at (0, 0)
    origin = events[:, route[-1]] if route else (0, 0)
    draw_weights = distance_weights_exp(candidates, origin)

    # random draw next event to visit weighted by their distance to current position
    selected = np.random.choice(candidate_ids, p=draw_weights/np.sum(draw_weights))

    return selected


def build_route(deliveries, pickups, van_capacity, load=0, route=[], evt_types=[]):
    '''
    Builds a route (or continues the given one) by iteratively calling `select_next_event` for
    either pickup or delivery events.

    By making the probabilty of selecting a pickup event dependent on how "full" the delivery van
    already is, provides for a reasonably flat probability distribution for the pickup event along
    the entire route. If one were to use a constant probability, the distribution would be skewed
    towards earlier events.

    Return:
    -------
    route:
        python list of event indices defining the route
    evt_types:
        python list of 'p' or 'd' characters defining pickup or delivery event
    '''
    while True:
        try:
            # decide whether do add a delivery or pickup event next.
            # there ought to be only one pickup event, so check that there isn't one yet and
            # randomly decide to pick a pickup event with the probabilty increasing as the van
            # fills up
            if ('p' not in evt_types) and (np.random.random() < load/van_capacity):
                p_route = [r for r, e in zip(route, evt_types) if e == 'p']
                idx = select_next_event(p_route, pickups, van_capacity-load)
                route += [idx]
                evt_types += ['p']

            else:
                d_route = [r for r, e in zip(route, evt_types) if e == 'd']
                idx = select_next_event(d_route, deliveries, van_capacity - load)
                load += deliveries[2, idx]
                route += [idx]
                evt_types += ['d']

        except RuntimeError:
            break

    return route, evt_types


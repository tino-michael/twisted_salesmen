import numpy as np

from .utils import distance_weights_exp, only_deliveries, only_pickups, get_capacity


def select_next_event(origin, route, events, capacity):
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

    # calculate the distance to all candidate events from last visited event
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

    if len(evt_types) == 0:
        recent = (0, 0)
    elif evt_types[-1] == 'd':
        recent = deliveries[0:2, route[-1]]
    else:
        recent = pickups[0:2, route[-1]]

    while True:
        try:
            # decide whether do add a delivery or pickup event next.
            # there ought to be only one pickup event, so check that there isn't one yet and
            # randomly decide to pick a pickup event with the probabilty increasing as the van
            # fills up
            if ('p' not in evt_types) and (np.random.random() < load/van_capacity):
                p_route = only_pickups(route, evt_types)
                idx = select_next_event(recent, p_route, pickups, van_capacity-load)
                route += [idx]
                evt_types += ['p']
                recent = pickups[0:2, idx]

            else:
                d_route = only_deliveries(route, evt_types)
                idx = select_next_event(recent, d_route, deliveries, van_capacity - load)
                load += deliveries[2, idx]
                route += [idx]
                evt_types += ['d']
                recent = deliveries[0:2, idx]

        except RuntimeError:
            break

    return route, evt_types


def rebuild_route(deliveries, pickups, van_capacity, route, evt_types):
    '''
    Rebuilds a route by randomly picking an event along the route, throwing away all events
    after and drawing new events from there.
    '''
    cut_off = np.random.randint(len(route))
    r_pruned = route[:cut_off]
    e_pruned = evt_types[:cut_off]

    c_pruned = get_capacity(r_pruned, e_pruned, deliveries)

    return build_route(deliveries, pickups, van_capacity, c_pruned, r_pruned, e_pruned)


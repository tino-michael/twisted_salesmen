#!/usr/bin/env python3

from arguments import setup_arguments
import simulation as sim
from routing import single_best

ap = setup_arguments()

args = ap.parse_args()

deli, pick = sim.generate_events(
    n_deli=args.number_deliveries,
    n_pick=args.number_pickups,
    x_max=args.region_extent_x,
    y_max=args.region_extent_y,
    seed=args.simulation_seed)

best_route, evt_types, route_length = single_best(
    args.van_capacity, deli, pick,
    args.generations, args.spawn_rate, args.survival_rate, args.routing_seed)

# print out results and validate consistency

print("the best route:")
print(best_route)
print("\nwith event types:")
print(evt_types)
print(f"\n{len(evt_types)-2} service stops and total distance of: {route_length}")

print("\nsimulating ride:")
# loading up every delivery
load = 0
for r, e in zip(best_route, evt_types):
    if e == 'd':
        load += deli[2, r]

# running route
for i, (r, e) in enumerate(zip(best_route, evt_types)):
    print(f"Stop {i}")
    if e == 'p':
        evt_load = int(pick[2, r])
        load += evt_load
        print(f"Pickup: {evt_load}")
    elif e == 'd':
        evt_load = int(deli[2, r])
        load -= evt_load
        print(f"Delivery: {evt_load}")
    elif e == 'o':
        print("Depot Stop: " + ("finishing" if i else "starting") + " route")
    print(f"current load: {int(load)} / {args.van_capacity}\n")

    if load > args.van_capacity:
        raise RuntimeError("Loaded more than van can carry!")


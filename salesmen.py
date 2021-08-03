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

single_best(
    args.van_capacity, deli, pick,
    args.routing_seed, args.spawn_rate, args.survival_rate, args.generations)

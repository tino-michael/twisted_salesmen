#!/usr/bin/env python3

from arguments import setup_arguments
import simulation as sim

ap = setup_arguments()

args = ap.parse_args()

deli, pick = sim.generate_events(
    n_deli=args.number_deliveries,
    n_pick=args.number_pickups,
    x_max=args.region_extent_x,
    y_max=args.region_extent_y,
    seed=args.simulation_seed)


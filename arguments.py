'''
This module provides functions to setup the command line arguments
'''

import argparse


def setup_arguments(ap=None):
    '''
    Sets up the argument parser.

    Either adds to an existing parser or creates a new one

    Parameter
    ---------

    ap (default: None)
        Already existing argument parser to which new arguments will be added
        If None, a new parser will be created

    '''
    ap = ap or argparse.ArgumentParser()

    sim_group = ap.add_argument_group(
        title="simulation",
        description="controls the simulation of delivery and pickup events")

    sim_group.add_argument(
        "--number_deliveries", type=int, default=200,
        help="number of delivery points to generate",)
    sim_group.add_argument(
        "--number_pickups", type=int, default=50,
        help="number of pickup points to generate")
    sim_group.add_argument(
        "--region_extent_x", type=int, default=100,
        help="maximum distance from depot at (0,0) in x direction to generate an event")
    sim_group.add_argument(
        "--region_extent_y", type=int, default=100,
        help="maximum distance from depot at (0,0) in y direction to generate an event")
    sim_group.add_argument(
        "--simulation_seed", type=int, default=None,
        help="give a seed for the random simulation of the delivery and pickup events")

    routing_group = ap.add_argument_group(
        title="routing",
        description="controls the plotting of the 'best' route")

    routing_group.add_argument(
        "--van_capacity", type=int, default=200,
        help="the capacity of the van; "
        "a higher capacity means more delivery points can be served")
    routing_group.add_argument(
        "--routing_seed", type=int, default=None,
        help="give a seed for the randomnes in the event routing")
    routing_group.add_argument(
        "--spawn_rate", type=int, default=5,
        help="how many child routes a parent ought to spawn each generation")
    routing_group.add_argument(
        "--survival_rate", type=int, default=5,
        help="how many routes are to survive each generation")
    routing_group.add_argument(
        "--generations", type=int, default=100,
        help="for how many generations, new routes are to be spawned to find the best one")

    return ap

'''
module provides weighting function for the random selection of the next event
'''
import numpy as np


def distance_weights(events, origin=(0, 0)):
    '''
    This function provides weights inversely proportional to the distance between events
    '''
    sq_dists = ((events[0]-origin[0])**2 + (events[1]-origin[1])**2)
    sq_dists[sq_dists == 0] = 1
    return sq_dists**-0.5


def distance_weights_exp(events, origin=(0, 0)):
    '''
    This function penalizes far events even more than `distance_weights`
    through exponential drop-off
    '''
    sq_dists = ((events[0]-origin[0])**2 + (events[1]-origin[1])**2)
    sq_dists[sq_dists == 0] = 1
    return np.exp(-(sq_dists**.5) / 100)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 11:21:55 2020

@author: alysonweidmann
"""
import math
import random
from collections import deque

"""

"""


def dist(xy1, xy2):
    """ Calculate the Euclidean distance between two points.

    """
    # TODO: Implement this function!
    x1 = xy1[0]
    x2 = xy2[0]
    
    y1 = xy1[1]
    y2 = xy2[1]
    
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


class TravelingSalesmanProblem:
    """ Representation of a traveling salesman optimization problem.
    
    An instance of this class represents a complete circuit of the cities
    in the `path` attribute.
    
    
    Parameters
    ----------
    cities : iterable
        An iterable sequence of cities; each element of the sequence must be
        a tuple (name, (x, y)) containing the name and coordinates of a city
        on a rectangular grid. e.g., ("Atlanta", (585.6, 376.8))
        
    shuffle : bool
        If True, then the order of the input cities (and therefore the starting
        city) is randomized.
    
    Attributes
    ----------
    names : sequence
        An iterable sequence (list by default) containing only the names from
        the cities in the order they appear in the current TSP path

    coords : sequence
        An iterable sequence (list by default) containing only the coordinates
        from the cities in the order they appear in the current TSP path

    path : tuple
        A path between cities as specified by the order of the city
        tuples in the list.
    """
    def __init__(self, cities, shuffle=False):
        if shuffle:
            cities = list(cities)
            random.shuffle(cities)
        self.path = tuple(cities)  
        self.__utility = None  

            
        
    def copy(self, shuffle=False):
        cities = list(self.path)
        if shuffle: random.shuffle(cities)
        return TravelingSalesmanProblem(cities)
    
    @property
    def names(self):
        """Strip and return only the city name from each element of the
        path list. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> ["Atlanta", ...]
        """
        names, _ = zip(*self.path)
        return names
    
    @property
    def coords(self):
        """ Strip the city name from each element of the path list and
        return a list of tuples containing only pairs of xy coordinates
        for the cities. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
        """
        _, coords = zip(*self.path)
        return coords
    
    @property
    def utility(self):
        """ Calculate and cache the total distance of the path in the
        current state.
        """
        if self.__utility is None:
            self.__utility = self.__get_value()
        return self.__utility
    
    def successors(self):
        """ Return a list of states in the neighborhood of the current state.
        
        
        Returns
        -------
        iterable<Problem>
            A list of TravelingSalesmanProblem instances initialized with their list
            of cities set to one of the neighboring permutations of cities in the
            present state
        """
        # TODO: Implement this function!
        initial_state = list(self.names)
        n = len(initial_state)
        n_states = math.factorial(n-1)
        
        end_point = initial_state[-1]
        
        neighbors = deque(maxlen=n_states)
        while True:
            k = random.sample(initial_state[:n-1], n-1)
            if k not in neighbors:
                neighbors.append(k)
            if len(neighbors) == neighbors.maxlen:
                break
        
        for i in neighbors:
            i.append(end_point)
            
        path_dict = dict(self.path)
        
        successors = list(TravelingSalesmanProblem(list((i, path_dict[i]) for i in x)) for x in neighbors)
        
        return successors
    
    def get_successor(self):
        """ Return a random state from the neighborhood of the current state.
    

        Returns
        -------
        list<Problem>
            A list of TravelingSalesmanProblem instances initialized with their list
            of cities set to one of the neighboring permutations of cities in the
            present state
        """
        # TODO: Implement this function!
        neighbors = self.successors()
        return random.choice(neighbors)

    def __get_value(self):
        """ Calculate the total length of the closed-circuit path of the current
        state by summing the distance between every pair of cities in the path
        sequence. 
        
        Returns
        -------
        float
            A floating point value with the total cost of the path given by visiting
            the cities in the order according to the self.cities list

        """
        # TODO: Implement this function!
        current_path = list(self.names)
        current_path.append(current_path[0])
        
        path_dict = dict(self.path)
        
        path_lengths = []
        for current, next in zip(current_path, current_path[1:]):
            distance = dist(path_dict[current], path_dict[next])
            path_lengths.append(distance)
            
        return sum(path_lengths)
    
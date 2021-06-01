#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" Program to find the cheapest path using A* search """
__author__="Ovezmyrat Arnazarov"

import os
import sys
from math import radians, cos, sin, asin, sqrt

distances = dict()          # dictionary that saves each city with adjacent neighbour cities and distances
coordinates = dict()        # dictionary that saves latitue and longitude values of every city
start = "Arad"              # start city
goal = "Bucharest"          # goal city

# populates city coordinates to 'distances' dictionary
def pop_coordinates(coordinatesLines):
    for line in coordinatesLines:
        temp_list = line.rstrip("\n").split(",")
        coordinates_list = [temp_list[1]]
        coordinates_list.append(temp_list[2])
        coordinates[temp_list[0]] = coordinates_list

# populates adjacent neighbours and distances to 'coordinates' dictionary
def pop_distances(costLines):
    for line in costLines:
        temp_list = line.rstrip("\n").split(",")
        cost_list = [temp_list[1]]
        cost_list.append(temp_list[2])
        if temp_list[0] in distances:
            distances[temp_list[0]].append(cost_list)
        else:
            distances[temp_list[0]] = [cost_list]

# gets adjacent neighbours list with distances of a given node or city
def get_neighbours(node):
    return distances[node]

# calculates straight line distances in miles using longitude and 
# latitude values of any given two cities
def straight_line_distance(node, goal):
    lat1 = radians(float(coordinates[node][0]))
    lon1 = radians(float(coordinates[node][1]))
    lat2 = radians(float(coordinates[goal][0]))
    lon2 = radians(float(coordinates[goal][1]))

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # radius for earth in miles
    r = 3956

    return c * r

# prints the path from start city to a goal city
def reconstruct_path(cameFrom, current):
    path = []

    while cameFrom[current] != current:
        path.append(current)
        current = cameFrom[current]

    path.append(start)
    path.reverse()

    print("Path found: {}".format(path))

# A* search algorithm finds path from start to goal
def A_Star(start, goal):
    # List of discovered cities. Initially, only the start city is known
    open = []        

    # List of visited cities
    closed = []

    # g is the distance in miles from one city to another
    g = {}
    g[start] = 0

    # h is the heuristic function which is straigh-line distance from any given two cities
    h = {}
    h[start] = straight_line_distance(start, goal)

    # f = g + h and represents our current estimated cost of the best path 
    f = {}
    f[start] = g[start] + h[start]

    # For a city n, cameFrom[n] is the city preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = {}
    cameFrom[start] = start

    open.append((f[start], start))

    while open:
        current = None

        # find a city with the lowest value of f() - evaluation function - from the open list
        for i in range(len(open)):
            if current == None or open[i][0] < value:   # get a node with the least cost
                value = open[i][0]
                current = open[i][1]

        # if the current city is the goal city, print out the reconstrucuted path
        if current == goal:
            print("Total distance: {}".format(g[current]))
            return reconstruct_path(cameFrom, current)

        # for all neighbors of the current city calculate f() values and save to open list
        for (neighbor, weight) in get_neighbours(current):
            if neighbor not in f:
                f[neighbor] = 9999 

            # if the current city is not in both open and closed lists
            # then add it to open list and save current as its parent
            if (f[neighbor], neighbor) not in open and (f[neighbor], neighbor) not in closed:
                    cameFrom[neighbor] = current
                    g[neighbor] = g[current] + int(weight)
                    f[neighbor] = g[neighbor] + straight_line_distance(neighbor, goal)
                    open.append((f[neighbor], neighbor))
            
            # otherwise, check if it is faster to first visit current, then neighbor
            # and if it is, update parent and f() value
            else:
                g[neighbor] = g[current] + int(weight)
                if f[neighbor] > g[neighbor] + straight_line_distance(neighbor, goal):
                    f[neighbor] = g[neighbor] + straight_line_distance(neighbor, goal) 
                    cameFrom[neighbor] = current
                    
                    # if neihgbor in the closed list, move it to open list
                    if neighbor in closed:
                        for item in open:
                            if current in item:
                                closed.remove(item)
                        open.append((f[neighbor], neighbor))

        # remove current from open list and add it to closed list
        # because all neihgbors are inspected
        for item in open:
            if current in item:
                open.remove(item)
        closed.append((f[current],current))

    return "Path not found"
    
# main function that executes the algorithm based on given command line parameters
def main(commandLine):
    cityCosts = None
    cityCoordinates = None
    global start
    global goal

    if len(commandLine) == 5:
        cityCosts = open(str(sys.argv[1]), "r")
        cityCoordinates = open(str(sys.argv[2]), "r")
        start = str(sys.argv[3])
        goal = str(sys.argv[4])
        costLines = cityCosts.readlines()
        coordinatesLines = cityCoordinates.readlines()     
        pop_coordinates(coordinatesLines)
        pop_distances(costLines)
        cityCosts.close()
        cityCoordinates.close()  
        A_Star(start, goal)

    elif len(commandLine) == 2 and str(commandLine[1]) == 'help':
        print('\nThis program implements A* search algorithm to find the cheapest or qucikest path in a map with distance routes and straight-line distances as a heuristic value.\n' +
        'The algorithm outputs total distance and the cheapest path from start city to the goal city.\nTo execute the algorithm, the user should enter filenames and parameters' +
        ' in the following manner:\n python final_project.py "filename with distance routes" "filename with coordinates" "name of the start city" "name of the goal city"\n' +
        'Enter full filename path for a proper execution. If filenames and parameters are ommitted, the algorithm automatically calculates the path from "Arad" to "Bucharest".')
        
    else: 
        cityCosts = open("city_costs.txt", "r")
        cityCoordinates = open("city_coordinates.txt", "r")
        costLines = cityCosts.readlines()
        coordinatesLines = cityCoordinates.readlines()     
        pop_coordinates(coordinatesLines)
        pop_distances(costLines)
        cityCosts.close()
        cityCoordinates.close()  
        A_Star(start, goal)
    

main(sys.argv)
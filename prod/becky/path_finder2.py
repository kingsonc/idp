from copy import deepcopy
import math
import cv2
import numpy as np
from config import current_config as config

def table3():
    # Left limit
    pts = np.array([[[0,0],[17,0],[11,240],[0,240]]])
    cv2.fillPoly(default_grid,pts,(255,255,255))

    # Right limit
    cv2.rectangle(default_grid, (209,0), (240,240), (255,255,255), -1)

    # Lighting
    cv2.rectangle(default_grid, (188,160), (209,240), (255,255,255), -1)

default_grid = np.zeros((240,240,3), dtype=np.uint8)
if config.TABLE == 3:
    table3()

def generate_grid(visible_fuelcells):
    grid = default_grid.copy()
    for fuelcell in visible_fuelcells:
        if not fuelcell.target:
            cv2.circle(grid, fuelcell.map_coord_cm, 16, (255,255,255), -1)
    return grid

def plot_path(grid,path):
    for i in range(len(path)-1):
        cv2.line(grid, path[i], path[i+1],(0,255,0),1)
    return grid

class Node:
    """A node for A* Pathfinding algorithm
    """
    def __init__(self, position, cost, parent_id):
        self.position = position
        self.cost = cost
        self.parent_id = parent_id

def path_algorithm(grid, start, end):
    """Implementation of A* Pathfinding algorithm
    Adapted from:
    https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/AStar/a_star.py
    Args:
        grid (numpy.ndarray): numpy 2d array of obstacles map
        start (tuple): coordinate of start position
        end (tuple): coordinate of end position

    Returns:
        path (list of tuples): shortest path from start to end in the grid
    """
    table = grid[:,:,0]
    start_node = Node(start,0,-1)
    end_node = Node(end,0,-1)

    # dx,dy,cost
    motions = [[0,1,1],
              [1,0,1],
              [0,-1,1],
              [-1,0,1],
              [-1,-1,math.sqrt(2)],
              [-1,1,math.sqrt(2)],
              [1,-1,math.sqrt(2)],
              [1,1,math.sqrt(2)]]

    openset = dict()
    closedset = dict()

    openset[calc_index(start_node)] = start_node

    while True:
        if not openset:
            print("no path found")
            return None
        current_id = min(openset,
                   key=lambda x: openset[x].cost+calc_heuristic(openset[x],end_node))
        current_node = openset[current_id]

        if current_node.position == end_node.position:
            end_node.parent_id = current_node.parent_id
            end_node.cost = current_node.cost

            path = calc_final_path(end_node, closedset)
            return path

        # Remove from open set and add to closed set
        del openset[current_id]
        closedset[current_id] = current_node

        # expand search
        for motion in motions:
            new_node = Node((current_node.position[0]+motion[0], current_node.position[1]+motion[1]),
                        current_node.cost + motion[2], current_id)
            node_id = calc_index(new_node)

            if node_id in closedset:
                continue

            if not verify_node(table, new_node):
                continue

            if node_id not in openset:
                openset[node_id] = new_node
            else:
                if openset[node_id].cost >= new_node.cost:
                    openset[node_id] = new_node

def calc_index(node):
    return (node.position[1])*240 + node.position[0]

def calc_heuristic(current_node, end_node):
    return math.sqrt((current_node.position[0] - end_node.position[0])**2 +
                     (current_node.position[1] - end_node.position[1])**2)

def verify_node(table, node):
    # Check within table range and not obstacle
    conditions = (node.position[0] < 0 or node.position[0] >= len(table)
                  or node.position[1] < 0 or node.position[1] >= len(table)
                  or table[node.position[1]][node.position[0]])

    if conditions:
        return False
    else:
        return True

def calc_final_path(end_node, closedset):
    path = [end_node.position]
    parent_id = end_node.parent_id

    while parent_id != -1:
        node = closedset[parent_id]
        path.append(node.position)
        parent_id = node.parent_id

    return path

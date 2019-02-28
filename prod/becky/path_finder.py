import numpy as np
import cv2
from config import current_config as config

def table3():
    # Left limit
    pts = np.array([[[0,0],[104,0],[70,1472],[0,1472]]])
    cv2.fillPoly(default_grid,pts,(255,255,255))

    # Right limit
    cv2.rectangle(default_grid, (1283,0), (1472,1472), (255,255,255), -1)

    # Lighting
    cv2.rectangle(default_grid, (1154,984), (1282,1472), (255,255,255), -1)

default_grid = np.zeros(config.FRAME_POST_PROCESS_SHAPE+(3,), dtype=np.uint8)
if config.TABLE == 3:
    table3()

def generate_grid(visible_fuelcells):
    grid = default_grid.copy()
    for fuelcell in visible_fuelcells:
        if not fuelcell.target:
            cv2.circle(grid, fuelcell.coord, 101, (255,255,255), -1)
    return grid

def plot_path(grid,path):
    for i in range(len(path)-1):
        cv2.line(grid, path[i], path[i+1],(0,255,0),3)
    return grid

class Node:
    """A node for A* Pathfinding algorithm
    """
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.f = 0      # Total cost of node
        self.g = 0      # Distance from start node
        self.h = 0      # Heuristic - estimated distance to end node

    def __eq__(self, other):
        return self.position == other.position

def path_algorithm(grid, start, end):
    """Implementation of A* Pathfinding algorithm
    Adapted from:
    https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    Args:
        grid (numpy.ndarray): numpy 2d array of obstacles map
        start (tuple): coordinate of start position
        end (tuple): coordinate of end position

    Returns:
        path (list of tuples): shortest path from start to end in the grid
    """
    grid = grid[:,:,0]
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found end point
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # Generate children
        children = []
        adj_points = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for new_position in adj_points: # Adjacent squares
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            # Check if node is in table range
            range_cond = (node_position[0] > (len(grid) - 1)
                          or node_position[0] < 0
                          or node_position[1] > (len(grid[0]) -1)
                          or node_position[1] < 0)
            if range_cond:
                continue

            # Check if node is obstacle
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node and add to current node's list of children
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            # Child is already in closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Calculate f,g,h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0])**2
                       + (child.position[1] - end_node.position[1])**2)
            child.f = child.g + child.h

            # Child is already in open list
            # -> ignore if new g is higher than existing g
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)

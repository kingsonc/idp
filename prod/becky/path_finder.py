import math
import multiprocessing
from multiprocessing import Queue
import time

import cv2
import numpy as np

from config import current_config as config

class Node:
    """A node for A* Pathfinding algorithm
    """
    def __init__(self, position, cost, parent_id):
        self.position = position
        self.cost = cost
        self.parent_id = parent_id

class PathFinder:
    def __init__(self):
        self._default_grid = np.zeros((240,240,3), dtype=np.uint8)

        self.visible_fuelcells_q = multiprocessing.Queue(1)
        self.robot_coords_q = multiprocessing.Queue(1)
        self.target_coords_q = multiprocessing.Queue(1)
        self.path_q = multiprocessing.Queue(1)

        # Create table boundaries
        if config.TABLE == 3:
            self._table3()

        self.process = multiprocessing.Process(target=self.path_algorithm, daemon=True)

    def _table3(self):
        # Left limit
        pts = np.array([[[0,0],[17,0],[11,240],[0,240]]])
        cv2.fillPoly(self._default_grid,pts,(255,255,255))

        # Right limit
        cv2.rectangle(self._default_grid, (209,0), (240,240), (255,255,255), -1)

        # Lighting
        cv2.rectangle(self._default_grid, (188,160), (209,240), (255,255,255), -1)

    def _generate_grid(self, visible_fuelcells):
        """Generates pathing obstacles based on position of fuelcells.
        Avoids 16cm radius zone from each fuelcell.
        """
        grid = self._default_grid.copy()
        if visible_fuelcells:
            for fuelcell in visible_fuelcells:
                if not fuelcell.target:
                    cv2.circle(grid, fuelcell.map_coord_cm, 16, (255,255,255), -1)
        return grid

    def path_algorithm(self):
        """Implementation of A* Pathfinding algorithm
        Adapted from:
        https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/AStar/a_star.py
        """
        # dx,dy,cost
        motions = [[0,1,1],
                  [1,0,1],
                  [0,-1,1],
                  [-1,0,1],
                  [-1,-1,math.sqrt(2)],
                  [-1,1,math.sqrt(2)],
                  [1,-1,math.sqrt(2)],
                  [1,1,math.sqrt(2)]]

        print("1")
        while True:
            # with self.variables_lock:
            # visible_fuelcells = self.visible_fuelcells_q.get()
            # start = self.robot_coords_q.get()
            # end = self.target_coords_q.get()
            visible_fuelcells = []
            start = (150,17)
            end = (120,140)

            # If start or end positions do not exist, continue
            if not start or not end:
                time.sleep(0.01)
                continue

            # Generate map based on current fuelcell positions
            table = self._generate_grid(visible_fuelcells)[:,:,0]
            start_node = Node(start,0,-1)
            end_node = Node(end,0,-1)

            openset = dict()
            closedset = dict()

            openset[self._calc_index(start_node)] = start_node

            while True:
                # If openset is empty -> no possible path
                if not openset:
                    print("no path found")
                    break

                # Find next best node to search according to minumum cost
                current_id = min(openset,
                           key=lambda x: openset[x].cost+self._calc_heuristic(openset[x],end_node))
                current_node = openset[current_id]

                # Found end position
                if current_node.position == end_node.position:
                    end_node.parent_id = current_node.parent_id
                    end_node.cost = current_node.cost

                    self.path_q.put(self._calc_final_path(end_node, closedset))
                    break

                # Remove searched node from open set and add to closed set
                del openset[current_id]
                closedset[current_id] = current_node

                # expand search, put neighbouring nodes into open set
                for motion in motions:
                    new_node = Node((current_node.position[0]+motion[0], current_node.position[1]+motion[1]),
                                current_node.cost + motion[2], current_id)
                    node_id = self._calc_index(new_node)

                    # Skip if node already in closed set, ie already been searched
                    if node_id in closedset:
                        continue

                    # Skip if node is a wall or obstacle
                    if not self._verify_node(table, new_node):
                        continue

                    if node_id not in openset:
                        # Add node into open set
                        openset[node_id] = new_node
                    else:
                        # If node already in open set, check if new path to node is faster
                        if openset[node_id].cost >= new_node.cost:
                            openset[node_id] = new_node

    def _calc_index(self, node):
        """Generates unique index for each position
        """
        return (node.position[1])*240 + node.position[0]

    def _calc_heuristic(self, current_node, end_node):
        """Euclidean distance between node and end position
        """
        return math.sqrt((current_node.position[0] - end_node.position[0])**2 +
                         (current_node.position[1] - end_node.position[1])**2)

    def _verify_node(self, table, node):
        # Check within table range and not obstacle
        conditions = (node.position[0] < 0 or node.position[0] >= len(table)
                      or node.position[1] < 0 or node.position[1] >= len(table)
                      or table[node.position[1]][node.position[0]])

        if conditions:
            return False
        else:
            return True

    def _calc_final_path(self, end_node, closedset):
        """Generate final shortest path
        """
        path = [end_node.position]
        parent_id = end_node.parent_id

        # Recursively look through parent nodes
        while parent_id != -1:
            node = closedset[parent_id]
            path.append(node.position)
            parent_id = node.parent_id

        return path

def plot_path(plot,path, pos, target):
    """Plot path onto map
    """
    for i in range(len(path)-1):
        cv2.line(plot, (int(path[i][0]*92/15), int(path[i][1]*92/15)),
                 (int(path[i+1][0]*92/15), int(path[i+1][1]*92/15)),(0,255,0),3)

    cv2.circle(plot, (int(pos[0]*92/15), int(pos[1]*92/15)), 10, (255,255,0),-1)
    cv2.circle(plot, (int(target[0]*92/15), int(target[1]*92/15)), 10, (255,255,0),-1)
    return plot

from copy import deepcopy
import math
import threading
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
        self.visible_fuelcells = None
        self.robot_coords = None
        self.target_coords = None
        self.path = None

        if config.TABLE == 3:
            self._table3()

        self.thread = threading.Thread(target=self.path_algorithm, daemon=True)
        self.variables_lock = threading.Lock()
        self.path_lock = threading.Lock()
        self.thread.start()

    def _table3(self):
        # Left limit
        pts = np.array([[[0,0],[17,0],[11,240],[0,240]]])
        cv2.fillPoly(self._default_grid,pts,(255,255,255))

        # Right limit
        cv2.rectangle(self._default_grid, (209,0), (240,240), (255,255,255), -1)

        # Lighting
        cv2.rectangle(self._default_grid, (188,160), (209,240), (255,255,255), -1)

    def _generate_grid(self, visible_fuelcells):
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
        Args:
            grid (numpy.ndarray): numpy 2d array of obstacles map
            start (tuple): coordinate of start position
            end (tuple): coordinate of end position

        Returns:
            path (list of tuples): shortest path from start to end in the grid
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

        while True:
            with self.variables_lock:
                visible_fuelcells = self.visible_fuelcells
                start = self.robot_coords
                end = self.target_coords

            if not start or not end:
                time.sleep(0.1)
                continue

            table = self._generate_grid(visible_fuelcells)[:,:,0]
            start_node = Node(start,0,-1)
            end_node = Node(end,0,-1)

            openset = dict()
            closedset = dict()

            openset[self._calc_index(start_node)] = start_node

            while True:
                if not openset:
                    print("no path found")
                    with self.path_lock:
                        self.path = None
                    break
                current_id = min(openset,
                           key=lambda x: openset[x].cost+self._calc_heuristic(openset[x],end_node))
                current_node = openset[current_id]

                if current_node.position == end_node.position:
                    end_node.parent_id = current_node.parent_id
                    end_node.cost = current_node.cost

                    with self.path_lock:
                        self.path = self._calc_final_path(end_node, closedset)
                    break

                # Remove from open set and add to closed set
                del openset[current_id]
                closedset[current_id] = current_node

                # expand search
                for motion in motions:
                    new_node = Node((current_node.position[0]+motion[0], current_node.position[1]+motion[1]),
                                current_node.cost + motion[2], current_id)
                    node_id = self._calc_index(new_node)

                    if node_id in closedset:
                        continue

                    if not self._verify_node(table, new_node):
                        continue

                    if node_id not in openset:
                        openset[node_id] = new_node
                    else:
                        if openset[node_id].cost >= new_node.cost:
                            openset[node_id] = new_node

    def _calc_index(self, node):
        return (node.position[1])*240 + node.position[0]

    def _calc_heuristic(self, current_node, end_node):
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
        path = [end_node.position]
        parent_id = end_node.parent_id

        while parent_id != -1:
            node = closedset[parent_id]
            path.append(node.position)
            parent_id = node.parent_id

        return path

def plot_path(plot,path):
    for i in range(len(path)-1):
        cv2.line(plot, (int(path[i][0]*92/15), int(path[i][1]*92/15)),
                 (int(path[i+1][0]*92/15), int(path[i+1][1]*92/15)),(0,255,0),3)
    return plot

from collections import OrderedDict
import numpy as np
from scipy.spatial import distance
import beqcuerella.vision as vision

class FuelCellsTracker:
    """Allows correlation of fuel cells between frames and persistance of state.
    Adapted from:
    https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
    """
    def __init__(self):
        self.nextFCID = 0
        self.fuelcells = OrderedDict()

    def register(self, coord):
        self.fuelcells[self.nextFCID] = FuelCell(self.nextFCID, coord)
        self.nextFCID += 1

    def update(self, new_coords):
        # Special condition when there are no tracked fuel cells yet
        if len(self.fuelcells) == 0:
            for i in range(len(new_coords)):
                self.register(new_coords[i])
        else:
            FCIDs = list(range(len(self.fuelcells)))
            prev_coords = [fc.coord for fc in self.fuelcells.values()]

            # Compute distance between each pair of existing and new coords
            # Shape: Rows->Existing coords; Cols-> New coords
            rel_dist = distance.cdist(prev_coords, new_coords)
            # Find smallest value in each row
            rows = rel_dist.min(axis=1).argsort()
            # Sort row indices based on minimum values
            cols = rel_dist.argmin(axis=1)[rows]

            checked_rows = set()
            checked_cols = set()

            # Loop over row,col combinations
            for (row, col) in zip(rows, cols):
                # Skip if already checked
                if row in checked_rows or col in checked_cols:
                    continue

                # Update fuel cell coords
                FCID = FCIDs[row]
                self.fuelcells[FCID].coord = new_coords[col]
                self.fuelcells[FCID].visible = True

                checked_rows.add(row)
                checked_cols.add(col)

            # Find unexamined rows and cols
            unused_rows = set(range(rel_dist.shape[0])).difference(checked_rows)
            unused_cols = set(range(rel_dist.shape[1])).difference(checked_cols)

            # No. of exisiting FCs >= No. of camera found FCs
            if rel_dist.shape[0] >= rel_dist.shape[1]:
                # Fuel cells that are no longer visible
                for row in unused_rows:
                    FCID = FCIDs[row]
                    self.fuelcells[FCID].visible = False
            else:
                for col in unused_cols:
                    self.register(new_coords[col])

        return self.fuelcells

class FuelCell:
    def __init__(self, FCID, coord):
        self.FCID = FCID
        self.map_coord_cm = None
        self.visible = True
        self.radioactive = True
        self.visited = False
        self.pickedUp = False

        self.coord = coord

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, coord):
        self._coord = coord
        self.map_coord_cm = vision.map_coord_to_cm(coord)

    # def init_coords(coord):

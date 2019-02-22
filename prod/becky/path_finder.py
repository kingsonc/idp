import numpy as np
from config import current_config as config

class MapGrid:
    def __init__(self, table_shape):
        self.grid = np.zeros(table_shape)


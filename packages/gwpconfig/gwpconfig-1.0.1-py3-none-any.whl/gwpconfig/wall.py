"""Module with wall measurements and method for creating grid of pins.
"""
import math
import numpy as np

# Wall size given in meters - (x, y).
WALL_SIZE = [4.1, 3.1]
# Pin raster - distances between pins in (x, y).
WALL_RASTER = [0.2, 0.25]
PIN_HEIGHT = 0.0


def create_grid(three_dim):
    """Calculate pins positions. Pins are placed in squared pattern.

    Args:
        threeDim (bool): If True, calculate pins positions in 3d space, otherwise in 2d space (without height dimension).

    Returns:
        numpy.ndarray: nx3 or nx2 array of pins positions, where n is number of pins and second number depends on wheter positions are calculated in 3d or 2d space.
    """
    number_of_pins_in_x = math.ceil(WALL_SIZE[0] / WALL_RASTER[0])
    number_of_pins_in_y = math.ceil(WALL_SIZE[1] / WALL_RASTER[1])

    x_grid = [x * WALL_RASTER[0] for x in range(int(number_of_pins_in_x))]
    y_grid = [y * WALL_RASTER[1] for y in range(int(number_of_pins_in_y))]

    pins = []
    for x in x_grid:
        for y in y_grid:
            if not three_dim:
                pins.append([x, y])
            else:
                pins.append([x, y, PIN_HEIGHT])

    return np.array(pins)

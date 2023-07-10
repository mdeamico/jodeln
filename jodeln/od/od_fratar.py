"""Biproportional Matrix Factoring (Fratar Factoring)"""
from copy import deepcopy
from enum import Enum

from od.od_matrix import ODMatrix, create_od_from_source

class ODAxis(Enum):
    """Axis in an ODMatrix. 
    
    Values are used to get the corresponding zone from an (O, D) dictionary key.
    For example: 
        ODMatrix.volume = {(8, 9) = 32.7}
        key = (8, 9)
        key[ODAxis.ORIGIN] = 8
        key[ODAxis.DESTINATION] = 9
    """
    ORIGIN = 0
    DESTINATION = 1

def fratar(od_seed: ODMatrix) -> ODMatrix:

    # Limit number of Fratar factoring iterations
    MAX_ITERATIONS = 10

    od_1 = create_od_from_source(od_seed, copy_volume=True, copy_targets=True)
    od_2 = create_od_from_source(od_seed, copy_volume=True, copy_targets=True)

    def fratar_iter(od: ODMatrix, axis: ODAxis):
        """Helper function to do row/col iterations.
        Row Iter: axis = ODAxis.ORIGIN = 0 
        Col Iter: axis = ODAxis.DESTINATION = 1
        """
        if axis is ODAxis.ORIGIN:
            targets = od.targets_o
            margin_sums = od.sums_o
        elif axis is ODAxis.DESTINATION:
            targets = od.targets_d
            margin_sums = od.sums_d
        else:
            raise Exception(f"Axis {axis} unknown Expected ODAxis.ORIGIN or ODAxis.DESTINATION.")

        for k, v in od.volume.items():
            zone = k[axis.value]
            if targets[zone] == -1:
                continue
            elif margin_sums[zone] == 0:
                od.volume[k] = 0
            else:    
                od.volume[k] = v * targets[zone] / margin_sums[zone]
        
        od.set_margin_sums()


    for _ in range(0, MAX_ITERATIONS):
        # Swap matrices to save results for both row & col iterations
        od_1, od_2 = od_2, od_1

        # Row Iteration
        fratar_iter(od_1, ODAxis.ORIGIN)

        # Col Iteration
        fratar_iter(od_2, ODAxis.DESTINATION)

    # Average last iterations
    od_3 = create_od_from_source(od_seed, copy_targets=True)

    for k in od_3.volume:
        od_3.volume[k] = (od_1.volume[k] + od_2.volume[k]) / 2.0

    od_3.set_margin_sums()

    return od_3
    

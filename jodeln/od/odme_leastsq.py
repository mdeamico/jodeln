"""OD Estimation using the least squares method."""
import numpy as np
from scipy.optimize import lsq_linear as scipy_lsq_linear

from od.od_matrix import ODMatrix, create_od_from_source
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from network.net import Network


def estimate_od(od_seed: ODMatrix, 
                net: 'Network', 
                select_link: dict,
                select_turn: dict,
                seed_od_weight: float):
    """
    Estimated OD matrix using least squares.

    Use scipy-optimize-lsq-linear:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.lsq_linear.html#scipy-optimize-lsq-linear
    """

    # Set of variables included in the "A" matrix.
    var_set = set()

    for _, zone_pairs in select_link.items():
        for zone_pair_key in zone_pairs:
            var_set.add(zone_pair_key)

    for _, zone_pairs in select_turn.items():
        for zone_pair_key in zone_pairs:
            var_set.add(zone_pair_key)

    n_seed_od_var = 0
    for zone_pair_key, seed_volume in od_seed.volume.items():
        if zone_pair_key in var_set: 
            n_seed_od_var += 1
            continue
        if seed_volume == 0:
            continue
        var_set.add(zone_pair_key)
        n_seed_od_var += 1

    var_indices = {}
    var_counter = {}

    for i, k in enumerate(var_set):
        # print(f"[{k}] == {i}")
        var_indices[k] = i
        var_counter[k] = 0

    n_equations = len(select_link) + len(select_turn) + n_seed_od_var
    n_variables = len(var_set)

    A = np.zeros(shape=(n_equations, n_variables))
    B = np.zeros(shape=A.shape[0])
    # Weights
    W = [1] * A.shape[0]
    

    # -------------------
    # Create Equations 
    # -------------------
    eq_row = 0

    # Link Equations
    for link_key, zone_pairs in select_link.items():
        # A matrix coeff
        for zone_pair_key, route_ratio in zone_pairs.items(): 
            var_col = var_indices[zone_pair_key]
            A[eq_row, var_col] += route_ratio
            var_counter[zone_pair_key] += 1
        
        # B matrix targets
        B[eq_row] = net.link(*link_key).target_volume
        eq_row += 1
    
    # Turn Equations
    for turn_key, zone_pairs in select_turn.items():
        # A matrix coeff
        for zone_pair_key, route_ratio in zone_pairs.items(): 
            var_col = var_indices[zone_pair_key]
            A[eq_row, var_col] += route_ratio
            var_counter[zone_pair_key] += 1
        
        # B matrix targets
        B[eq_row] = net.turn(*turn_key).target_volume
        eq_row += 1     

    # Seed Equations
    for zone_pair_key, seed_volume in od_seed.volume.items():
        if zone_pair_key not in var_set: continue
        var_col = var_indices[zone_pair_key]
        A[eq_row, var_col] = 1
        B[eq_row] = seed_volume
        W[eq_row] = seed_od_weight * (var_counter[zone_pair_key] / (1.0 - seed_od_weight))
        eq_row += 1

    # Lower and upper bounds on OD volumes.
    lbounds = [0] * A.shape[1]
    ubounds = [np.inf] * A.shape[1]
    
    # print(A)
    # print(B)
    # print(W)

    # Convert weights to a diagonal matrix for lsq_linear solver
    W = np.diag(W)

    # ----------------------------
    # Run Least Squares Solver
    # ----------------------------
    # TODO: expose 'tol' as a user input?
    result = scipy_lsq_linear(np.dot(W, A), np.dot(W, B), bounds=(lbounds, ubounds), 
                              method='bvls', tol=1e-20)
    
    # print(result)
    # for k, v in var_indices.items():
    #     print(f"{k}: {result.x[v]}")
    
    od_estimated = create_od_from_source(source_od=od_seed, copy_targets=True)

    for zone_pair_key, v in var_indices.items():
        od_estimated.volume[zone_pair_key] = result.x[v]
    
    od_estimated.set_margin_sums()

    return result, od_estimated

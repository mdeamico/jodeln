import cma

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..network.net import Network
    from .od_matrix import ODMatrix

def objective_fn_prep_net_geh(net: 'Network'):
    """ Prepare optimization objective function by estimating maximum network GEH.

    Warning: this function mutates net by directly assigning link and turn volumes.
    TODO: after calling this function, reset net to its state before calling this funciton.
    
    Parameters
    ----------
    net : Network
        Network containing OD link and turn target volumes. 

    Returns
    -------
    float
        Estimated maximum sum of all differences between the seed and estimated OD.
    """
    # Each volume is scaled by the mulitplier to simulate a worst-case estimation.
    multipler = 5

    for link in net.links():
        link.assigned_volume = link.seed_volume * multipler
    
    for t in net.turns():
        t.assigned_volume = t.seed_volume * multipler

    net.calc_network_geh()
    return net.total_geh   



def objective_fn_prep_odsse(net: 'Network', od_seed: 'ODMatrix'):
    """Estimate maximum sum of sq error between seed and final od.

    Parameters
    ----------
    net : Network
        Network containing OD seed volumes.
    od_seed : ODMatrix
        Seed OD Matrix.

    Returns
    -------
    float
        Estimated maximum sum of all differences between the seed and estimated OD.
    """
    multiplier = 5
    odsse = 0
    for od in net.od_pairs:
        for route in od.routes:
            route_vol = od_seed.volume[(od.origin, od.destination)] * route.target_ratio * multiplier
            odsse += (route_vol - route.seed_volume) * (route_vol - route.seed_volume)

    return odsse



def objective_fn_prep_route_ratios(net: 'Network'):
    """Estimate maximum sum of route ratio differences.

    Parameters
    ----------
    net : Network
        Network containing multiple routes per OD. (Also works with one route per OD,
        but technically the route ratios do not need to be involved if all ODs have
        a single route.)

    Returns
    -------
    float
        Estimated maximum sum of all differences between assigned and target route ratios.
    """

    total_sum = 0

    for od in net.od_pairs:
        target_ratios = [route.target_ratio for route in od.routes]
        tgt_rel_diffs = [route.target_rel_diff for route in od.routes]

        # estimate worst-case route ratios
        # est_ratios is a sorted list of list: 
        # [[target ratio, index in target_ratio], [], ... ]
        est_ratios = sorted([[v, i] for i, v in enumerate(target_ratios)])

        # initialize worst-case route ratio to 0.01 for all targets
        for e in est_ratios:
            e.append(0.01)

        # smallest target_ratio should have highest worst case ratio
        est_ratios[0][-1] = 1 - (len(target_ratios) - 1) * 0.01

        # calculate worst-case relative differences
        est_rel_diffs = [(e[1], e[2] - (1 - e[2])) for e in est_ratios]

        diff_from_tgt = [e[1] - tgt_rel_diffs[e[0]] for e in est_rel_diffs]
        
        sum_sq_diff = sum([d * d for d in diff_from_tgt])

        total_sum += sum_sq_diff

    return total_sum



def estimate_od(
        net: 'Network', 
        od_seed: 'ODMatrix', 
        od_estimated: 'ODMatrix', 
        weight_total_geh=None, 
        weight_odsse=None, 
        weight_route_ratio=None) -> list[float]:
    """Estimate an OD matrix based on a seed matrix and target volumes within 
    the network links/turns. 
    
    Estimated matrix is directly saved in the 'od_estimated' variable.

    Uses a cma-es optimization algorithm to iteratively manipulate the seed matrix
    until the target volumes are met.

    Parameters
    ----------
    net : Network
    od_seed : ODMatrix
        OD matrix to use as an initial seed in the optimization process.
    od_estimated : ODMatrix
        Resulting estimated OD. This variable is mutated directly by the 
        optimization process.
    weight_total_geh : float, optional
        Objective function weight of the sum of all GEH values in the network.
    weight_odsse : float, optional
        Objective function weight for the influence of the seed matrix. Higher
        weight means the estimated matrix should have values close to the
        seed matrix, even if that means sacrificing link and turn GEH.
    weight_route_ratio : float, optional
        Objective function weight of the OD route ratios.

    Returns
    -------
    List[float]
        Result from cma-es objective function variables.
    """

    # Assign default objective function weights. Default weights lower importance of odsse.
    weight_total_geh = weight_total_geh or 1.0
    weight_odsse = weight_odsse or 0.10
    weight_route_ratio = weight_route_ratio or 1.0

    # Associate each route with a variable in the cma-es optimizer 
    p_counter = 0
    for od in net.od_pairs:
        for route in od.routes:
            route.opt_var_index = p_counter
            p_counter += 1

    net.init_seed_volumes(od_seed)

    estimated_max_net_geh = objective_fn_prep_net_geh(net)
    if estimated_max_net_geh <= 0:
        estimated_max_net_geh = 1
    
    estimated_max_odsse = objective_fn_prep_odsse(net, od_seed) 
    if estimated_max_odsse <= 0:
        estimated_max_odsse = 1

    estimated_max_ratio_sse = objective_fn_prep_route_ratios(net)
    if estimated_max_ratio_sse <= 0:
        estimated_max_ratio_sse = 1

    def objective_fn(x):
        """Objective function for the cma-es optimization algorithm.

        Parameters
        ----------
        x : List[float]
            Contains variables to optimize.

        Returns
        -------
        float
            Value to minimize.
        """

        odsse = 0
        ratio_sse = 0

        # calculate route volume based on estimated x values.
        for od in net.od_pairs:
            od_seed_total_vol = od_seed.volume[(od.origin, od.destination)]
            od_est_total_vol = 0
            for route in od.routes:
                # mulitplier m = x * x to ensure m is positive
                m = x[route.opt_var_index] * x[route.opt_var_index]
                est_route_vol = od_seed_total_vol * route.target_ratio * m
                odsse += (est_route_vol - route.seed_volume) * (est_route_vol - route.seed_volume)
                route.assigned_volume = est_route_vol
                od_est_total_vol += est_route_vol
            
            od_estimated.volume[(od.origin, od.destination)] = od_est_total_vol
            
            # update route ratios
            for route in od.routes:
                if od_est_total_vol > 0:
                    route.assigned_ratio = route.assigned_volume / od_est_total_vol
                else:
                    route.assigned_ratio = 1
                
                est_rel_diff = route.assigned_ratio - (1 - route.assigned_ratio)
                ratio_diff = est_rel_diff - route.target_rel_diff
                ratio_sqdiff = ratio_diff * ratio_diff
                ratio_sse += ratio_sqdiff

        net.set_link_and_turn_volume_from_route()
        net.calc_network_geh() 

        res = (weight_total_geh * (net.total_geh / estimated_max_net_geh) 
               + weight_odsse * (odsse / estimated_max_odsse)
               + weight_route_ratio * (ratio_sse / estimated_max_ratio_sse))

        return res

    # Run optimization algorithm
    res = cma.fmin(objective_fn, [1] * p_counter, 1, {'verbose':-9})

    # apply result
    objective_fn(res[0])

    return res[0]


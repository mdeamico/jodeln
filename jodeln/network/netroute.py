from dataclasses import dataclass

@dataclass
class NetRoute():
    """Contains sequence of nodes from origin to destination.

    Attributes
    ----------
    nodes : List[int]
        Ordered sequence of node IDs along the route, from origin to destination.
    name : str
        Human-readable name for the route. Does not have to be unique amongst all routes.
    seed_volume : float
        Volume on the route assigned from the seed OD matrix.
    target_ratio : float
        If one OD pair has multiple routes, this is the desired proportion of the 
        total OD volume that should occur on this route.
    target_rel_diff : float
        If one OD pair has multiple routes, this is a helper variable for the OD
        optimization that indicates how different this route is relative to all 
        other routes within the OD. For example, 2 routes, one has a target_ratio 
        of 0.8, the other 0.20. The target relative differences are 0.60 and -0.60, 
        respectively.
    assigned_volume : float
        Volume assigned to this route based on the estimated OD matrix.
    assigned_ratio : float
        If one OD pair has multiple routes, this is the actual proportion of the 
        total estimated OD volume. assigned_ratio is compared to the target_ratio
        in the OD optimization.
    opt_var_index : int
        Helper variable for the OD optimization algorithm. The OD optimization
        takes a list of variables. opt_var_index is the position of this route 
        within the list of optimization variables.
    """
    __slots__ = ['nodes', 'name', 'seed_volume', 'target_ratio', 'target_rel_diff',
                 'assigned_volume', 'assigned_ratio', 'opt_var_index']
    nodes: list[int]
    name: str
    seed_volume: float
    target_ratio: float
    target_rel_diff: float
    assigned_volume: float
    assigned_ratio: float
    opt_var_index: int

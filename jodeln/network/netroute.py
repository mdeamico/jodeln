from dataclasses import dataclass

@dataclass(slots=True)
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
    nodes: list[int]
    name: str
    seed_volume: float = 0
    target_ratio: float = 1
    target_rel_diff: float = 1
    assigned_volume: float = 0
    assigned_ratio: float = 1
    opt_var_index: int = -1

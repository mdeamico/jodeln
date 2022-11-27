from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .netroute import NetRoute

@dataclass
class NetODpair():
    """Origin-Destination data in the Network. 
    
    Attributes
    ----------
    origin : int
        node ID of the OD origin.
    destination : int
        node ID of the OD destination.
    seed_total_volume : float
        Volume for this OD pair within the seed OD matrix.
    est_total_volume : float
        Volume for this OD pair within the estimated OD matrix.
    routes : List[route]
        List of all possible routes from origin to destination to include in the
        OD optimization. One OD can contain multiple routes.
    """
    __slots__ = ['origin', 'destination', 'seed_total_volume', 'est_total_volume', 'routes']
    origin: int
    destination: int
    seed_total_volume: float
    est_total_volume: float
    routes: list['NetRoute']
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .netroute import NetRoute

@dataclass(slots=True)
class NetODpair():
    """Origin-Destination data in the Network. 
    
    Attributes
    ----------
    origin : int
        node ID of the OD origin.
    destination : int
        node ID of the OD destination.
    routes : list[NetRoute]
        List of all possible routes from origin to destination. One OD can 
        contain multiple routes.
    """
    origin: int
    destination: int
    routes: list['NetRoute']
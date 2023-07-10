from copy import deepcopy

class ODMatrix:
    """OD Matrix data structure.

    Attributes
    ----------
    volume: dict[tuple[int, int], float]
        OD volume for zone pair
    origins: list[int]
        List of origin nodes
    destination: list[int]
        List of destination nodes
    names_o: list[str]
        Origin zone names
    names_d: list[str]
        Destination zone names
    targets_o: dict[int, float]
        Origin zone total target volumes
    targets_d: dict[int, float]
        Destination zone total target volumes
    sums_o: dict[int, float]
        Origin zone total volume
    sums_d: dict[int, float]
        Destination zone total volume
    """
    __slots__ = ('volume', 'origins', 'destinations', 'names_o', 'names_d', 
                 'targets_o', 'targets_d', 'sums_o', 'sums_d')

    def __init__(self, volume, origins, destinations, names_o, names_d, targets_o, targets_d) -> None:
        self.volume: dict[tuple[int, int], float] = volume
        self.origins: list[int] = origins
        self.destinations: list[int] = destinations
        self.names_o: list[str] = names_o
        self.names_d: list[str] = names_d
        self.targets_o: dict[int, float] = targets_o
        self.targets_d: dict[int, float] = targets_d

        self.sums_o: dict[int, float] = dict.fromkeys(self.origins, 0)
        self.sums_d: dict[int, float] = dict.fromkeys(self.destinations, 0)
        self.set_margin_sums()

    def set_margin_sums(self):
        for k in self.sums_o:
            self.sums_o[k] = 0
        
        for k in self.sums_d:
            self.sums_d[k] = 0

        for (o, d), v in self.volume.items():
            self.sums_o[o] += v
            self.sums_d[d] += v

def create_od_from_source(
        source_od: ODMatrix,
        copy_volume: bool = False,
        copy_targets: bool = False
        ) -> ODMatrix:
    """Create an OD matrix based on the input source matrix.
    
    If the copy parameters are False, then the new OD matrix is filled with zeros.
    """
    if copy_volume:
        new_volume = deepcopy(source_od.volume)
    else:
        new_volume = dict.fromkeys(source_od.volume, 0)

    if copy_targets:
        new_targets_o = deepcopy(source_od.targets_o)
        new_targets_d = deepcopy(source_od.targets_d)
    else:
        new_targets_o = dict.fromkeys(source_od.targets_o, 0)
        new_targets_d = dict.fromkeys(source_od.targets_d, 0)

    return ODMatrix(
        volume=new_volume,
        origins=deepcopy(source_od.origins),
        destinations=deepcopy(source_od.destinations),
        names_o=deepcopy(source_od.names_o),
        names_d=deepcopy(source_od.names_d),
        targets_o=new_targets_o,
        targets_d=new_targets_d
    )  

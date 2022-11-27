from dataclasses import dataclass

@dataclass
class LinkParameters():
    """Parameters needed for constructing a NetLinkData object.
    """
    __slots__ = ['name', 'cost', 'target_volume', 'shape_points']
    name: str
    cost: float
    target_volume: float
    shape_points: list[tuple[float, float]]


@dataclass
class NetLinkData():
    """Data on Network links.

    Attributes
    ----------
    cost: float
        Friction on the link that is used when determining shortest routes.
    name: str
        Human-readable name for the link. Does not have to be unique.
    target_volume: float
        Desired volume on this link.
    link_index: int
        Unique identifier for this link.
    assigned_volume: float
        Volume on the link as assigned from the estimated OD matrix.
    geh: float
        GEH statistic comparing the target_volume and assigned_volume.
    seed_volume: float
        Volume on the link as assigned from the seed OD matrix.
    """
    __slots__ = ['cost', 'name', 'target_volume', 'link_index', 'assigned_volume', 
                 'geh', 'seed_volume', 'shape_points']
    cost: float
    name: str
    target_volume: float
    link_index: int
    assigned_volume: float
    geh: float
    seed_volume: float
    shape_points: list[tuple[float, float]]

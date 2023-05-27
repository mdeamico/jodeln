from dataclasses import dataclass

@dataclass(slots=True)
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
    key: tuple[int, int]
        Unique identifier for this link. Defaults to an invalid (-1, -1). 
        Create a valid value when adding the link to the network based on the 
        node keys: upstream i, downstream j.
    assigned_volume: float
        Volume on the link as assigned from the estimated OD matrix.
    geh: float
        GEH statistic comparing the target_volume and assigned_volume.
    seed_volume: float
        Volume on the link as assigned from the seed OD matrix.
    """
    cost: float
    name: str
    target_volume: float
    shape_points: list[tuple[float, float]]
    key: tuple[int, int] = (-1, -1)
    assigned_volume: float = 0
    seed_volume: float = 0
    geh: float = 0

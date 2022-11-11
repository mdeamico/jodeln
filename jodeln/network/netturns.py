from dataclasses import dataclass

@dataclass
class TurnData():
    """Data on Network turns.
    
    A turn is a sequence of three consecutive nodes: A-B-C. In this case "B"
    is the intersection, A is upstream, and C is downstream.

    Attributes
    ----------
    key: tuple[int, int, int]
        Unique ID for the turn composed of the upstream, self, and downstream node keys.
    name: str
        Human-readable name for the turn. Typically based on the A-B-C node names.
    seed_volume: float
        Volume on the turn as assigned from the seed OD matrix.
    target_volume: float
        Desired volume on this turn.
    assigned_volume: float
        Volume on the turn as assigned from the estimated OD matrix.
    geh: float
        GEH statistic comparing the target_volume and assigned_volume.
    """
    __slots__ = ['key', 'name', 'seed_volume', 'target_volume', 'assigned_volume', 'geh']
    key: tuple[int, int, int]
    name: str
    seed_volume: float
    target_volume: float
    assigned_volume: float
    geh: float
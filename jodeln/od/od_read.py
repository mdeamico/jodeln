"""Import OD volumes.
"""

import csv
from collections import OrderedDict

from typing import TYPE_CHECKING

from od.od_matrix import ODMatrix

if TYPE_CHECKING:
    from ..network.net import Network

def od_from_csv(od_csv, net: 'Network') -> ODMatrix:
    """Creates an OD object from a csv OD matrix.
    
    csv is a square OD matrix (n rows = n columns), zones are ordered the same in the rows
    and columns. First column contains zone name.

    Example csv for four zones A, B, C, D.  D is not a destination, C is not an origin:

    A,0,100,250,0
    B,99,0,98,0
    C,0,0,0,0 
    D,10,12,12,0

    Parameters
    ----------
    od_csv : str
        File path to OD csv file.
    net : Network
        Network to assign the OD to.

    Returns
    -------
    Dict
        Keyed by a tuple of (origin name, destination name) with a value of 
        the OD volume.
    """
    

    # temp_od contains the data as-is from the csv, before final format
    # order of rows defines order of columns - matrix is assumed square
    # dictionary contains {zone: [volumes]}
    temp_od = OrderedDict()

    with open(od_csv, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            temp_od[row[0]] = row[1:]

    # convert OD zone names to Network node indices
    zones = list(temp_od.keys())
    zone_node_keys = [net.get_node_by_name(node_name)[0] for node_name in zones]

    # TODO: validate that OD matrix is applicable to Network.
    # i.e. zones in OD are found in Network

    # convert volume lists into a dictionary of {(o, d): volume}
    od: dict[tuple[int, int], float] = {}
    for o_name, volumes  in temp_od.items():
        o_node_key = net.get_node_by_name(o_name)[0]
        for i, v in enumerate(volumes):
            od[(o_node_key, zone_node_keys[i])] = float(v)

    origins = set()
    destinations = set()

    # Assumes matrix has square dimensions.
    for (o, d), v in od.items():
        origins.add(o)
        destinations.add(d)

    names_o = [net.node(o).name for o in origins]
    names_d = [net.node(d).name for d in destinations]

    # Targets set to zero. Actual targets are obtained from a separate input file.
    targets_o = dict.fromkeys(origins, 0)
    targets_d = dict.fromkeys(destinations, 0)

    od_matrix = ODMatrix(
        volume=od,
        origins=list(origins),
        destinations=list(destinations),
        names_o=names_o,
        names_d=names_d,
        targets_o=targets_o,
        targets_d=targets_d
    )

    return od_matrix


def import_zone_targets(zone_targets_csv, od_matrix: ODMatrix) -> None:
    """Import zone total target volumes for origin/destinations into the ODMatrix."""
    with open(zone_targets_csv, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            node_name, zone_type, target_volume = row
            target_volume = float(target_volume)
            
            if zone_type == "o":
                od_zone_names = od_matrix.names_o
                od_targets = od_matrix.targets_o
                od_nodes = od_matrix.origins
            elif zone_type == "d":
                od_zone_names = od_matrix.names_d
                od_targets = od_matrix.targets_d
                od_nodes = od_matrix.destinations
            else:
                raise Exception(f"Unknown zone type: {zone_type}. Expected 'o' or 'd'.")
            
            zone_i = od_zone_names.index(node_name)
            zone_node = od_nodes[zone_i]
            od_targets[zone_node] = target_volume
            

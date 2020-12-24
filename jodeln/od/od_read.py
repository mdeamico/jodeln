"""Import OD volumes.
"""

import csv
from collections import OrderedDict

def od_from_csv(od_csv, net):
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
    od = {}
    for o_name, volumes  in temp_od.items():
        o_node_key = net.get_node_by_name(o_name)[0]
        for i, v in enumerate(volumes):
            od[(o_node_key, zone_node_keys[i])] = float(v)

    return od

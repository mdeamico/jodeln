"""
Create Network objects from various user inputs. 

Users may have varying available inputs when using this program.
For example:
    - node and link csv only.
    - node, link, and turn csv.
    - node, link, and OD csv,
Eventually formats other than csv might be accepted (such as shapefiles).

Was initially thinking of mplementing classmethods to overload __init__ in Graph
https://stackoverflow.com/questions/44765482/multiple-constructors-the-pythonic-way
but a separate Factory module (this file) seems more flexible.
"""

import csv
from .net import Network, NetRoute


def from_node_link_csv(node_csv, link_csv):
    """Create a network from csv files of nodes and links. 
    
    The Network turns and potential OD routes are also initialized so that the new
    network object returned is functional.

    Columns in node csv (columns must be in this order):

    1. node name
    2. x-coordinate
    3. y-coordinate
    4. is_origin (0 = False, 1 = True)
    5. is_destination (0 = False, 1 = True)

    Columns in link csv
    1. from_node
    2. to_node
    3. cost
    4. name
    5. target_volume

    Parameters
    ----------
    node_csv : str
        File path to node csv file.
    link_csv : str
        File path to link csv file.

    Returns
    -------
    Network
        New network containing input nodes and links.
    """
    # TODO: validate csv paths before continuing to create network graph

    net = Network()

    with open(node_csv, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for node_payload in reader:
            net.add_node(node_payload)

    with open(link_csv, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            i_name, j_name, *payload = row
            net.add_link(i_name, j_name, payload)

    net.init_turns()
    net.init_routes()

    return net


def import_turns(turn_csv, net: Network):
    """Import turn target volumes from csv.

    Turns are any portion of a route traversing 3 nodes, ex: A-B-C

    Columns in node csv (columns must be in this order):

    1. A node name
    2. B node name
    3. C node name
    4. turn name
    5. target volume

    Parameters
    ----------
    turn_csv : str
        File path to user gernerated turn csv file.
    net : Network
        Turns are imported into this network.
    """

    with open(turn_csv, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            i_name, j_name, k_name, *payload = row
            i, _ = net.get_node_by_name(i_name)
            j, _ = net.get_node_by_name(j_name)
            k, _ = net.get_node_by_name(k_name)
            turn_name = payload[0]
            turn_target = float(payload[1])

            if (i, j, k) not in net.turns:
                print(f'Cannot import turn {turn_name}. Turn not found in Network.')

            net.turns[(i, j, k)].name = turn_name
            net.turns[(i, j, k)].target_volume = turn_target


def import_routes(route_csv, net: Network):
    """Replace routes from O to D with user-defined routes.
    
    All routes between O and D must be contained in the csv. For example,
    if there is one existing route between O and D, and the user wants to add a 
    new second route, both the existing and new route must be contained in the csv.

    Columns in the route csv (columns must be in this order):
    
    1. origin: node name
    2. destination: node name
    3. target_ratio: how much volume should be on the route
                 (e.x. 0.20 means 20% of the total OD volume should be on this route)
    4. sequence: comma separated values of the node names from O to D

    Parameters
    ----------
    route_csv : str
        File path to user-defined OD route file.
    net : Network
        OD routes are imported into this network.
    """

    # keep track of which OD's are defined in the csv.
    user_od_set = set()

    with open(route_csv, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            o_name, d_name, user_ratio, *user_seq = row

            # convert node names to indices
            origin, _ = net.get_node_by_name(o_name)
            destination, _ = net.get_node_by_name(d_name)
            user_ratio = float(user_ratio)
            node_seq = [net.get_node_by_name(v)[0] for v in user_seq]

            for od in net.od:
                if not (od.origin == origin and od.destination == destination):
                    continue
                
                if (od.origin, od.destination) not in user_od_set:
                    # Delete all existing routes from O to D. Only delete once per OD.
                    od.routes = []
                    user_od_set.add((od.origin, od.destination))

                od.routes.append(
                    NetRoute(
                        nodes=node_seq,
                        name="",
                        seed_volume=0, 
                        target_ratio=user_ratio,
                        target_rel_diff=0, 
                        assigned_volume=0, 
                        assigned_ratio=0, 
                        opt_var_index=-1))

        # Normalize target_ratios
        for od in net.od:
            ratio_sum = 0
            for route in od.routes:
                ratio_sum += route.target_ratio
            
            if ratio_sum == 0:
                ratio_sum = 1
            
            for route in od.routes:
                route.target_ratio = route.target_ratio / ratio_sum
                route.target_rel_diff = route.target_ratio - (1 - route.target_ratio)
        
        # Update route names
        net.set_route_names()

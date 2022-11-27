"""
Create Network objects from various user inputs. 

Users may have varying available inputs when using this program.
For example:
    - node and link only.
    - node, link, and turn.
    - node, link, and OD
    - etc
"""

import csv
import os
from sys import maxsize as MAXSIZE

import shapefile

from .net import Network
from .netlink import LinkParameters
from .netnode import NetNode, NodeParameters
from .netroute import NetRoute


def create_network(node_file: str, link_file: str) -> Network:
    """Create a new network from user-supplied files.
    
    The network turns and potential OD routes are also initialized so that the new
    network object returned is functional.

    Parameters
    ----------
    node_file : str
        File path to node file.
    link_file : str
        File path to link file.

    Returns
    -------
    Network
        New network containing nodes and links. Turns and routes are initialized
        from the nodes and links.
    """
    
    node_handler = {
        '.csv': add_nodes_from_csv,
        '.shp': add_nodes_from_shp
    }

    link_handler = {
        '.csv': add_links_from_csv,
        '.shp': add_links_from_shp
    }

    node_file_ext = os.path.splitext(node_file)[1]
    link_file_ext = os.path.splitext(link_file)[1]

    if (node_file_ext not in node_handler.keys()) or (link_file_ext not in link_handler.keys()):
        return
    
    new_network = Network()

    node_handler[node_file_ext](new_network, node_file)
    link_handler[link_file_ext](new_network, link_file)

    new_network.init_turns()
    new_network.init_routes()
    new_network.set_coord_scale()

    return new_network


def add_nodes_from_csv(net: Network, node_csv: str) -> None:
    """Adds nodes to the network from the given csv file.

    Columns in node csv (columns must be in this order):

    1. node name
    2. x-coordinate
    3. y-coordinate
    4. is_origin (0 = False, 1 = True)
    5. is_destination (0 = False, 1 = True)

    Parameters
    ----------
    net : Network
        Network object where nodes will be added.
    node_csv : str
        File path to node file.
    """

    with open(node_csv, newline='') as file:
        reader = csv.reader(file)

        # skip header
        next(reader)

        for payload in reader:
            node_name = payload[0]
            
            try:
                node_x = float(payload[1])
            except ValueError:
                node_x = 0
            
            try:
                node_y = float(payload[2])
            except ValueError:
                node_y = 0
            
            node_is_origin = int(payload[3]) == 1
            node_is_destination = int(payload[4]) == 1

            node_parameters = NodeParameters(
                name=node_name,
                x=node_x,
                y=node_y,
                is_origin=node_is_origin,
                is_destination=node_is_destination
            )

            net.add_node(node_parameters) 


def add_links_from_csv(net: Network, link_csv: str) -> None:
    """Adds links to the network from the given csv file.
    
    Requires that the network already has nodes in it.
    
    Columns in link csv (columns must be in this order):

    1. from_node
    2. to_node
    3. cost
    4. name
    5. target_volume

    The csv file format does not allow defining intermediate shape points
    between the link start point and end point. Use shapefile format if 
    intermediate points are desired.

    Parameters
    ----------
    net : Network
        Network object where links will be added.
    link_csv : str
        File path to link file.
    """
    with open(link_csv, newline='') as file:
        reader = csv.reader(file)
        
        # skip header
        next(reader)
        
        for payload in reader:
            i_name = payload[0]
            j_name = payload[1]
            
            try:
                link_cost = float(payload[2])
            except ValueError:
                link_cost = 0
            
            try:
                link_target_volume = float(payload[4])
            except ValueError:
                link_target_volume = 0


            link_parameters = LinkParameters(
                name=payload[3],
                cost=link_cost,
                target_volume=link_target_volume,
                shape_points=[(net.get_node_by_name(i_name)[1].x, net.get_node_by_name(i_name)[1].y), 
                              (net.get_node_by_name(j_name)[1].x, net.get_node_by_name(j_name)[1].y)]
            )
            
            net.add_link(i_name, j_name, link_parameters)


def add_nodes_from_shp(net: Network, node_shp: str) -> None:
    """Adds nodes to the network from the given shapefile path.

    Parameters
    ----------
    net : Network
        Network object where nodes will be added.
    node_shp : str
        File path to node shapefile.
    """
    node_sf = shapefile.Reader(node_shp)

    for node_sr in node_sf.shapeRecords():
        node_parameters = NodeParameters(
            name=node_sr.record['name'],
            x=node_sr.shape.points[0][0],
            y=node_sr.shape.points[0][1],
            is_origin=int(node_sr.record['is_origin']) == 1,
            is_destination=int(node_sr.record['is_destina']) == 1
        )
        net.add_node(node_parameters)


def add_links_from_shp(net: Network, link_shp: str) -> None:
    """Adds links to the network from the given shapefile paths.
    
    Requires that the network already has nodes in it.

    Parameters
    ----------
    net : Network
        Network object where links will be added.
    link_shp : str
        File path to link shapefile.
    """
    link_sf = shapefile.Reader(link_shp)

    for link_sr in link_sf.shapeRecords():

        link_start_xy = link_sr.shape.points[0]
        link_end_xy = link_sr.shape.points[-1]

        start_pt = _find_closest_node(link_start_xy, net)
        end_pt = _find_closest_node(link_end_xy, net)
        
        i_name = start_pt.name
        j_name = end_pt.name
           
        try:
            link_cost = float(link_sr.record['cost'])
        except ValueError:
            link_cost = 0
            
        try:
            link_target_volume = float(link_sr.record['target_vol'])
        except ValueError:
            link_target_volume = 0

        link_parameters = LinkParameters(
            name=link_sr.record['name'],
            cost=link_cost,
            target_volume=link_target_volume,
            shape_points=link_sr.shape.points
        )
        
        net.add_link(i_name, j_name, link_parameters)

        # Add link in opposite direction (if two-way)
        if link_sr.record['oneway'] == 2:

            rev_pts = list(link_sr.shape.points)
            rev_pts.reverse()

            # TODO: opposite direction link needs a different name?
            link_parameters = LinkParameters(
                name=link_sr.record['name'],
                cost=link_cost,
                target_volume=link_target_volume,
                shape_points=rev_pts
            )

            net.add_link(j_name, i_name, link_parameters)


def import_turns(turn_csv, net: Network) -> None:
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

            if (i, j, k) not in net._turns:
                print(f'Cannot import turn {turn_name}. Turn not found in Network.')

            net._turns[(i, j, k)].name = turn_name
            net._turns[(i, j, k)].target_volume = turn_target


def import_routes(route_csv, net: Network) -> None:
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


def _find_closest_node(search_pt: tuple, net: Network) -> NetNode:
    """Given a search point, find the closest point within a group of points.
    
    Parameters
    ----------
    search_pt : tuple
        x, y coordinate of the search point
    net : Network
        Network that already has nodes loaded. search_pt will be compared against
        the nodes in this network.

    Returns
    -------
    closest_node
        NetNode object of closest point within the network. Returns None if nothing found.
    """
    x1 = search_pt[0]
    y1 = search_pt[1]
    
    min_dist = MAXSIZE
    closest_node = None

    for node in net.nodes():
        x2 = node.x
        y2 = node.y
        dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
        if dist < min_dist:
            min_dist = dist
            closest_node = node

    return closest_node
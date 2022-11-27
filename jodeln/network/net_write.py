"""Export network features to csv files.
"""

import os
import csv

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .net import Network

def export_turns(net: 'Network', output_folder=None) -> None:
    """Exports network turns to a csv file.

    Parameters
    ----------
    net : Network
        Network cotaining turns to export.
    output_folder : str, optional
        Folder to export turn file, by default None indicates the current working
        directory as returned by os.getcwd().
    """
    if len(net._turns) == 0:
        print("Network does not contain any turns.")
        return

    if output_folder is None:
        output_folder = os.getcwd()

    output_file = os.path.join(output_folder, 'exported_turns.csv')

    print('Output turns to: ', output_file)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["a_node", "b_node", "c_node"])

        for (i, j, k), _ in net.turns(True):
            A = net.node(i).name
            B = net.node(j).name
            C = net.node(k).name
            writer.writerow([A, B, C])



def export_node_sequences(net: 'Network', output_folder=None) -> None:
    """Export the links and turns on every OD route to csv.

    Parameters
    ----------
    net : Network
        Network containing the node sequences to export.
    output_folder : str
        Folder to export the node file, by default None indicates the current working
        directory as returned by os.getcwd().
    """
    if net.od is None:
        print("Network does not contain any OD.")
        return

    if output_folder is None:
        output_folder = os.getcwd()

    output_turn_seq_file = os.path.join(output_folder, 'exported_route_turn_seq.csv')
    output_link_seq_file = os.path.join(output_folder, 'exported_route_link_seq.csv')
    
    with open(output_turn_seq_file, 'w', newline='') as turn_f, \
         open(output_link_seq_file, 'w', newline='') as link_f:
        
        turn_writer = csv.writer(turn_f)
        link_writer = csv.writer(link_f)

        turn_writer.writerow(["o_node", "d_node", "route", "a_node", "b_node", "c_node"])
        link_writer.writerow(["o_node", "d_node", "route", "a_node", "b_node"])

        for od in net.od:
            o_name = net.node(od.origin).name
            d_name = net.node(od.destination).name

            for route in od.routes:
                n_route_nodes = len(route.nodes)
                
                if n_route_nodes <= 1:
                    # route is O == D
                    continue

                if n_route_nodes == 2:
                    # route is one link
                    a = net.node(route.nodes[0]).name
                    b = net.node(route.nodes[1]).name
                    link_writer.writerow([o_name, d_name, a, b])
                    continue

                # route has 3 or more nodes
                for x in range(0, len(route.nodes) - 2):
                    a = net.node(route.nodes[x]).name
                    b = net.node(route.nodes[x + 1]).name
                    c = net.node(route.nodes[x + 2]).name
                    turn_writer.writerow([o_name, d_name, route.name, a, b, c])
                    link_writer.writerow([o_name, d_name, route.name, a, b])

                # last link
                b = net.node(route.nodes[x + 1]).name
                c = net.node(route.nodes[x + 2]).name
                link_writer.writerow([o_name, d_name, route.name, b, c])

    

def export_route_list(net: 'Network', output_folder=None) -> None:
    """Export the nodes along each route. One row per route.

    Sample csv output. First two rows of the sample output are the same origin-destination, 
    but have different routes.
    --
    100,101,103,105
    100,110,112,105
    105,107,108,109
    --

    Parameters
    ----------
    net : Network
        Network containing the routes to export.
    output_folder : str, optional
        Folder to export route file, by default None indicates the current working
        directory as returned by os.getcwd().
    """
    
    if net.od is None:
        print("Network does not contain any OD.")
        return

    if output_folder is None:
        output_folder = os.getcwd()

    print('Output OD to: ', output_folder)
    
    output_list_file = os.path.join(output_folder, 'exported_nodes_on_routes.csv')
    with open(output_list_file, 'w', newline='') as list_f:
        
        list_writer = csv.writer(list_f)

        for od in net.od:
            for route in od.routes:
                list_writer.writerow([str(net.node(x).name) for x in route.nodes])


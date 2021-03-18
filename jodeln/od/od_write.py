"""Export OD volumes.
"""

from typing import TYPE_CHECKING
import os
import csv


if TYPE_CHECKING:
    from ..network.net import Network


def export_od_as_list(net: 'Network', output_folder=None):
    """Save the estimated OD to a csv file with one row per OD pair.
    
    csv columns are:

    1. origin name
    2. destination name
    3. estimated volume.

    Sample csv output
    --
    100,101,32.2
    100,102,67.6
    105,109,21.0
    --

    Parameters
    ----------
    net : Network
        Network containing OD to export.
    output_folder : str, optional
        Folder to export OD file, by default None indicates the current working
        directory as returned by os.getcwd().
    """
    
    if net.od is None:
        print("Network does not contain any OD.")
        return

    if output_folder is None:
        output_folder = os.getcwd()

    print('Output OD to: ', output_folder)
    
    output_list_file = os.path.join(output_folder, 'exported_od_(list format).csv')
    with open(output_list_file, 'w', newline='') as list_f:
        
        list_writer = csv.writer(list_f)
        list_writer.writerow(["o_node", "d_node", "volume"])

        for od in net.od:
            o_name = net.nodes[od.origin].name
            d_name = net.nodes[od.destination].name

            list_writer.writerow([o_name, d_name, od.est_total_volume])



def export_od_by_route(net: 'Network', output_folder=None):
    """Save the estimated OD to a csv file. One row per route.

    This export format allows showing the volume assigned to each route, if multiple 
    routes between the origin and destination exist.

    csv columns are: 

    1. origin
    2. destination
    3. route name
    4. estimated route volume

    Sample csv output. First two rows of the sample output are the same origin-destination, 
    but have different routes.

    --
    100,105,101_106,30.0
    100,105,102_107,15.0
    105,109,105_110,21.0
    --

    Parameters
    ----------
    net : Network
        Network containing OD to export.
    output_folder : str, optional
        Folder to export OD file, by default None indicates the current working
        directory as returned by os.getcwd().
    """
    
    if net.od is None:
        print("Network does not contain any OD.")
        return

    if output_folder is None:
        output_folder = os.getcwd()

    print('Output OD to: ', output_folder)
    
    output_list_file = os.path.join(output_folder, 'exported_route_volumes.csv')
    with open(output_list_file, 'w', newline='') as list_f:
        
        list_writer = csv.writer(list_f)
        list_writer.writerow(["o_node", "d_node", "route", "volume"])

        for od in net.od:
            o_name = net.nodes[od.origin].name
            d_name = net.nodes[od.destination].name
            for route in od.routes:
                list_writer.writerow([o_name, d_name, route.name, route.assigned_volume])
    

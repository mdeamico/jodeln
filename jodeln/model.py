"""Model component of the Model-View-Controller (MVC) design pattern for Jodeln.
"""

import os
from dataclasses import dataclass
from typing import List

from network import net_read
from network import net_write

from od import od_read
from od import od_write
from od import od_estimation as odme


@dataclass
class RouteInfo:
    """Basic OD information for a route."""
    origin: int
    destination: int
    o_name: str
    d_name: str
    name: str
    nodes: List


class Model():
    """Contains the network and od data, and methods to operate on them.
    
    These methods are the API for a view/controller to interact with the data.
    """
    __slots__ = ['net', 'od_seed']

    def __init__(self):
        """Initialize Model with an empty network and empty OD Seed Matrix.
        
        The Model variables are populated via the Model.load() function.
        """

        #: Network: Object containing network graph of nodes and links, as well 
        # as turns, volume targets, and OD info.
        self.net = None
        
        #: dict: Seed OD matrix loaded from csv.
        self.od_seed = None

    def load(self, node_file=None, links_file=None, od_seed_file=None, turns_file=None, od_routes_file=None):
        """Populate network and od variables with user supplied data.

        Parameters
        ----------
        node_file : str, optional
            File path to Network nodes, by default None.
        links_file : str, optional
            File path to Network links, by default None.
        od_seed_file : str , optional
            File path to seed matrix, by default None.
        turns_file : str, optional
            File path to turn targets, by default None.
        od_routes_file : str, optional
            File path to OD routes, by default None.

        Returns
        -------
        bool
            True if load was successful, otherwise False.
        """

        node_file = _clean_file_path(node_file)
        links_file = _clean_file_path(links_file)
        od_seed_file = _clean_file_path(od_seed_file)
        turns_file = _clean_file_path(turns_file)
        od_routes_file = _clean_file_path(od_routes_file)

        if self.net is None:
            if node_file is None or links_file is None:
                # TODO: This case should trigger an alert to the user that
                # their inputs are invalid.
                return False
            
            self.net = net_read.from_node_link_csv(node_file, links_file)
        
        if self.net is None:
            # can't continue loading OD or turns without a Network
            return False

        if od_seed_file is not None:
            self.od_seed = od_read.od_from_csv(od_seed_file, self.net)

        if turns_file is not None:
            net_read.import_turns(turns_file, self.net)

        if od_routes_file is not None:
            net_read.import_routes(od_routes_file, self.net)

        return True

    def estimate_od(self, weight_total_geh=None, weight_odsse=None, weight_route_ratio=None):
        """Estimate an OD matrix that attempts to meet various network volume targets.
        
        By default the ODME objective function weights are None. Passing None 
        allows odme.estimate_od function to set the default objective function weights.
        
        Parameters
        ----------
        weight_total_geh : float, optional
            Objective function weight of the sum of all GEH values in the network.
        weight_odsse : float, optional
            Objective function weight for the influence of the seed matrix. Higher
            weight means the estimated matrix should have values close to the
            seed matrix, even if that means sacrificing link and turn GEH.
        weight_route_ratio : float, optional
            Objective function weight of the OD route ratios.
            
        Returns
        -------
        List[float]
            List of the final values of the ODME objective function variables.
        """
        if self.od_seed is None or self.net is None:
            return

        res = odme.estimate_od(self.net, self.od_seed, weight_total_geh, weight_odsse, weight_route_ratio)
        return res

    def export_od(self, output_folder=None):
        """Write estimated OD to csv."""
        output_folder = _clean_folder_path(output_folder)
        od_write.export_od_as_list(self.net, output_folder)

    def export_turns(self, output_folder=None):
        """Write turns to csv."""
        output_folder = _clean_folder_path(output_folder)
        net_write.export_turns(self.net, output_folder)

    def export_od_by_route(self, output_folder=None):
        """Write estimated OD to csv, in list format, one row per OD pair."""
        output_folder = _clean_folder_path(output_folder)
        od_write.export_od_by_route(self.net, output_folder)

    def export_node_sequence(self, output_folder=None):
        """Write the links and turns on every OD route to csv."""
        output_folder = _clean_folder_path(output_folder)
        net_write.export_node_sequences(self.net, output_folder)

    def export_route_list(self, output_folder=None):
        """Export the nodes along each route. One row per route."""
        output_folder = _clean_folder_path(output_folder)
        net_write.export_route_list(self.net, output_folder)

    def get_node_xy(self):
        """Return xy coordinates for each node."""
        if not self.net:
            return
        
        return {i: (node.x, node.y, node.name) for i, node in self.net.nodes.items()}

    def get_link_end_ids(self):
        """Return node ids for the start and end of each link."""
        if not self.net:
            return
        
        return [(i, j) for i, j, _ in self.net.links()]

    def get_route_list(self):
        """Return basic OD information for each route."""
        routes = [] # type: List[RouteInfo]
        
        for od in self.net.od:
            o_name = self.net.nodes[od.origin].name
            d_name = self.net.nodes[od.destination].name

            for route in od.routes:
                basic_info = RouteInfo(od.origin, 
                                       od.destination, 
                                       o_name,
                                       d_name,
                                       route.name,
                                       route.nodes)

                routes.append(basic_info)

        return routes


def _clean_file_path(file_path):
    """Check if a file exists and return a valid path, else None."""
    if file_path is None:
        return None

    file_path = file_path.replace('"', '')
    if not os.path.isfile(file_path):
        return None

    return file_path


def _clean_folder_path(folder_path):
    """Check if a folder exists and return a valid path, else None."""
    if folder_path is None:
        return None

    folder_path = folder_path.replace('"', '')
    if not os.path.isdir(folder_path):
        return None

    return folder_path

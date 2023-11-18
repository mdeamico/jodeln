"""Model component of the Model-View-Controller (MVC) design pattern for Jodeln.
"""

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from network import net_read, net_write

from od import od_read, od_write, odme_fratar, odme_cmaes, odme_leastsq
from od.od_matrix import ODMatrix, create_od_from_source

if TYPE_CHECKING:
    from .network.netnode import NetNode
    from .network.netlink import NetLinkData
    from .network.net import Network

# Type Aliases
LinkKey = tuple[int, int]
TurnKey = tuple[int, int, int]
ZonePairKey = tuple[int, int]

@dataclass(slots=True)
class RouteInfo:
    """Basic OD information for a route."""
    origin: int
    destination: int
    o_name: str
    d_name: str
    name: str
    nodes: list


class Model():
    """Contains the network and od data, and methods to operate on them.
    
    These methods are the API for a view/controller to interact with the data.
    """
    __slots__ = ['net', 'od_seed', 'od_estimated', 'od_diff']

    def __init__(self):
        """Initialize Model with an empty network and empty OD Seed Matrix.
        
        The Model variables are populated via the Model.load() function.
        """

        #: Network: Object containing network graph of nodes and links, as well 
        # as turns, volume targets, and OD info.
        self.net: Network = None
        
        #: ODMatrix: Seed OD matrix loaded from csv.
        self.od_seed: ODMatrix = None

        #: ODMatrix: Estimated OD matrix
        self.od_estimated: ODMatrix = None

        #: ODMatrix: Difference matrix = od_estimated - od_seed
        self.od_diff: ODMatrix = None

    def load(self, 
             node_file=None, 
             links_file=None, 
             od_seed_file=None, 
             turns_file=None, 
             od_routes_file=None,
             zone_targets_file=None) -> bool:
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
        zone_targets_file : str, optional
            File path to OD zone targets, by default None.

        Returns
        -------
        bool
            True if load was successful, otherwise False.
        """
        self.reset()
        
        node_file = _clean_file_path(node_file)
        links_file = _clean_file_path(links_file)
        od_seed_file = _clean_file_path(od_seed_file)
        turns_file = _clean_file_path(turns_file)
        od_routes_file = _clean_file_path(od_routes_file)
        zone_targets_file = _clean_file_path(zone_targets_file)

        if self.net is None:
            if node_file is None or links_file is None:
                # TODO: This case should trigger an alert to the user that
                # their inputs are invalid.
                return False
            
            self.net = net_read.create_network(node_file, links_file)
        
        if self.net is None:
            # can't continue loading OD or turns without a Network
            return False

        if turns_file is not None:
            net_read.import_turns(turns_file, self.net)

        if od_routes_file is not None:
            net_read.import_routes(od_routes_file, self.net)

        if od_seed_file is not None:
            self.od_seed = od_read.od_from_csv(od_seed_file, self.net)
            self.init_od_seed_targets()
            
            self.od_estimated = create_od_from_source(self.od_seed, copy_targets=True)
            self.od_diff = create_od_from_source(self.od_seed, copy_targets=True)
            self.compute_od_diff()

        if zone_targets_file is not None:
            if self.od_seed is not None:
                od_read.import_zone_targets(zone_targets_file, self.od_seed)
                self.od_estimated.targets_o = self.od_seed.targets_o
                self.od_estimated.targets_d = self.od_seed.targets_d

        return True

    def reset(self):
        """Reset network and OD to empty state."""
        self.net = None
        self.od_seed = None
        self.od_estimated = None
        self.od_diff = None

    def has_od(self) -> bool:
        return self.od_seed is not None

    def init_od_seed_targets(self):
        """Init zone targets based on incoming/outgoing link targets."""

        # ----------------------------------------------------
        # Check link targets.
        # ----------------------------------------------------
        # If link_target == -1, then check turn targets.
        # Lists of flagged zones to check for turn targets.
        check_origin_turns = []
        check_destination_turns = []

        # Origin Link Targets
        for i in self.od_seed.origins:
            self.od_seed.targets_o[i] = 0
            for j in self.net.node(i).neighbors:
                link = self.net.link(i, j)
                if link.target_volume > 0:
                    self.od_seed.targets_o[i] += link.target_volume
                else:
                    check_origin_turns.append(i)

        # Destination Link Targets
        for j in self.od_seed.destinations:
            self.od_seed.targets_d[j] = 0
            for i in self.net.node(j).up_neighbors:
                link = self.net.link(i, j)
                if link.target_volume > 0:
                    self.od_seed.targets_d[j] += link.target_volume
                else:
                    check_destination_turns.append(j)

        # ---------------------------------------------------------
        # Check turn targets at flagged origins and destinations.
        # ---------------------------------------------------------
        # Origin Turn Targets
        for i in check_origin_turns:
            self.od_seed.targets_o[i] = 0
            for j in self.net.node(i).neighbors:
                for k in self.net.node(j).neighbors:
                    turn = self.net.turn(i, j, k)
                    if turn.target_volume > 0:
                        self.od_seed.targets_o[i] += turn.target_volume  

        # Destination Turn Targets
        for k in check_destination_turns:
            self.od_seed.targets_d[k] = 0
            for j in self.net.node(k).up_neighbors:
                for i in self.net.node(j).up_neighbors:
                    turn = self.net.turn(i, j, k)
                    if turn.target_volume > 0:
                        self.od_seed.targets_d[k] += turn.target_volume


    def compute_od_diff(self):
        """Calculate difference between Estimated and Seed OD matrices."""
        for k in self.od_estimated.volume:
            self.od_diff.volume[k] = self.od_estimated.volume[k] - self.od_seed.volume[k]

    def estimate_od_fratar(self):
        print(f"Running Fratar Factoring")
        self.od_estimated = odme_fratar.estimate_od(self.od_seed)
        self.compute_od_diff()

    def estimate_od_leastsq(self, seed_od_weight: float):
        diagnostics, self.od_estimated = odme_leastsq.estimate_od(
                                            self.od_seed, 
                                            self.net, 
                                            self.select_link(only_target_links=True),
                                            self.select_turn(only_target_turns=True),
                                            seed_od_weight)
        self.compute_od_diff()

        return diagnostics

    def estimate_od_cmaes(self, weight_total_geh=None, weight_odsse=None, weight_route_ratio=None):
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

        res = odme_cmaes.estimate_od(
                self.net, 
                self.od_seed, 
                self.od_estimated, 
                weight_total_geh, 
                weight_odsse, 
                weight_route_ratio)
        
        self.compute_od_diff()
        
        return res

    def export_od(self, output_folder=None) -> None:
        """Write estimated OD to csv."""
        output_folder = _clean_folder_path(output_folder)
        od_write.export_od_as_list(self.net, self.od_estimated, output_folder)

    def export_turns(self, output_folder=None) -> None:
        """Write turns to csv."""
        output_folder = _clean_folder_path(output_folder)
        net_write.export_turns(self.net, output_folder)

    def export_od_by_route(self, output_folder=None) -> None:
        """Write estimated OD to csv, in list format, one row per OD pair."""
        output_folder = _clean_folder_path(output_folder)
        od_write.export_od_by_route(self.net, output_folder)

    def export_node_sequence(self, output_folder=None) -> None:
        """Write the links and turns on every OD route to csv."""
        output_folder = _clean_folder_path(output_folder)
        net_write.export_node_sequences(self.net, output_folder)

    def export_route_list(self, output_folder=None) -> None:
        """Export the nodes along each route. One row per route."""
        output_folder = _clean_folder_path(output_folder)
        net_write.export_route_list(self.net, output_folder)

    def get_node_name(self, node: int) -> str:
        """Return the name of the node."""
        return self.net.node(node).name

    def get_nodes(self) -> list['NetNode']:
        """Return a list of nodes in the network."""
        if not self.net:
            return
        
        return list(self.net.nodes())

    def get_links(self) -> list['NetLinkData']:
        """Return a list of data for each link."""
        if not self.net:
            return
        
        return list(self.net.links())

    def get_routes(self) -> list[RouteInfo]:
        """Return basic OD information for each route."""
        routes: list[RouteInfo] = []
        
        for od in self.net.od_pairs:
            o_name = self.net.node(od.origin).name
            d_name = self.net.node(od.destination).name

            for route in od.routes:
                basic_info = RouteInfo(od.origin, 
                                       od.destination, 
                                       o_name,
                                       d_name,
                                       route.name,
                                       route.nodes)

                routes.append(basic_info)

        return routes

    def select_link(self, only_target_links=False) -> dict[LinkKey, dict[ZonePairKey, float]]:
        """Return zone pairs that flow through each network link."""

        select_link: dict[LinkKey, dict[ZonePairKey, float]] = \
            self._init_select_element("link", only_target_links)
        
        for od in self.net.od_pairs:
            zone_pair_key = (od.origin, od.destination)
            for route in od.routes:
                route_ratio = route.target_ratio
                n_route_nodes = len(route.nodes)

                if n_route_nodes <= 1:
                    # route is O == D
                    continue

                # route has 2 or more nodes
                for x in range(0, n_route_nodes - 1):
                    i = route.nodes[x]
                    j = route.nodes[x + 1]
                    if (i, j) not in select_link: continue
                    select_link[(i, j)].setdefault(zone_pair_key, 0)
                    select_link[(i, j)][zone_pair_key] += route_ratio

        return select_link  


    def select_turn(self, only_target_turns=False) -> dict[TurnKey, dict[ZonePairKey, float]]:
        """Return zone pairs that flow through each network turn."""

        select_turn: dict[TurnKey, dict[ZonePairKey, float]] = \
            self._init_select_element("turn", only_target_turns)

        for od in self.net.od_pairs:
            zone_pair_key = (od.origin, od.destination)
            for route in od.routes:
                route_ratio = route.target_ratio
                n_route_nodes = len(route.nodes)

                if n_route_nodes <= 2:
                    # Need at least 3 nodes in a sequence to have turns
                    continue

                # route has 3 or more nodes
                for x in range(0, n_route_nodes - 2):
                    i = route.nodes[x]
                    j = route.nodes[x + 1]
                    k = route.nodes[x + 2]
                    if (i, j, k) not in select_turn: continue
                    select_turn[(i, j, k)].setdefault(zone_pair_key, 0)
                    select_turn[(i, j, k)][zone_pair_key] += route_ratio

        return select_turn 

    def _init_select_element(self, element: str = "link", only_elements_with_targets=False) -> dict:
        select_element = {}
        
        if element == "link":
            elements = self.net.links(True)
        elif element == "turn":
            elements = self.net.turns(True)
        else:
            raise Exception(f"Unknown element {element}. Expected 'link' or 'turn'.")

        if only_elements_with_targets:
            for key, element in elements:
                if element.target_volume == -1:
                    continue
                select_element[key] = {}
        else:
            for key, _ in elements:
                select_element[key] = {}

        return select_element


def _clean_file_path(file_path: str) -> str:
    """Check if a file exists and return a valid path, else None."""
    if file_path is None:
        return None

    file_path = file_path.replace('"', '')
    if not os.path.isfile(file_path):
        return None

    return file_path


def _clean_folder_path(folder_path: str) -> str:
    """Check if a folder exists and return a valid path, else None."""
    if folder_path is None:
        return None

    folder_path = folder_path.replace('"', '')
    if not os.path.isdir(folder_path):
        return None

    return folder_path

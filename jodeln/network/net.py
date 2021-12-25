"""Contains the Network class and related classes.
"""

import sys
from dataclasses import dataclass
from .geh import geh
from typing import List, Dict, Tuple, Generator
from collections import Counter


@dataclass
class NetRoute():
    """Contains sequence of nodes from origin to destination.

    Attributes
    ----------
    nodes : List[int]
        Ordered sequence of node IDs along the route, from origin to destination.
    name : str
        Human-readable name for the route. Does not have to be unique amongst all routes.
    seed_volume : float
        Volume on the route assigned from the seed OD matrix.
    target_ratio : float
        If one OD pair has multiple routes, this is the desired proportion of the 
        total OD volume that should occur on this route.
    target_rel_diff : float
        If one OD pair has multiple routes, this is a helper variable for the OD
        optimization that indicates how different this route is relative to all 
        other routes within the OD. For example, 2 routes, one has a target_ratio 
        of 0.8, the other 0.20. The target relative differences are 0.60 and -0.60, 
        respectively.
    assigned_volume : float
        Volume assigned to this route based on the estimated OD matrix.
    assigned_ratio : float
        If one OD pair has multiple routes, this is the actual proportion of the 
        total estimated OD volume. assigned_ratio is compared to the target_ratio
        in the OD optimization.
    opt_var_index : int
        Helper variable for the OD optimization algorithm. The OD optimization
        takes a list of variables. opt_var_index is the position of this route 
        within the list of optimization variables.
    """
    __slots__ = ['nodes', 'name', 'seed_volume', 'target_ratio', 'target_rel_diff',
                 'assigned_volume', 'assigned_ratio', 'opt_var_index']
    nodes: List[int]
    name: str
    seed_volume: float
    target_ratio: float
    target_rel_diff: float
    assigned_volume: float
    assigned_ratio: float
    opt_var_index: int


@dataclass
class NetODpair():
    """Origin-Destination data in the Network. 
    
    Attributes
    ----------
    origin : int
        node ID of the OD origin.
    destination : int
        node ID of the OD destination.
    seed_total_volume : float
        Volume for this OD pair within the seed OD matrix.
    est_total_volume : float
        Volume for this OD pair within the estimated OD matrix.
    routes : List[route]
        List of all possible routes from origin to destination to include in the
        OD optimization. One OD can contain multiple routes.
    """
    __slots__ = ['origin', 'destination', 'seed_total_volume', 'est_total_volume', 'routes']
    origin: int
    destination: int
    seed_total_volume: float
    est_total_volume: float
    routes: List[NetRoute]

@dataclass
class LinkParameters():
    """Parameters needed for constructing a NetLinkData object.
    """
    __slots__ = ['name', 'cost', 'target_volume']
    name: str
    cost: float
    target_volume: float


@dataclass
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
    link_index: int
        Unique identifier for this link.
    assigned_volume: float
        Volume on the link as assigned from the estimated OD matrix.
    geh: float
        GEH statistic comparing the target_volume and assigned_volume.
    seed_volume: float
        Volume on the link as assigned from the seed OD matrix.
    """
    __slots__ = ['cost', 'name', 'target_volume', 'link_index', 'assigned_volume', 'geh', 'seed_volume']
    cost: float
    name: str
    target_volume: float
    link_index: int
    assigned_volume: float
    geh: float
    seed_volume: float


@dataclass
class TurnData():
    """Data on Network turns.
    
    A turn is a sequence of three consecutive nodes: A-B-C. In this case "B"
    is the intersection, A is upstream, and C is downstream.

    Attributes
    ----------
    key: int
        Unique ID for the turn.
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
    key: int
    name: str
    seed_volume: float
    target_volume: float
    assigned_volume: float
    geh: float


@dataclass
class NodeParameters():
    """Parameters needed for constructing a NetNode object.
    """
    __slots__ = ['name', 'x', 'y', 'is_origin', 'is_destination']
    name: str
    x: float
    y: float
    is_origin: bool
    is_destination: bool


class NetNode():
    """A point (junction) in the network graph.

    Two connected nodes form an link. A sequence of three nodes forms a 
    Turn (see TurnData).

    Attributes
    ----------
    key : int
        Unique identifier for the node.
    name : str
        Name, or label, for the node.
    x : float
        x-coordinate of node. Defaults to zero.
    y : float
        y-coordinate of node. Defaults to zero.
    is_origin : bool
        Indicates if traffic can start their trip from this node (source node)
    is_destination : bool
        Indicates if traffic can end their trip at this node (sink node)
    neighbors : Dict[int, NetLinkData]
        Adjacency list of connected downstream node IDs and associated data
    up_neighbors : list
        Upstream node IDs connected to this node.
    """
    def __init__(self, key, parameters: NodeParameters):
        """Create a node in the network graph.

        Parameters
        ----------
        key : int
            Unique identifier.
        parameters : NodeParameters
            Data about the node. Name, x,y coordinates, etc.
        """
        self.key = key
        
        self.name = parameters.name
        self.x = parameters.x
        self.y = parameters.y
        self.is_origin = parameters.is_origin
        self.is_destination = parameters.is_destination

        self.neighbors = {} # type: Dict[int, NetLinkData]
        self.up_neighbors = []

    def add_neighbor(self, neighbor, link_data) -> None:
        """Connects two nodes to form an link.

        links are stored as an adjacency list.

        Parameters
        ----------
        neighbor : int
            Unique identifier of neighboring (connecting) node.
        link_data : NetLinkData
            See NetLinkData class.
        """
        self.neighbors[neighbor] = link_data

    def get_connections(self):
        """Return list of node keys connected to self node."""
        return self.neighbors.keys()


class Network():
    """Contains the network nodes and links, turns, and assigned origin-destination 
    information.

    Nodes and links are stored in an 'adjaceny list' graph data structure.
    For example: self.nodes = {node id, node data}
    where node data contains the connected nodes that form the network links.

    Attributes
    ----------
    nodes : Dict[int, NetNode]
        nodes within the Network graph.
    turns : Dict[int, TurnData]
        Turns within the Network graph.
    n_links : int
        number of links in the network.
    od : List[NetODpair]
        OD data for the network.
    total_geh : int
        Grand total of summing all the GEH values of the links and turns. 
        See the calc_network_geh method.
    """
    __slots__ = ['nodes', 'turns', 'n_links', 'od', 'total_geh']

    def __init__(self):
        self.nodes = {} # type: Dict[int, NetNode]
        self.turns = {}  # type: Dict[Tuple[int, int, int], TurnData]
        self.n_links = 0
        self.od = [] # type: List[NetODpair]
        self.total_geh = 0

    def add_node(self, parameters: NodeParameters) -> None:
        """Add a node to the network graph.

        Parameters
        ----------
        parameters : NodeParameters
            Data about the node. Name, x,y coordinates, etc.
        """
        key = len(self.nodes)
        self.nodes[key] = NetNode(key, parameters)

    def add_link(self, i_name, j_name, parameters: LinkParameters) -> None:
        """Connects two nodes to form an link in the network graph.

        Parameters
        ----------
        i_name : str
            Origin node name
        j_name : str
            Destination node name
        parameters : LinkParameters
            Data belonging to the link. Name, cost, etc.
        """
        i_key, _ = self.get_node_by_name(i_name) 
        j_key, _ = self.get_node_by_name(j_name) 
        
        link_data = NetLinkData(
            cost=parameters.cost, 
            name=parameters.name,
            target_volume=parameters.target_volume,
            link_index=self.n_links,
            assigned_volume=0,
            geh=0,
            seed_volume=0)

        self.nodes[i_key].add_neighbor(j_key, link_data)
        self.n_links += 1

        self.nodes[j_key].up_neighbors.append(i_key)
        
    def link(self, i, j):
        """Convenience function to access link properties."""
        return self.nodes[i].neighbors[j]

    def links_(self) -> Generator[Tuple[int, int, NetLinkData], None, None]:
        """Generator function to iterate through all the links.
        
        Function name has a trailing underscore for consistency with self.turns_()
        """
        for i, node in self.nodes.items():
            for j, _ in node.neighbors.items():
                yield (i, j, self.nodes[i].neighbors[j])

    def turns_(self) -> Generator[Tuple[Tuple[int, int, int], TurnData], None, None]:
        """Generator function to itertae through all the turns.

        Function name has a trailing underscore to avoid conflict with self.turns
        variable name. Function is implemented to create consistent looking code 
        when iterating through all the turns or iterating through all the links.
        e.x.:
           "for k, v in net.turns_()" or "for k, v in net.links_()"
        """
        for (i, j, k), turn in self.turns.items():
            yield (i, j, k), turn


    def init_turns(self) -> None:
        """Initialize all turns within the network."""

        turn_counter = 0
        for i, node1 in self.nodes.items():
            for j, _ in node1.neighbors.items():
                for k, _ in self.nodes[j].neighbors.items():
                    self.turns[(i, j, k)] = TurnData(key=turn_counter,
                                                     name=f'{i}_{j}_{k}',
                                                     seed_volume=0,
                                                     target_volume=0,
                                                     assigned_volume=0,
                                                     geh=0)
                    turn_counter += 1

    def init_routes(self) -> None:
        """Initialize routes by determining shortest route from all origins
        to all destinations."""

        for i, o_node in self.nodes.items():
            if not o_node.is_origin:
                continue

            result = _dijkstra(self, i)

            # for each destination, get route from O to D
            for j, d_node in self.nodes.items():
                if not d_node.is_destination:
                    continue
                
                node_seq = _node_seq_from_dijkstra(result, i, j)
                
                if len(node_seq) != 0:
                    od = NetODpair(i, j, 0, 0, [NetRoute(nodes=node_seq,
                                                         name="",
                                                         seed_volume=0, 
                                                         target_ratio=1,
                                                         target_rel_diff=1,
                                                         assigned_volume=0, 
                                                         assigned_ratio=1,
                                                         opt_var_index=-1)])
                    self.od.append(od)
        
        # Update route names
        self.set_route_names()

    def get_node_by_name(self, node_name):
        """Helper function to return a node by name."""
        for k, node in self.nodes.items():
            if node.name == node_name:
                return k, node
        else:
            # TODO: handle error if didn't find the node
            print(f'node name {node_name} not found')
            pass

    def calc_network_geh(self) -> None:
        """Sum up the total geh of all the links & turns in the network."""
        
        self.total_geh = 0
        
        # calc link geh
        for _, _, link in self.links_(): 
            # TODO: handle case when link has no raw volume
            link_geh = geh(link.target_volume, link.assigned_volume)
            link.geh = link_geh
            self.total_geh += link_geh
        
        # calc turn geh
        for _, t in self.turns_():
            # TODO: better handling when turn has no target volume
            if t.target_volume <= 0:
                continue
            turn_geh = geh(t.target_volume, t.assigned_volume)
            t.geh = turn_geh
            self.total_geh += turn_geh

    def init_seed_volumes(self, od_mat) -> None:
        """Assign route, link, and turn seed volumes based on an od matrix.

        Parameters
        ----------
        od_mat : Dict
            OD matrix, imported from csv. See od_read.py.
        """
        for od in self.od:
            od_volume = od_mat[(od.origin, od.destination)]
            od.seed_total_volume = od_volume
            for route in od.routes:
                route.seed_volume = od_volume * route.target_ratio
                route.assigned_volume = route.seed_volume

        self.set_link_and_turn_volume_from_route()

        for _, _, link in self.links_():
            link.seed_volume = link.assigned_volume
        
        for _, t in self.turns_():
            t.seed_volume = t.assigned_volume
    
    def set_link_and_turn_volume_from_route(self) -> None:
        """Calculate the volume on all links and turns based on the OD route volumes."""
        # reset link & turn volumes to zero
        for _, _, link in self.links_():
            link.assigned_volume = 0
        
        for _, t in self.turns_():
            t.assigned_volume = 0
        
        # assign link & turn volumes
        for od in self.od:
            for route in od.routes:
                n_route_nodes = len(route.nodes)
                
                if n_route_nodes <= 1:
                    # route is O == D
                    continue

                if n_route_nodes == 2:
                    # route is one link
                    i = route.nodes[0]
                    j = route.nodes[1]
                    self.link(i, j).assigned_volume += route.assigned_volume
                    continue

                # route has 3 or more nodes
                for x in range(0, len(route.nodes) - 2):
                    i = route.nodes[x]
                    j = route.nodes[x + 1]
                    k = route.nodes[x + 2]
                    self.link(i, j).assigned_volume += route.assigned_volume
                    self.turns[(i, j, k)].assigned_volume += route.assigned_volume

                j = route.nodes[x + 1]
                k = route.nodes[x + 2]
                self.link(j, k).assigned_volume += route.assigned_volume
   
    def set_route_names(self) -> None:
        """Assign unique route names within each OD.

        Unique names are assigned by finding a unique link on the route. For example,
        if there are two routes from A to B with nodes: A-X-Y-B and A-X-C-Y-B, 
        the two routes could be named "X-Y" and "X-C" because those links are 
        unique to their respective routes.
        """
        
        for od in self.od:
            # gather all the links on all routes from o to d
            od_links = []
            for route in od.routes:
                for x in range(0, len(route.nodes) - 1):
                    a = self.nodes[route.nodes[x]].name
                    b = self.nodes[route.nodes[x + 1]].name
                    od_links.append((a, b))
            
            # Find unique links based on counting how many times each link is used
            # amongst all the routes from o to d.
            link_counts = Counter(od_links)
            unique_links = [link for link, n in link_counts.items() if n == 1]
            
            # Assign route names based on a unique link along the route.
            for route in od.routes:
                for x in range(0, len(route.nodes) - 1):
                    a = self.nodes[route.nodes[x]].name
                    b = self.nodes[route.nodes[x + 1]].name
                    if (a, b) in unique_links:
                        route.name = str(a) + "_" + str(b)
                        # Remove link to prevent assigning the same name to mulitple routes.
                        unique_links.remove((a, b))
                        break



def _dijkstra(net: Network, source):
    """Uses dijkstra's algorithm to compute the shortest route between
    source and all destinations.
    
    The 'shortest route' returned is a sequence of nodes.
    Used the pseudocode on wikipedia: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode

    Parameters
    ----------
    net : Network
        Network to use in this shortest route algorithm.
    source : int
        ID of the origin node.

    Returns
    -------
    Dict
        Dictionary of distances and previous nodes. See _node_seq_from_dijkstra
        to extract the shortest routes from this dictionary.
    """
    
    # unvisited nodes
    Q = []
    
    # shortest distance to each node
    dist = {}

    # previous node on shortest route
    prev = {}

    for i in net.nodes:
        Q.append(i)  
        dist[i] = sys.maxsize
        prev[i] = None
    dist[source] = 0

    while len(Q) > 0:
        min_dist = sys.maxsize
        for i in Q:
            if dist[i] <= min_dist:
                u, min_dist = i, dist[i]

        Q.remove(u)

        for v, link in net.nodes[u].neighbors.items():
            alt = dist[u] + link.cost
            if alt < dist[v]:   
                dist[v] = alt
                prev[v] = u

    return {'dist': dist, 'prev': prev}


def _node_seq_from_dijkstra(dijkstra_result, origin, destination):
    """Helper function to convert dijkstra result to usable route data.

    Parameters
    ----------
    dijkstra_result : Dict
        Output from _dijkstra function.
    origin : int
        Origin node ID.
    destination : int
        Destination node ID.

    Returns
    -------
    List
        Sequence of node IDs along the shortest route from origin to destination.
    """

    if dijkstra_result['prev'][destination] is None: return [] # D unreachable from O
    if origin == destination: return [origin] # O == D

    node_seq = []
    u = destination

    while dijkstra_result['prev'][u] is not None:
        node_seq.append(u)
        u = dijkstra_result['prev'][u]
    
    if u == origin:
        node_seq.append(origin)

    node_seq.reverse()
    
    return node_seq

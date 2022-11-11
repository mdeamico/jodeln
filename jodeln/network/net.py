"""Contains the Network class and related classes.
"""

import sys
from collections import Counter
from typing import TYPE_CHECKING, Generator

from .geh import geh
from .netlink import NetLinkData
from .netnode import NetNode
from .netod import NetODpair
from .netroute import NetRoute
from .netturns import TurnData

if TYPE_CHECKING:
    from .netlink import LinkParameters
    from .netnode import NodeParameters
    

class Network():
    """Contains the network nodes and links, turns, and assigned origin-destination 
    information.

    Nodes and links are stored in an 'adjaceny list' graph data structure.
    For example: self.nodes = {node id, node data}
    where node data contains the connected nodes that form the network links.

    Attributes
    ----------
    _graph : Dict[int, NetNode]
        nodes within the Network graph.
    turns : Dict[int, TurnData]
        Turns within the Network graph.
    n_links : int
        number of links in the network.
    od : List[NetODpair]
        OD data for the network.
    total_geh : float
        Grand total of summing all the GEH values of the links and turns. 
        See the calc_network_geh method.
    coord_scale : float
        Scalar to convert node x,y position to real-world coordinates. Required
        to ensure the network is displayed legibly in the GUI.
    """
    __slots__ = ['_graph', '_turns', 'n_links', 'od', 'total_geh', 'coord_scale']

    def __init__(self):
        self._graph: dict[int, NetNode] = {}
        self._turns: dict[tuple[int, int, int], TurnData] = {}
        self.n_links: int = 0
        self.od: list[NetODpair] = []
        self.total_geh: float = 0
        self.coord_scale: float = 1

    def add_node(self, parameters: 'NodeParameters') -> None:
        """Add a node to the network graph.

        Parameters
        ----------
        parameters : NodeParameters
            Data about the node. Name, x,y coordinates, etc.
        """
        # FIXME: length not guaranteed to return a unique key number.
        key = len(self._graph)
        self._graph[key] = NetNode(key, parameters)

    def add_link(self, i_name, j_name, parameters: 'LinkParameters') -> None:
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
            seed_volume=0,
            shape_points=parameters.shape_points)

        self._graph[i_key].add_neighbor(j_key, link_data)
        self.n_links += 1

        self._graph[j_key].up_neighbors.append(i_key)

    def node(self, key: int) -> NetNode:
        """Convenience function to access node properties."""
        # TODO: Handle case if key is not in _graph.
        return self._graph[key]

    def nodes(self, return_keys: bool=False) -> \
        Generator[NetNode, None, None] | \
        Generator[tuple[int, NetNode], None, None]:
        """Generator function to return all network nodes"""
        for key, node in self._graph.items():
            if return_keys:
                yield key, node
            else:
                yield node

    def link(self, i: int, j: int) -> NetLinkData:
        """Convenience function to access link properties."""
        return self._graph[i].neighbors[j]

    def links(self, return_keys: bool=False) -> \
        Generator[NetLinkData, None, None] | \
        Generator[tuple[tuple[int, int], NetLinkData], None, None]:
        """Generator function to iterate through all the links."""
        for i, node in self._graph.items():
            for j, _ in node.neighbors.items():
                if return_keys:
                    yield (i, j), self._graph[i].neighbors[j]
                else:
                    yield self._graph[i].neighbors[j]

    def turn(self, i: int, j: int, k: int) -> TurnData:
        """Convenience function to access turn properties."""
        return self._turns[(i, j, k)]

    def turns(self, return_keys: bool=False) -> \
        Generator[TurnData, None, None] | \
        Generator[tuple[tuple[int, int, int], TurnData], None, None]:
        """Generator function to itertate through all the turns."""
        for key, turn in self._turns.items():
            if return_keys:
                yield key, turn
            else:
                yield turn


    def init_turns(self) -> None:
        """Initialize all turns within the network."""

        for i, node1 in self._graph.items():
            for j, _ in node1.neighbors.items():
                for k, _ in self._graph[j].neighbors.items():
                    self._turns[(i, j, k)] = TurnData(key=(i, j, k),
                                                     name=f'{i}_{j}_{k}',
                                                     seed_volume=0,
                                                     target_volume=0,
                                                     assigned_volume=0,
                                                     geh=0)

    def init_routes(self) -> None:
        """Initialize routes by determining shortest route from all origins
        to all destinations."""

        for i, o_node in self._graph.items():
            if not o_node.is_origin:
                continue

            result = _dijkstra(self, i)

            # for each destination, get route from O to D
            for j, d_node in self._graph.items():
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
        for k, node in self._graph.items():
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
        for link in self.links(): 
            # TODO: handle case when link has no raw volume
            link_geh = geh(link.target_volume, link.assigned_volume)
            link.geh = link_geh
            self.total_geh += link_geh
        
        # calc turn geh
        for t in self.turns():
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

        for link in self.links():
            link.seed_volume = link.assigned_volume
        
        for t in self.turns():
            t.seed_volume = t.assigned_volume
    
    def set_link_and_turn_volume_from_route(self) -> None:
        """Calculate the volume on all links and turns based on the OD route volumes."""
        # reset link & turn volumes to zero
        for link in self.links():
            link.assigned_volume = 0
        
        for t in self.turns():
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
                    self.turn(i, j, k).assigned_volume += route.assigned_volume

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
                    a = self._graph[route.nodes[x]].name
                    b = self._graph[route.nodes[x + 1]].name
                    od_links.append((a, b))
            
            # Find unique links based on counting how many times each link is used
            # amongst all the routes from o to d.
            link_counts = Counter(od_links)
            unique_links = [link for link, n in link_counts.items() if n == 1]
            
            # Assign route names based on a unique link along the route.
            for route in od.routes:
                for x in range(0, len(route.nodes) - 1):
                    a = self._graph[route.nodes[x]].name
                    b = self._graph[route.nodes[x + 1]].name
                    if (a, b) in unique_links:
                        route.name = str(a) + "_" + str(b)
                        # Remove link to prevent assigning the same name to mulitple routes.
                        unique_links.remove((a, b))
                        break

    def set_coord_scale(self):
        """Scales the node x,y coordinates to to ensure the network is displayed
        legibly in the GUI. Scale value is saved in self.coord_scale
        """
        coords = []
        for node in self.nodes():
            coords.append((node.x, node.y))
        
        # Calculate extents, min/max on x-axis and y-axis
        min_x = min([x for x, _ in coords])
        max_x = max([x for x, _ in coords])
        
        min_y = min([y for _, y in coords])
        max_y = max([y for _, y in coords])
        print(f"extents: {min_x}, {max_x}, {min_y}, {max_y}")

        # Calculate scale factor
        legible_diff = 1000
        scale_factor_x = legible_diff / abs(max_x - min_x)
        scale_factor_y = legible_diff / abs(max_y - min_y) 
        self.coord_scale = max(scale_factor_x, scale_factor_y)

        # Scale node coordinates and link shape points
        for node in self.nodes():
            node.x *= self.coord_scale
            node.y *= self.coord_scale

        for link in self.links():
            new_shape_points = [(x * self.coord_scale, y * self.coord_scale) for x, y in link.shape_points]
            link.shape_points = new_shape_points


def _dijkstra(net: Network, source: int):
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

    for i in net._graph:
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

        for v, link in net._graph[u].neighbors.items():
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

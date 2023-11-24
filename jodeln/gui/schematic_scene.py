from PySide2.QtWidgets import QGraphicsScene
from .schematic_items import LinkItem, NodeItem

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    import PySide2.QtWidgets    

class NodeData(Protocol):
    @property
    def name(self) -> str:
        ...
    @property
    def x(self) -> float:
        ...
    @property
    def y(self) -> float:
        ...

class LinkData(Protocol):
    @property
    def key(self) -> tuple[int, int]:
        ...
    @property
    def shape_points(self) -> list[tuple[float, float]]:
        ...    

class RouteInfo(Protocol):
    @property
    def origin(self) -> int:
        ...
    @property
    def destination(self) -> int:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def nodes(self) -> list[int]:
        ...

class SchematicScene(QGraphicsScene):
    """QGraphicsScene for displaying the network.

    Attributes
    ----------
    links : dict[tuple[int, int], LinkItem]
        Stores a LinkItem for each link in the network.
        Keyed by: (start node id, end node id)
    route_nodes: dict[tuple[int, int, str], list[int]]
        Stores the nodes along each route.
        Keyed by: (route.origin, route.destination, route.name) 
    """
    
    def __init__(self):
        super().__init__()
        self.links: dict[tuple[int, int], LinkItem] = {}
        self.route_nodes: dict[tuple[int, int, str], list[int]] = {}
        self.nodes: list[NodeItem] = []

    def load_network(self, nodes: list[NodeData], links: list[LinkData]) -> None:
        """Transfer network node and link data from the Model to the SchematicScene. 

        Parameters
        ----------
        nodes : list[NodeData]
            List of basic data for each node: x, y, name.
        links : List[LinkData]
            List of basic data for each link: key, list of points
        """
        for n in nodes:
            new_node_item = NodeItem(n.x, n.y, n.name)
            self.nodes.append(new_node_item)
            self.addItem(new_node_item)
        
        for link in links:
            new_link_item = LinkItem(link.shape_points)
            self.links[link.key] = new_link_item
            self.addItem(new_link_item)

    def load_routes(self, routes: list[RouteInfo]) -> None:
        """Transfers data about the routes and od from the Model to the SchematicScene.

        Parameters
        ----------
        routes : list[RouteInfo]
            Basic info about the route for each OD. 
            Includes route origin, destination, route name, and nodes.
        """
        for route in routes:
            self.route_nodes[(route.origin, route.destination, route.name)] = route.nodes

    def color_route(self, route: tuple[int, int, str], is_selected: bool) -> None:
        """Sets a bool to indicate if the link is on the user-selected path.

        LinkItem objects in the scene can update themselves to be colored based
        on the selection bool.

        Parameters
        ----------
        route : tuple[int, int, str]
            Route identifier tuple: (route.origin, route.destination, route.name)
        is_selected : bool
            True if the the link is on the user selected path.
        """
        route_nodes = self.route_nodes[route]

        for x in range(len(route_nodes) - 1):
            i = route_nodes[x]
            j = route_nodes[x + 1]
            self.links[(i, j)].is_on_selected_path = is_selected

    def scale_node_labels(self, value):
        for n in self.nodes:
            n.node_label.set_size_multiplier(value / 10.0)
        self.update()

    def scale_nodes(self, value):
        for n in self.nodes:
            n.set_diameter(value)
        self.update()

    def zoom(self, lod):
        for n in self.nodes:
            n.set_label_pos(lod)
        self.update()

    def mousePressEvent(self, event: 'PySide2.QtWidgets.QGraphicsSceneMouseEvent') -> None:
        return super().mousePressEvent(event)

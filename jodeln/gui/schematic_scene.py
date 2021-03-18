from PySide2.QtWidgets import QGraphicsScene
from .schematic_items import LinkItem, NodeItem

from typing import TYPE_CHECKING
from typing import List
from model import RouteInfo

if TYPE_CHECKING:
    import PySide2.QtWidgets    



class SchematicScene(QGraphicsScene):
    """QGraphicsScene for displaying the network.

    Attributes
    ----------
    links : Dict
        Stores a LinkItem for each link in the network.
        Keyed by: (start node id, end node id)
    routes: Dict
        Stores the nodes along each route.
        Keyed by: (route.origin, route.destination, route.name) 
    """
    
    def __init__(self):
        super().__init__()
        self.links = {}
        self.routes = {}

    def load_network(self, nodes, links):
        """Transfer network node and link data from the Model to the SchematicScene. 

        Parameters
        ----------
        nodes : Dict
            {i: (x, y, name)} Dict of coordinates for each node.
        links : List
            [(i, j), ...] List of start/end node numbers for each link.
        """
        for _, (x, y, name) in nodes.items():
            self.addItem(NodeItem(x, y, name))
        
        for (i, j) in links:
            self.links[(i, j)] = LinkItem(nodes[i][0],
                                          nodes[i][1],
                                          nodes[j][0],
                                          nodes[j][1])

            self.addItem(self.links[(i, j)])

    def load_routes(self, routes: List[RouteInfo]):
        """Transfers data about the routes and od from the Model to the SchematicScene.

        Parameters
        ----------
        routes : List[RouteInfo]
            Basic info about the route for each OD. 
            Includes route origin, destination, route name, and nodes.
        """
        for route in routes:
            self.routes[(route.origin, route.destination, route.name)] = route.nodes

    def color_route(self, route, is_selected):
        """Sets a bool to indicate if the link is on the user-selected path.

        LinkItem objects in the scene can update themselves to be colored based
        on the selection bool.

        Parameters
        ----------
        route : Tuple
            Route identifier tuple: (route.origin, route.destination, route.name)
        is_selected : bool
            True if the the link is on the user selected path.
        """
        for x in range(len(self.routes[route]) - 1):
            i = self.routes[route][x]
            j = self.routes[route][x + 1]
            self.links[(i, j)].is_on_selected_path = is_selected

    def mousePressEvent(self, event: 'PySide2.QtWidgets.QGraphicsSceneMouseEvent') -> None:
        return super().mousePressEvent(event)

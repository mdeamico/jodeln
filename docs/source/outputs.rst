Jodeln Outputs
==============

Jodeln can output **4 csv files** related to the network and routes. 

1. **csv of nodes** along the routes for each origin-destination pair.

.. code-block::

    A,W,X,Z,D



2. **csv of links** (sequence of 2 nodes) between the origin and destination. Each route is automatically assigned a unique name based on the lowest-cost route. The lowest-cost route between A and D goes through link W-X, and is therefore assigned the route name **W_X**.

.. code-block::

    o_node,d_node,route,a_node,b_node
    A,D,W_X,A,W
    A,D,W_X,W,X
    A,D,W_X,X,Z
    A,D,W_X,Z,D
    ...


3. **csv of turns** (sequence of 3 nodes) between the origin and destination.

.. code-block::

    o_node,d_node,route,a_node,b_node,c_node
    A,D,W_X,A,W,X
    A,D,W_X,W,X,Z
    A,D,W_X,X,Z,D



4. **csv of all turns** (sequence of 3 nodes) within the network. This is useful for creating a file of target turning volumes for OD matrix estimation. 

.. code-block::

    a_node,b_node,c_node
    A,W,B
    A,W,X
    A,W,Y
    ...

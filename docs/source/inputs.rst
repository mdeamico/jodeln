User Inputs
===========

Jodeln can accept inputs in csv or shapefile (shp) format.

Inputs include:

- :ref:`Nodes`
- :ref:`Links`
- :ref:`Turns`
- :ref:`Routes`
- :ref:`Seed OD matrix`

.. _Nodes:

Nodes
-----
The Nodes input file defines the start and end points for each link in the network.

Nodes csv
~~~~~~~~~~

Columns in node csv include the following, in this order:

1. node name
2. x-coordinate
3. y-coordinate
4. is_origin (0 = False, 1 = True)
5. is_destination (0 = False, 1 = True)

The first line of the csv file must be a header row.

.. code-block::

    name,x,y,is_origin,is_destination
    100,103,100,1,0
    101,126,127,1,0
    102,163,100,0,0
    103,224,100,0,0
    104,258,127,0,1
    105,280,100,0,1

Nodes shapefile
~~~~~~~~~~~~~~~
A nodes shapefile needs to contain point data types with the following attribute
(field) names and *[types]*:

- name *[string]*
- is_origin *[integer (0 = False, 1 = True)]*
- is_destina *[integer (0 = False, 1 = True)]*

Other attributes will be ignored.


.. _Links:

Links
-----
The Links input file defines the connection between two nodes.

Links csv
~~~~~~~~~~
Each travel direction must be included independently, e.x. A-B and B-A are
two separate links (two rows in the csv).

Columns in link csv include the following, in this order:

1. from_node
2. to_node
3. cost
4. name
5. target_volume

.. code-block::

    from_node,to_node,cost,name,target_volume
    100,102,3.2,9000,100
    101,102,7.1,9001,75
    102,103,4.0,9002,175
    103,104,5,9003,50
    103,105,9.32,9004,125

The first line of the csv file must be a header row.

Links shapefile
~~~~~~~~~~~~~~~
A links shapefile needs to contain polyline data types with the following attribute
(field) names and *[types]*:

- name *[string]*
- cost *[double]*
- target_vol *[double]*
- oneway *[integer (1 = one-way link, 2 = two-way link)]*

Other attributes will be ignored.

Unlike the links csv format, two-way links can be specified as one entity in the
shapefile with the *oneway* attribute set to 2. Alternatively, two separate links
could be used, each with *oneway* set to 1.

The links shapefile does not need to include the link start and end nodes. Start
and end nodes are determined automatically based on the closest node coordinates
and digitized direction of the link. Links must be drawn in the direction traveling
from the start node to the end node.

.. _Turns:

Turns
-----
Turns are any portion of a route traversing 3 nodes, ex: A-B-C

A Turns csv file contains these columns, in this order:

1. A node name
2. B node name
3. C node name
4. turn name
5. target volume

The first line of the csv file must be a header row.

Example Turns csv:

.. code-block::

    a_node,b_node,c_node,name,target_volume
    100,102,103,t1,100
    101,102,103,t2,75
    102,103,104,t3,50
    102,103,105,t4,125

.. _Routes:

Routes
------
All routes between O and D must be contained in the Route csv. For example,
if there is one existing route between O and D, and the user wants to add a 
new second route, both the existing and new route must be contained in the csv.

Columns in the route csv include the following, in this order:

1. origin: node name
2. destination: node name
3. target_ratio: how much volume should be on the route
                (e.x. 0.20 means 20% of the total OD volume should be on this route)
4. sequence: comma separated values of the node names from O to D

The first line of the csv file must be a header row.

Example Route csv:

.. code-block::

    o_node,d_node,target_ratio,sequence
    A,C,0.8,A,W,X,Z,C
    A,D,0.8,A,W,X,Z,D
    B,C,0.8,B,W,X,Z,C
    B,D,0.8,B,W,X,Z,D
    A,C,0.2,A,W,Y,Z,C
    A,D,0.2,A,W,Y,Z,D
    B,C,0.2,B,W,Y,Z,C
    B,D,0.2,B,W,Y,Z,D

.. _Seed OD Matrix:

Seed OD Matrix
--------------
An OD matrix must be in square format (n rows = n columns). An additional first 
column defines the zone names and order. All zones must be included in the same
order in both the rows and columns. If a zone is an origin-only, or 
destination-only zone, then fill the corresponding row or column values with zeros.

The following is an example csv for four zones named A, B, C, D.
Zone D is not a destination, C is not an origin. 
The OD volume from A to C is 250.

.. code-block::

    A,0,100,250,0
    B,99,0,98,0
    C,0,0,0,0 
    D,10,12,12,0


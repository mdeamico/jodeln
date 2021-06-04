# Jodeln
Jodeln helps you solve shortest-path and origin-destination (OD) estimation problems.
(Pronounced *Yo-den* - [What's with the name?](#))

Jodeln can:

- Export shortest paths from a network of links and nodes.
- Estimate an OD matrix based on an initial (seed) matrix and target volumes on link and turns.
- Estimate an OD matrix with multiple user-defined routes between OD pairs (i.e. matrix estimation with parallel routes).

Path outputs from Jodeln are especially useful for developing custom traffic assignment spreadsheets [Link to example](#).

Jodeln *is not* a travel demand model. It is also *not* a network editor. Users are expected to create compatible networks using GIS or other means.

# Resources (TODO)
- [Installation - TODO](#)
- [Documentation for users - TODO](#)
- [Documenation for developers - TODO](#)
- [License - TODO](#)

# Examples
## Path Finding Example
Given a network as shown, what is the shortest route between A and D? The cost to travel on each link is shown as a number between the nodes.

![network](./tests/networks/net04/net04_example.png)

There are two possible routes between A and D.

- A-W-**X**-Z-D: Total cost = 27
- A-W-**Y**-Z-D: Total cost = 28

For this network, Jodeln would automatically find the lowest-cost route via node **X**. The user can override Jodeln's path finding by importing their own set of one or more routes for each OD pair.

## Path Finding Outputs

Jodeln can output **4 csv files** related to the network and routes. The following examples show the primary two csv files. The elipsis in each example indicates that more rows would be included for other OD pairs beyond the example OD from A to D (i.e. the files would include A to C, B to D, etc).

An output **csv of links** lists each link (sequence of two nodes) along a route from the origin to the destination. Each route is automatically assigned a unique name based on a unique link within the route. The lowest-cost route between A and D goes through link W-X, and is therefore assigned the name **W_X** in the route column.

| o_node | d_node | route | a_node | b_node |
|--------|--------|-------|--------|--------|
| A      | D      | W_X   | **A**  | W      |
| A      | D      | W_X   | W      | X      |
| A      | D      | W_X   | X      | Z      |
| A      | D      | W_X   | Z      | **D**  |
| ...    | ...    | ...   | ...    | ...    |


An output **csv of turns** lists each turn (sequence of 3 nodes) along a route from the origin to the destination.

| o_node | d_node | route | a_node | b_node | c_node |
|--------|--------|-------|--------|--------|--------|
| A      | D      | W_X   | **A**  | W      | X      |
| A      | D      | W_X   | W      | X      | Z      |
| A      | D      | W_X   | X      | Z      | **D**  |
| ...    | ...    | ...   | ...    | ...    | ...    |

### How are Path Finding Outputs Helpful?

One way to use the csv outputs is for traffic assignment spreadsheets. Consider the following example problem:

> Given the following OD volume matrix, find the volume on each network link. Origins are in the rows, destinations in the columns.

|       | C   | D  |
|-------|-----|----|
| **A** | 100 | 35 |
| **B** | 20  | 75 |

This problem can be solved by importing the **csv of links** into a spreadsheet and adding an *OD volume* column to the table. For each row, the *OD volume* column looks up the *o_node*-*d_node* pair within the OD matrix and returns the volume (each A-D row contains the volume 35, each A-C row contains 100, etc).

| row |  o_node | d_node | route | a_node | b_node | *OD volume* |
|-----| --------|--------|-------|--------|--------|-------------|
| 1   |  A      | D      | W_X   | A      | W      | 35          |
| 2   |  A      | D      | W_X   | W      | X      | 35          |
| 3   |  A      | D      | W_X   | X      | Z      | 35          |
| 4   |  A      | D      | W_X   | Z      | D      | 35          |
| 5   |  A      | C      | W_X   | A      | W      | 100         |
| ... |  ...    | ...    | ...   | ...    | ...    | ...         |

The volume on each link can be found by conditionally summing the *OD volume* column. For example, the volume on link A-W can be found by summing the *OD volume* column for all rows where *a_node* = A and *b_node* = W. The volume on link A-W = 135 (found by summing *OD volume* for rows 1 and 5, assuming none of the elipsis rows affect link A-W).

Volumes on turns within the network can be found by using similar logic to the above example. Other uses for Jodeln outputs are left to the imagination of the user.


## OD Matrix Estimation Example
In this example, Jodeln estimates an OD matrix based on user-inputs consisting of an initial (seed) matrix, link target volumes, and assumed route percentages.

*The network and link costs:*

![network](./tests/networks/net04/net04_link_costs.png)

*Target volumes:*

![network](./tests/networks/net04/net04_target_volumes.png)

*Routes:*

There is more than one route from each origin to each destination. Jodeln only automatically finds the single shortest route. If the user wants to include multiple routes (or override the shortest route), they must input the routes and assumed percentages manually. Jodeln does not have any functions to estimate route percentages. The OD matrix estimation will try to respect the assumed input route percentages, but may deviate in order to meet the target volumes.

In this example, there are two routes from each origin to each destination (Origins: A, B. Destinations: C, D.) The user-assumed inputs are 80% of traffic using the route via node X, and 20% via node Y.

![network](./tests/networks/net04/net04_route_pct.png)


*Seed OD matrix of total traffic between each origin and destination:*

|       | C   | D  |
|-------|-----|----|
| **A** | 100 | 35 |
| **B** | 20  | 75 |

### Outputs

Given the above inputs, the estimated OD matrix from Jodeln is shown below. Because Jodeln uses an evolutionary stragegy ([CMA-ES](https://en.wikipedia.org/wiki/CMA-ES)) for estimating OD, the outputs may differ slightly each time you run the program. Outputs from Jodeln are in csv format, and include the total traffic for each OD pair as well as the traffic assigned to each route.

| Totals |       | 130    | 105   |
|--------|-------|--------|-------|
|        |       | **C**  | **D** |
| 160    | **A** | 116.27 | 43.73 |
|  75    | **B** | 13.73  | 61.27 |


## What's with the name Jodeln?
A hip name is the hallmark of modern software. The Origin-Destination abbreviation 
"OD" is pronounced "oh-dee." Repeating "OD" over-and-over again in a rhythmic pattern 
sounds a lot like the background music in the Price is Right game Cliff Hanger
(oh-dee oh-dee oh, oh-dee oh-dee oh...). In German, yodel is written yodeln. 
Both written words have "od" in the middle of them, so there you go. When you are 
done with your OD estimation you might want to Yodel too!

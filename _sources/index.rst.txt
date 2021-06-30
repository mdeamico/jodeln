Jodeln
==================================
Jodeln helps you solve shortest-path and origin-destination (OD) estimation problems.
(Jodeln is pronounced *yo-den* `What's with the name? <#what-s-with-the-name>`__)

Features:

- Export lists of links and turns along the shortest path between every OD pair in a network.
  (Think `Dijkstra's algorithm <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>`__)
- Refine a seed OD matrix to meet link and turn target volumes within a network (experimental feature).

Outputs are especially useful for developing custom traffic assignment spreadsheets.
`Example <#>`__.

Jodeln *is not* a travel demand model.
It is also *not* a network editor.
Users are expected to create compatible networks using GIS or other means.


.. toctree::
   :maxdepth: 1
   :caption: Contents

   installation
   quick_start
   conceptual_examples
   inputs
   outputs
   modules


What's with the name?
=========================
A hip name is the hallmark of modern software. 
The Origin-Destination abbreviation "OD" is pronounced "oh-dee."
Repeating "OD" over-and-over again in a rhythmic pattern sounds a lot like the background music in the Price is Right game "Cliff Hanger" (`listen when the hiker climbs <https://youtu.be/8qHZWYcydGY?t=116>`__): oh-dee oh-dee oh, oh-dee oh-dee oh...).
In German, yodel is written yodeln.
Both written words have "od" in the middle of them, so there you go.
When you are done with your OD estimation you might want to Yodel too!


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

# Tile based approximator

## Problem formulation

- The **primary task** is to approximate a multidimensional function that: 
  - Has a codomain that positive reals (prices) 
  - Has a domain that defined by continuous paths over a Geo-spatial route network
- The **simplified task** is to approximate six-dimensional function:
  - The coordinates of the route points are ignored and only route distances are used
  - The function domain becomes five-dimensional: start-latitude, start-longitude, end-latitude, end-longitude, distance
- A **transportation trip** is a Geo-spatial route from a start point to an end point and associated a price.
- A set of transportation trips is used to solve the primary- and simplified tasks.
  - That set can be small or large.
  - It is expected that the trips are consistent according to a certain rationale.

---

## General idea

- In order to approximate the pricing function of the primary task we use a Mathematical Artifact (MA) that is 
composed of Geo-spatial tiles that cover the geographical area of interest.
- For a given pair of geographical start- and end point MA finds a route over the route network and derives the corresponding prices from the tiles the route passes through.
- Each tile contributes to MA's (approximating) price in an additive manner.
- All tiles use the same formula based on the same *generic variables*.
- The *generic variables* associated with each tile are:
  - Distance multiplication factor
  - Offset
  - Departure offset
  - Arrival offset
  - Eight directions: North, South, East, West, North-East, North-West, South-East, South-West
  - Population
  - Elevation
- Additional variables can be added for certain temporal events corresponding to:
  - Fuel landscape
  - Weather conditions

-----

## The model formulation


The definitions are given with the "primary task" in mind. Some of the definitions are have are differ when considering "simplified task". 

- **Geo-taxonomy** 
  - A Geo taxonomy is a collection of polygons:
  - The polygons cover the geographical area of interest.
  - The mesh or grid of a Geo-taxonomy can be regular or irregular.
    - For example, square grid, each square with length 1 degree (i.e. ≈ 69 miles or 111 km).
    - Geohash with resolution 4 can be used to define a Geo-taxonomy.
- **Tile**
  - A two-dimensional (2D) polygon which is an element of a Geo-taxonomy.
- **Tile identifier (tile ID)**
  - A string that uniquely identifies a tile in a given Geo-taxonomy.
- **Tile center**
  - For a given tile $i$ the geometric center $c(i)$, of its polygon.
    - Also, $c_i$ is used.
- **Geo-taxonomy graph**
  - Undirected graph obtained by connecting the center each tile with the centers of its adjacent neighbors.
    - The polygons of two adjacent neighbor tiles have a common side.
- **Route network subgraph**
  - A Geo-taxonomy graph $GT$ can have one or many subgraphs that have edges determined by route networks mapped on $GT$.
    - Those route networks are in the geographical area covered by $GT$.
- **Geo-tile basis**
  - A set of Geo-spatial tiles each endowed with a formula based on a set of variables.
  - Each tile has the same formula, $F_{generic}$.
    - $F_{gen}$ for short, if the context allows.  
  - Each tile has its own localization of $F_{gen}$ based on the tile-localized generic variables.
- **Tile basis function**
  - For given tile ID $i$ a piecewise continuous function $b(i):\mathbb R^{2}\to\mathbb R$.
  - The function support can be the tile itself, or the tile and a certain set of neighboring tiles.
    - In other words, the basis function support can coincide with the tile, or it is larger than the tile.
  - Larger-than-the-tile support basis functions can be used to obtain smoother approximations.
- **Tile path** 
  - Primary task: An ordered set of *adjacent* tiles that correspond to a *transportation trip*.
    - The first tile contains trip's start location, the last tile contains trip's end location.
  - Simplified task: An ordered *pair* of tiles that correspond to a *transportation trip*.
- **Geo-taxonomy data**
  - Geospatial data associated with a given taxonomy.
  - For tile ID $i$:
    - $pop(i)$ : population in tile $i$ (number of people, count)
    - $elev(i)$ : average Geo-elevation in the tile $i$ (feet or meters)
    - *For now the Geo-elevation variance is not considered.*
- **Tile variables**
  - For a tile ID $i$ we define the following variables
  - $k(i)$ : a distance multiplier of the tile basis function $b(i)$
  - $n(i)$ : an intercept for $b(i)$
    - The approximation formula uses this term $k(i) \, b(i)+n(i)$; see below.
  - $sn(i)$ : starting tile offset
  - $en(i)$ : end tile offest
  - $vec(j), j \in [1,8]$ : eight Geo-direction vectors enumerated counter-clockwise, starting with the vector $(1,0)$
  - $dir(i,j), j \in [1,8]$ : multipliers for the Geo-direction vectors
  - $p(i)$ : population offset
  - $ev(i)$ : Geo-elevation offset
- **Tile path passing direction**
  - For given tile $i$ that belongs to certain tile path $p$, and it is not the last of tile of $p$, 
    the "passing direction" of $p$ over $i$ is the Geo-direction vector $vec(j)$ with the smallest 
    Cosine distance with the vector $\overrightarrow{c_{i}c_{i+1}}$. 
      - I.e., the vector connecting the center of tile $i$ with the center of tile $i+1$.
  - The index $j$ of the found passing direction of $vec(j)$ is denoted with $pass(p,i)$.
- **Tile formula**
  - For given tile $i$ its formula is:
    - $k(i) \, b(i)+n(i) + sn(i) + en(i) + p(i) \, pop(i) + ev(i) \, elev(i) + dir(i,pass(p,i))$
- **Price approximation formula** 
  - Input
    - Geo-taxonomy graph
    - Geo-coordinates of a start location $g_1$ 
    - Geo-coordinates of an end location $g_2$
  - Computation
    1. Find the tiles $t_1: g_1 \in t_1$ and $t_2: t_2 \in g_2$  
    2. Find a path $p$ from $t_1$ to $t_2$ in the Geo-taxonomy graph
       - This can be the shortest path, a or path over a subgraph (that corresponds to a route network.)
    3. Let the length of $p$ is $n$.
    4. For each tile $i$ in $p$ find the passing direction $pass(p, i)$  
    5. Here is the global formula assuming the support of each basis function $b(i)$ is the tile $i$:
  $$
    price(g_1,g_2)=\sum_{i=1}^{n}{k(i) \, b(i)+n(i) + sn(i) + en(i) + p(i) \, pop(i) + ev(i) \, elev(i) + dir(i,pass(p,i))}
  $$
- **Training data** or **training dataset**
  - A dataset of transportation trips.
  - The dataset does not need to be large -- the calibration process can run with a few transportation trips.
  - The training data can transportation trips that are with the same start- and end points but different prices.
  - The training is assumed to be "generally" consistent. I.e., there is a certain rationale behind the trips and associated prices.
- **Optimization problem**
  - An optimization problem that finds concrete values for all tile variables 
    with which that minimizes a certain metric of the difference of between the training dataset prices
    and the prices computed with the price approximation formula.
  - Several metrics of the difference can be considered:
    - Minimizing the total difference:
      - total of approximated prices vs. total of training prices
      - I.e. 1-norm, or taxicab norm, or Manhattan norm)
    - Minimizing the difference per transportation trip
      - I.e. Infinity norm, or Chebyshev distance
  - *See the next section for full mathematical details.*
- **Calibration**
  - The solving of the optimization problem with particular:
    - Geo-taxonomy
    - Geo-data
    - Training dataset

----

## The calibration optimization problem 

----

## Computation with a calibrated model
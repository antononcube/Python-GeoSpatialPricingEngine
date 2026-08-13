# Tile based approximator

## Problem formulation

- The **primary task** is to approximate a multidimensional function that: 
  - Has a codomain that is the non-negative reals (prices) 
  - Has a domain that is defined by continuous paths over a Geo-spatial route network
- The **simplified task** is to approximate a six-dimensional function:
  - The coordinates of the route points are ignored and only route distances are used
  - The function domain becomes five-dimensional: start-latitude, start-longitude, end-latitude, end-longitude, distance
- A **transportation trip** is a Geo-spatial route from a start point to an end point and associated a price.
- A set of transportation trips is used to solve the primary- and simplified tasks.
  - That set can be small or large.
  - It is expected that the trips are consistent according to a certain rationale.
    - For example, the prices can have trends or patterns corresponding to distance, direction of travel, or locations.

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
  - The polygon of a tile with identifier $i$ -- as a set of points -- is denoted as $poly(i)$ or $P(i)$.
- **Tile identifier (tile ID)**
  - A string that uniquely identifies a tile in a given Geo-taxonomy.
- **Tile center**
  - For a given tile $i$ the geometric center $c(i)$, of its polygon.
    - Also, $c_i$ is used.
- **Tile diameter**
  - For a regular tile or irregular tile $i$, the tile diameter is defined as $diam(i) = 2 \, \sqrt{area(i) / \pi}$.
  - Reasonable approximations can be used. For example, for a regular hexagon tile the diameter can be the length of any line segment that passes through its center. 
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
  - In the simplest ("standard") case $b(i)$ is $1$ on the tile $i$ and $0$ elsewhere.
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
    - $k(i) \, b(i) \, diam(i)+n(i) + sn(i) + en(i) + p(i) \, pop(i) + ev(i) \, elev(i) + dir(i,pass(p,i))$
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
    5. Assuming the support of each basis function $b(i)$ is the tile $i$ and $b(i)$ takes only the values ${0, 1}$, i.e.:
$$
b(i)(x)=
\begin{cases}
1 & \text{if }x\in poly(i),\\[4pt]
0 & \text{otherwise}.
\end{cases}
$$    
    6. Here is the approximation formula:
  $$
    price(g_1,g_2)=\sum_{i=1}^{n}{k(i) \, b(i) \, diam(i)+n(i) + sn(i) + en(i) + p(i) \, pop(i) + ev(i) \, elev(i) + dir(i,pass(p,i))}
  $$
- **Training data** or **training dataset**
  - A dataset of transportation trips.
  - The dataset does not need to be large -- the calibration process can run with a few transportation trips.
  - The training data can transportation trips that are with the same start- and end points but different prices.
  - The training is assumed to be "generally" consistent. I.e., there is a certain rationale behind the trips and associated prices.
- **Optimization problem**
  - An optimization problem that finds concrete values for all tile variables 
    that minimize a certain metric of the difference between the training dataset prices
    and the prices computed with the price approximation formula.
  - Several metrics of the difference can be considered:
    - Minimizing the total difference:
      - "total of approximated prices" vs. "total of training prices"
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

In order to calibrate the tile-based approximation model (or "mathematical artifact")
a linear optimization problem is formulated with the following steps:

1. Define a Geo-taxonomy, $GT$ with $n_{GT}$ tiles 
2. Obtain a training dataset, $TD$, with $n_D$ transportation trips
   - Each $trip(k) \in TD$ has an associated price $price(k)$. 
3. For each transportation trip $trip(k) \in TD$ apply the price approximation formula
   - Denote the expression as $formula(k)$
4. Introduce the non-negative slack variables $s^{+}(i) \ge 0, i \in [1, n_{TD}]$ and $s^{-}(i) \ge 0, i \in [1, n_{TD}]$
5. Make the constraints:

$$
expr(k) + s^{+}(k) - s^{-}(k) = price(k), k \in [1, n_{TD}]
$$
 
6. Make the objective function to be minimized -- infinity norm:

$$
\sum_{k=1}^{n_{TD}}{s^{+}(k)} + \sum_{k=1}^{n_{TD}}{s^{-}(k)}
$$

7. From the constraints make the corresponding matrix to be multiplied by the vector:

$$
(k(1), \dots, k(n_{GT}), n(1), \dots , n(n_{GT}), sn(1), \dots , sn(n_{GT}), en(1), \dots , en(n_{GT}), p(1), \dots , p(n_{GT}), ev(1), \dots , ev(n_{GT}), dir(1,1), \dots , dir(1, 8), \dots, dir(8, n_{GT}))
$$

8. From the constraints make the corresponding Right Hand Side (RHS) vector:

$$
(price(1), \dots, price(n_{GT}))
$$

### Additional constraints

The optimization problem formulation can incorporate additional constraints like:

  - $k(1) = k(i), \forall \, i \in GT$ 
    - I.e., constant distance factor for all tiles.
  - $n(1) = n(i), \forall \, i \in GT$
    - I.e., constant offset for all tiles.
  - $dir(i,j) ≤ 20, \forall \, i \in GT \land j \in [1,8]$
    - I.e., no tile is too "pivotal" in price contribution.
  - $0.1 ≤ k(i) ≤ 1.4, 0 ≤ n(i) ≤ 20, \forall \, i \in GT $ 
    - I.e., the distance factors and intercepts are restrained according to certain assumptions. 

### Modification with distance

If distance is given for each transportation trip then only $k(1)\,d(k) + n(1)$ is used in the approximation formula. 

### Modification using the uniform norm

In some cases instead of using the 1-norm (aka taxicab norm) as a minimization objective function (as in the formulation above)
it is preferred to use the max-norm (aka uniform norm or infinity norm.) 
It is attempted with the max-norm to make all deviations relatively small.
Which norm to use in concrete cases should be determined by experiments. (Like business simulations.) 

----

## Extrapolation of variables

With small training datasets not all variables are going to values changed or assigned by the calibration process.
One simple approach is to extrapolate the calibrated values of tile variables to nearest neighbor tiles. 
Such extrapolation can be (i) a simple copy of values, or (ii) assignment of values weighted by distance.

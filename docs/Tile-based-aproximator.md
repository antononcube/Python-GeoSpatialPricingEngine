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


----

## The calibration optimization problem 

----

## Computation with a calibrated model
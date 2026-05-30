# Architectural design

## Introduction

This document has architectural design elements, discussions, and related diagrams of an Object-Oriented Programming (OOP) framework
that can create, calibrate, and invoke objects that compute numerical values (prices) with Geo-spatial parameters.

----

## Definitions

- [**Well Known Text** (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) is markup language for representing vector geometry objects.
  
- **Geo-taxonomy** 
  - A Geo taxonomy is a collection of polygons:
  - The polygons cover a certain Geographical area, like, USA
  - The mesh or grid of a Geo-taxonomy can be regular or irregular
    - For example, square grid, each square with length 1 degree (i.e. ≈ 69 miles or 111 km)
    - Geohash with resolution 4 can be used to define a Geo-taxonomy
  - Geo-taxonomy can be completely specified as a table each row of which specifies a tile
  - The table has the columns:
    - Tile ID 
    - Latitude of tile's center
    - Longitude of tile's center
    - WKT of the polygon that is the tile
- **Design pattern**
  - One of the Gang of Four (GoF) patterns for micro-architectural sofware design.
  - See [Design patterns](https://en.wikipedia.org/wiki/Design_Patterns).
  - The OOP framework specified below is based on Template Method, Strategy, Composite, Decorator, and Builder.
- **Nearest neighbor graph of the Geo-taxonomy**
  - The graph in which every tile is connected to the tiles with which it has a common side.
- **Order**
  - An order has start, end, price, and an optional distance
  - A collection of orders can be specified as a table with the columns:
    - StartLat
    - StartLon
    - EndLat
    - EndLong
    - Distance
    - Price
- **Pricing strategy**
  - A mathematical artifact that for every ordered pair of two Geo-points gives a number (that is a price.)
  - The pricing strategy is static in time:
    - It is only dependent five parameters:
      - Two Geo-spatial points
      - Optionally given distance
  - The pricing strategy function $p$ can be invoked with: 
    - Five numbers as arguments: $p(lat1, lon1, lat2, lon2, d)$
    - Two Geo-points and a number: $p(g_1, g_2, d)$
  - The last, distance argument in both signatures can be skipped
- **Pricing policy**
  - A pricing policy is a collection of pricing strategies that has dependencies on additional parameters, like:
    - Time (hour of the day, or week of the year, etc.)
    - Type of goods, transporters (companies, people), or transporting vehicles
    - Service tier, level, or grade ("smart", "premium", etc.)
- **Pricing engine**
  - A software framework that can be used to create, calibrate, and invoke pricing strategies.

----

## Software architectural design

### Classes
 
- `Point2D` 
  - Has `(x, y)` coordinates
  - Can compute:
    - norm
    - dot product with
      - other `Point2D` object
      - with `(x2, y2)` pair
    - distance to other point
- `GeoPoint`
  - Inherits from `Point2D`
  - Has an `id`
  - Has a gist (`__str__`) the includes the ID and coordinates
  - Can compute distance in miles and kilometers
    - I.e. convert from Earth radians to miles and kilometers
- `Geo-taxonomy`
  - Can read/import a Geo-taxonomy given in different formats:
    - CSV
    - JSON 
    - JSON (that is pandas data frame)
- `TiledRegion`
  - Abstract class
  - Has a Geo-taxonomy
  - Has methods to find the tile for a given 
    - `GeoPoint`
    - Geo-point given with `(x, y)` coordinates
  - Has abstract methods for finding tile paths between:
    - Two `GeoPoint` objects
    - Two Geo-points gives as `(x1, y1, x2, y2)` arguments
- `TiledRegionTrivial`
  - Inherits `TiledRegion` 
  - All tile paths are just the start tile and end tile.
    - For example, for the Geo-points `(x1, y1)` and `(x2, y2)` the tile path is `[self.tile(x1, y1), self.tile(x2, y2)]` 
- `TiledRegionGraph`
  - Use two graphs of tiles in order to find tile paths.
    - The first, coarse graph corresponds to a network of highways or/and primary roads
    - The second, fine graph corresponds to the nearest neighbor graph of the Geo-taxonomy
  - If the coarse graph is not given only the fine graph is used.
- `Orders`
  - Abstract class for the ingestion of collection of orders and transforming them in convenient computational data structures. 
  - The descendants of the class know how to ingest CSV or JSON files, or retrieve orders from databases.
  - Its hierarchy uses both Template Method and Strategy.
- `PricingEngine`
  - Central class of the framework.
  - Each instance of the class is a "pricing strategy".
  - Has methods to compute prices via different signatures.
- `PricingEngineCalibrator`
  - Calibrates a pricing strategy with a set of orders.
  - The class has attributes that are instances of `Orders`, `TiledRegsion`, and `PricingEngine`.
  - Uses Google OR-Tools to formulate and solve the optimizational problem that corresponds to the calibration process.
- `PricingEngineExtrapolator`
  - A class that corresponds to a certain type of post-processing of calibrated pricing strategies.
- `PricingEngineBuilder`
  - Uses JSON dictionary-like specification to create and calibrate a `PricingEngine` object.
  - The building steps include:
    - Retrieval of Geo-taxonomy
    - Ingestion of orders
    - Calibration of a pricing strategy
    - Post-processing
  - The retrieval and ingestion steps can involve reading files or accessing databases. 


----

## Diagram

```mermaid

```
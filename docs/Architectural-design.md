# Architectural design

## Introduction

This document has architectural design elements, discussions, and related diagrams.

----

## Design

### Definitions

- [**Well Known Text** (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) is markup language for representing vector geometry objects.
  
- A **Geo-taxonomy** is collection of polygons:
  - The polygons cover a certain Geo area, like, USA
  - The mesh or grid of Geo-taxonomy can be regular or irregular
    - For example, square grid, each square with length 1 degree (i.e. ≈ 69 miles or 111 km)
    - Geohash with resolution 4 can be used to define a Geo-taxonomy
  - Geo-taxonomy can be completely specified as table with columns:
    - Tile ID 
    - Latitude of tile's center
    - Longitude of tile's center
    - WKT of the polygon that is the tile
- **Nearest neighbor graph of the Geo-taxonomy**
  - The graph in which every tile is connected to the tiles with which it has a common side.

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

----

## Diagram

```mermaid

```
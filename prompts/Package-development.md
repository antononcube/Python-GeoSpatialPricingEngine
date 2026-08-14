# Package development prompts

----

## First version

The first versions of the files in the package directory ["../GeoSpatialPricingEngine"](../GeoSpatialPricingEngine) were
created using OpenAI's "gpt-5.6-luna" with the prompt:

```text
Analyze the document "./docs/Architectural-design.md" and implement the Python package "GeoSpatialPricingEngine" in this directory. 
Each class should have its own file. Implement the class attributes, setters, and getters, but do not implement the "serious", functionality methods. 
(I will direct their implementation later on.)
```

----

## Separate PostgreSQL class

````text
Implement a generic PostgreSQL access class:
  - Encapsulates the PostgreSQL database access
  - Imports data to data frames
  - Importers like `geo_taxonomy` and `orders` provide new column names if renaming of the database columns is needed 

Use the (newer, recommended) modern "psycopg" ("psycopg3") package.

The class creator should take as an argument the dictionary:  

```python
DB_CONFIG = {
    'dbname': 'geo_spatial_pricing_engine',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}
```

There should be attributes and setters and getters for each of the keys in `DB_CONFIG`.
````

````text
Make tests for the created `PostgreSQLAccess` class in "GeoSpatialPricingEngine/postgresql_access.py" that accesses
the database with:

```python
DB_CONFIG = {
    'dbname': 'geo_spatial_pricing_engine',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}
```

and checks that:

1. The ingestion of the table `geo_taxonomy` with the SQL query:

```sql
SELECT * FROM geo_taxonomy WHERE geo_taxonomy_id = 'Hextile1deg' 
```

produces a data frame with more than 1000 rows and columns: 'id', 'geo_taxonomy_id', 'tile_id', 'center_lat', 'center_lon', 'coordinates'.

2. The ingestion of the table `transportation_trips` with the SQL query

```sql
SELECT * FROM raw_transportation_trips WHERE raw_transportation_trips_id = 'FAFDerived'
```

produces a data frame with more than 4000 rows and columns: 'id', 'raw_transportation_trips_id', 'start_lat', 'start_lon',
       'start_state', 'start_city', 'start_zip_code', 'end_lat', 'end_lon',
       'end_state', 'end_city', 'end_zip_code', 'distance', 'price'.
````

----

## Geo-points handling classes

```text
Fully implement the classes `Point2D` and `GeoPoint` -- see the section "Classes" in the document "./docs/Architectural-design.md".
```

----

## Geo-taxonomy class

### Importing from SQL

````text
In the class `GeoTaxonomy` in './GeoSpatialPricingEngine/geo_taxonomy.py', 
using the class `PostgreSQLAccess` in './GeoSpatialPricingEngine/postgresql_access.py',
implement the method `read_sql` for the database import of a Geo-taxonomy for a specified `geo_taxonomy_id`. 

The ingestion from the database table `geo_taxonomy` is with the SQL query:

```sql
SELECT * FROM geo_taxonomy WHERE geo_taxonomy_id = 'Hextile1deg' 
```

The produced data frame is with the columns: 'id', 'geo_taxonomy_id', 'tile_id', 'center_lat', 'center_lon', 'coordinates',
The corresponding column types are: string, string, string, number, number, JSON-string.

The 'coordinates' column should have JSON array strings -- convert them to Python arrays.
````

#### Additional changes

```text
Make the method read_sql of the class GeoTaxonomy to use the argument "connection" -- which I just added.
```

```text
When I run the test I get the error:
>       if isinstance(connection, PostgreSQLAccess):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> E       TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```

----

## Transportation trips

### Importing from SQL

````text
In the class `Orders` in './GeoSpatialPricingEngine/orders.py', 
using the class `PostgreSQLAccess` in './GeoSpatialPricingEngine/postgresql_access.py',
implement the method `ingest_db` for the database import of a transportation trips for a specified `transportation_trips_id`. 

The ingestion from the database table `transportation_trips` is with the SQL query:

```sql
SELECT * FROM transportation_trips WHERE transportation_trips_id = 'FAFDerivedLinear' 
```

The produced data frame is with the columns: 'id', 'transportation_trips_id', 'start_lat', 'start_lon', 'end_lat', 'end_lon', 'distance', 'price', 'is_training',
The corresponding column types are: string, string, number, number, number, number, number, number, boolean.
````

#### Additional changes

After applying the prompts in "Geo-taxonomy class / Importing from SQL / Additional changes":

```text
Change the method ingest_db of Orders in the same way. I am getting similar / same error when I run "test_order.py".
```

```text
When I run "test_orders.py" I getting the error: 
> Expected :True
> Actual   :np.True_
```

----

## Pricing Engine builder

### Calibration JSON spec

```text
Create a JSON specification form that is a JSON dictionary to create and calibrate a `PricingEngine` object,
and put in the directory "./resources".

The building steps include:
- PostgreSQL database access elements 
- Retrieval of Geo-taxonomy: Geo-taxonomy ID
- Ingestion of orders: transportation orders ID
- Whether to split the data in training & testing parts
    - Assuming the transportation orders have the column 'is_training'
- Calibration of a pricing strategy
    - min & max of multiplication factor `k`
    - min & max of global offset `n`
    - min & max of start-location offset `sn`
    - min & max of start-location offset `sn`
    - min & max of end-location offset `en`
    - min & max of population offset `p`
    - min & max of elevation offset `ev`
    - max of directional variables `dir`
- Post-processing
    - Whether to use extrapolation or not
    - Extrapolation method
    - Number of nearest neighbors for the extrapolation method "nearest-neighbors"
```

#### Review & change

After the generation of the JSON spec with the prompt above:

```text
Good. Analyze the file "./docs/Tile-based-aproximator.md" -- do you think other elements to the JSON calibration spec should be added? 
```


> Great prompt — I’ll read that design doc and map any missing JSON spec elements to concrete keys.
>
> Yes — based on `../docs/Tile-based-approximator.md`, I’d add several important spec fields.
>
> **Recommended Additions**
> - Add all 8 directional coefficients (not only a single cap): `N,S,E,W,NE,NW,SE,SW` bounds, since directions are explicit in the model (`docs/Tile-based-aproximator.md:30`, `docs/Tile-based-aproximator.md:181`).
> - Add optimization objective selection: `objective_norm: "l1" | "linf"` (`docs/Tile-based-aproximator.md:140`, `docs/Tile-based-aproximator.md:207`).
> - Add constraint toggles for “shared across all tiles” variables, e.g. `k_constant_across_tiles`, `n_constant_across_tiles` (`docs/Tile-based-aproximator.md:194`).
> - Add model mode: `task_mode: "primary" | "simplified"` and `distance_only_formula` option (`docs/Tile-based-aproximator.md:8`, `docs/Tile-based-aproximator.md:205`).
> - Add route/path policy: `path_strategy` (e.g., shortest-path vs route-subgraph) (`docs/Tile-based-aproximator.md:65`, `docs/Tile-based-aproximator.md:118`).
> - Add basis-function configuration: support type (`tile_only` vs neighbors) and neighbor radius (`docs/Tile-based-aproximator.md:73`).
>
> **Post-processing Additions**
> - Add `extrapolate_variables` list (which coefficients are extrapolated), since extrapolation is described per variable (`docs/Tile-based-aproximator.md:216`).
> - Add extrapolation subtype for nearest neighbors: `"copy"` vs `"distance_weighted"` (`docs/Tile-based-aproximator.md:220`).
>
> If you want, I can now update `../GeoSpatialPricingEngine/resources/PricingEngineSpecForm.json` with these fields (keeping your current schema backward-compatible).


### Ingestion of the JSON calibration spec

```text
Implement the ingestion of the JSON calibration spec in the class PricingEngineBuilder in "./GeoSpatialPricingEngine/pricing_engine_builder.py". 
The spec ingestion method should take a file path. 
Check does the file exist, and can be JSON parsed.
```

----

## Tiled region 

### Tile mapper method

A Template Method for the mapping of Geo-positions to Geo-taxonomy tiles.

````text
For the class `TiledRegion` in "./GeoSpatialPricingEngine/tiled_region.py" implement a Template Method method that maps Geo-positions to Geo-taxonomy tile IDs.
Here is how to use the package "GeometricNearestNeighborsProcessor" is used to make a mapping object: 

```python
from GeometricNearestNeighborsProcessor import *
aTileCenters={rec["tile_id"]: (rec["center_lat"], rec["center_lon"]) for rec in dfTaxonomy.to_dict(orient="records")}
gnnObj=GeometricNearestNeighborsProcessor(aTileCenters)
``` 

Here is how the tile of a given point is found:

```python
gnnObj.find_nearest(point=(rec["lat"], rec["lon"]), n=1).take_value()["ID"][0]
```
````

### Trivial paths


````text
Implement the methods `find_path` and `find_path_for_coords` of the class `TiledRegionTrivial` using the `TiledRegion`
method `tile_for_coords` and `tile_for_point`.

The trivial path is an array of exactly two strings each of which is a tile ID. For example

```python
['tile01012', 'tile00851']
```
````

### Calibration records

````text
Implement the method `to_calibration_records` in `TiledRegion` that converts an `Orders` object 
into a dictionary of dictionaries witt the form:

```python
{
'5': {
    'id': 5,
    'path': ['tile01012', 'tile00851'],
    'distance': 1004.7,
    'price': 394
   },
'6': {
    'id': 6,
    'path': ['tile01012', 'tile00556'],
    'distance': 1835.9,
    'price': 503
   },   
  ...
]
```

As it can be seen in "./GeoSpatialPricingEngine/postgresql_access.py" the data attribute of `Orders` 
is a data frame with columns: "id", "start_lat", "start_lon", "end_lat", "end_lon", "distance", "price".

Make tests using `TiledRegionTrivial`.
````

---

## Pricing engine builder

### Building from JSON (first)

```text
In the method `PricingEngineBuilder.build_from_json` implement the steps:
- Reading the JSON spec file
- Ingesting the specified Geo-taxonomy
- Ingesting the specified transportation orders data
- Mapping the transportation orders to Geo-tiles
    - If the specified "model.path_strategy" is different than "trivial-path" give an error message.
    - Otherwise use `TiledRegion.to_calibration_records` to do the mapping with an instance of `TiledRegionTrivial`. 
```

---

## Package building

```text
Add "setup.py" file in order to install packages.
```

```text
Add URL placeholder.
```

```text
Make the sure the resource package "./resources/PricingEngineCalibrationSpec.json" is accessible when the package is loaded with from GeoSpatialPricingEngine import *.
```

---

## Pricing engine calibrator

```text
Carefully analyze the theoretical model description in the file "./docs/Tile-based-approximator.md" and implement
the corresponding calibration steps in the class `PricingEngineCalibrator`. 

Use Google OR-Tools for the Linear Programming (LP)
implementation. See how the JSON file calibration specification is utilized in the Jupyter notebook "./notebooks/Jupyter/Pricing-engine-calibration.ipynb".
The notebook shows the data frames and data structures that are used in `PricingEngineCalibrator`.

Make the calibration implementation coherent -- set the required attributes `PricingEngineCalibrator` in `PricingEngineBuilder.build_from_json`
and trigger the calibration from ``PricingEngineCalibrator.build_from_json`.
```

After reviewing the first implementation:

```text
In the class `GeoTaxonomy` add the attribute `_tile_diameter` with default value `None` and corresponding setter and getter methods. 
Implement in `GeoTaxonomy` the method `tile_area` that finds polygon area from its coordinates. 
In the calibration implementation if the tile diameter is a number (or not `None`) use it for all tiles; if it is `None` use `tile_area` per tile.
```
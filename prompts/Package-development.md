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
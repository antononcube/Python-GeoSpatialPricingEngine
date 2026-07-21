# Package development prompts

## First version

The first versions of the files in the package directory ["../GeoSpatialPricingEngine"](../GeoSpatialPricingEngine) were
created using OpenAI's "gpt-5.6-luna" with the prompt:

```text
Analyze the document "./docs/Architectural-design.md" and implement the Python package "GeoSpatialPricingEngine" in this directory. 
Each class should have its own file. Implement the class attributes, setters, and getters, but do not implement the "serious", functionality methods. 
(I will direct their implementation later on.)
```

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
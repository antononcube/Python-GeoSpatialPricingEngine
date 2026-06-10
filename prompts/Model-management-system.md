# Model Management System (MMS)

## Generation prompt

Generate the tables of a Model Management System (MMS) that is in PostgreSQL with tables for:
- Geo-taxonomies
- Model calibration parameters
- Model 
- Experiments 
- Experimental results

Many models can be trained over the same transportation data using different parameters or Geo-taxonomies.
 
Use the Star schema design pattern, the central table is `model`. Here are all tables:

- `model`
  - Model identifier (ID)
  - Connections to the tables used to create and calibrate the model:
    - `model_parameter` : one to many
    - `geo_taxonomy` : one to one for model_id vs geo_taxonomy_id 
    - `tile_data` : one to one for model_id vs tile_data_id
    - `transportation_trips` : one to one for model_id vs transportation_trips_id
    - `calibrated_value` : one to many for model_id vs id
- `model_parameter`
  - Parameter id, name, description, min-, and max value
- `calibrated_value`
  - Has all tile variable names and the calibrated values assigned to them
- `geo_taxonomy`
  - Has Geo-taxonomy ID, tile IDs, tile coordinates as JSON string, latitude and longitude of tiles' centers
- `tile_data`
  - For each tile of a given Geo-taxonomy there is a set of numerical data variables, like, elevation and population.
  - Connects to `geo_taxonomy` 
    - One to one fo geo_taxonomy_id vs tile_data_id
  - Columns:
    - tile_data_id 
    - geo_taxonomy_id
    - id
    - tile_id
    - name
    - value
- `transportation_trips`
  - Connects to `model` (many to many)
  - Connects to `raw_transportation_trips` (many-to-one)
    - One-to-one for transportation_trips_id vs raw_transportation_trips_id
  - Preprocessed raw data used for model calibration.
  - Has an indicator column, `is_trianing`, for which records are for training and which for testing
  - Columns:
    - transportation_trips_id
    - raw_transportation_trips_id
    - id
    - start_lat
    - start_lon
    - end_lat
    - end_lon
    - distance (can be null)
    - price
    - is_training
- `raw_transportation_trips`
  - Columns:
    - raw_transportation_trips_id
    - id
    - start_lat
    - start_lon
    - start_state
    - start_zip_code
    - end_lat
    - end_lon
    - end_state
    - end_zip_code
    - distance (can be null)
    - price

Generate the SQL code for the creation of the tables and their indexes.
Chose reasonable column names and types make their names consistent.

**Remark:** Maybe, the Mermaid-JS code should be generated first, and then the SQL.
The Mermaid-Code can be used to tweak/tune the design. 

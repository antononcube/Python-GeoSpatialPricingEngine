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
  - model_id    (primary key)
  - model_name  (textual, cannot be null, unique)
  - description (textual, can be null) 
  - Connections to the tables used to create and calibrate the model:
    - `model_parameter` : one to many
    - `geo_taxonomy` : one to one for model_id vs geo_taxonomy_id 
    - `tile_data` : one to one for model_id vs tile_data_id
    - `transportation_trips` : one to one for model_id vs transportation_trips_id
    - `calibrated_value` : one to many for model_id vs id
- `model_parameter`
  - id             (primary key)
  - model_id       (not unique)
  - parameter_name (textual, cannot be null, not unique)
  - min_value
  - max_value
- `calibrated_value`
  - Has all tile variable names and the calibrated values assigned to them
  - id              (primary key)
  - model_id        (cannot be null, not unique)
  - variable_name
  - value
- `geo_taxonomy`
  - id              (primary key)
  - geo_taxonomy_id (textual, cannot be null, not unique)
  - tile_id         (textual, cannot be null, not unique)
  - center_lat
  - center_lon
  - coordinates     (tile polygon coordinates as a JSON string)
- `tile_data`
  - For each tile of a given Geo-taxonomy there is a set of numerical data variables, like, elevation and population.
  - Connects to `geo_taxonomy` 
    - One to one fo geo_taxonomy_id vs tile_data_id
  - One-to-one relationship between the values of `geo_taxonomy_id` and `tile_data_id`
  - Columns:
    - tile_data_id      (textual, cannot be null, not unique)
    - geo_taxonomy_id   (textual, cannot be null, not unique)
    - id                (primary key)
    - tile_id           (textual, cannot be null)
    - name
    - value
- `transportation_trips`
  - Connects to `model` (many to many)
  - Connects to `raw_transportation_trips` (many-to-one)
    - One-to-one for transportation_trips_id vs raw_transportation_trips_id
  - Preprocessed raw data used for model calibration.
  - Has an indicator column, `is_trianing`, for which records are for training and which for testing
  - One-to-one relationship between the values of `transportation_trips_id` and `raw_transportation_trips_id`
  - Columns:
    - transportation_trips_id       (textual, cannot be null, not unique)
    - raw_transportation_trips_id   (textual, can be null, not unique)
    - id                            (primary key)
    - start_lat
    - start_lon
    - end_lat
    - end_lon
    - distance (can be null)
    - price
    - is_training
- `raw_transportation_trips`
  - Columns:
    - raw_transportation_trips_id  (textual, cannot be null, not unique)
    - id             (primary key)
    - start_lat      (numeric, cannot be null)
    - start_lon      (numeric, cannot be null)
    - start_state    (string, can be null)
    - start_city     (string, can be null)
    - start_zip_code (string, can be null)
    - end_lat        (numeric, cannot be null) 
    - end_lon        (numeric, cannot be null) 
    - end_state      (string, can be null)
    - end_city       (string, can be null)
    - end_zip_code   (string, can be null)
    - distance       (numeric, can be null)
    - price          (numeric, cannot be null) 

Generate the SQL code for the creation of the tables and their indexes.
Chose reasonable column names and types make their names consistent.


-----

## Meta comments & prompts

**Remark:** Maybe, the Mermaid-JS code should be generated first, and then the SQL.
The Mermaid-Code can be used to tweak/tune the design. 

**Codex prompt:** Carefully read "./prompts/Model-management-system.md" and generate the corresponding SQL script for creating the PostgreSQL tables in the directory "./sql".
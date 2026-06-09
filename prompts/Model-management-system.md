# Model Management System (MMS)

## Generation prompt

Generate the tables of a Model Management System (MMS) that is in PostgreSQL with tables for:
- Geo-taxonomies
- Model calibration parameters
- Model 
- Experiments 
- Experimental results

Many models can be trained over the same transportation data using different parameters or Geo-taxonomies.
 
Use the Star schema design the central table is `model`. Here are all tables:

- `model`
  - Model identifier (ID)
  - Connections to the tables used to create and calibrate the model:
    - `model_parameter`
    - `geo_taxonomy`
    - `tile_data`
    - `transportation_trips`
    - `calibrated_value`
- `model_parameter`
  - Connects to `model` id (one to many
  - Parameter id, name, description, min-, and max value
- `calibrated_value`
  - Connects to `model`
  - Has all tile variable names and the calibrated values assigned to them
- `geo_taxonomy`
  - Connects to `model`
  - Has Geo-taxonomy ID, tile IDs, tile coordinates as JSON string, latitude and longitude of tiles' centers
- `tile_data`
  - For each tile of a given Geo-taxonomy there is 
- `transportation_trips`
  - Connects to `model`
  - Preprocessed raw data used for model calibration. 
- `raw_transportation_trips`
  - Connects to `transportation_trips`

Generate the SQL code for the creation of the tables and their indexes.
Chose reasonable column names and types make their names consistent.

**Remark:** Maybe, the Mermaid-JS code should be generated first, and then the SQL.
The Mermaid-Code can be used to tweak/tune the design. 

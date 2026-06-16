BEGIN;

-- Model Management System (MMS) schema

CREATE TABLE IF NOT EXISTS raw_transportation_trips (
    id BIGSERIAL PRIMARY KEY,
    raw_transportation_trips_id TEXT NOT NULL,
    start_lat NUMERIC(10,7) NOT NULL,
    start_lon NUMERIC(10,7) NOT NULL,
    start_state TEXT,
    start_city TEXT,
    start_zip_code TEXT,
    end_lat NUMERIC(10,7) NOT NULL,
    end_lon NUMERIC(10,7) NOT NULL,
    end_state TEXT,
    end_city TEXT,
    end_zip_code TEXT,
    distance NUMERIC(12,4),
    price NUMERIC(12,4) NOT NULL
);

CREATE TABLE IF NOT EXISTS geo_taxonomy (
    id BIGSERIAL PRIMARY KEY,
    geo_taxonomy_id TEXT NOT NULL,
    tile_id TEXT NOT NULL,
    center_lat NUMERIC(10,7),
    center_lon NUMERIC(10,7),
    coordinates JSONB
);

CREATE TABLE IF NOT EXISTS transportation_trips (
    id BIGSERIAL PRIMARY KEY,
    transportation_trips_id TEXT NOT NULL,
    raw_transportation_trips_id TEXT,
    start_lat NUMERIC(10,7),
    start_lon NUMERIC(10,7),
    end_lat NUMERIC(10,7),
    end_lon NUMERIC(10,7),
    distance NUMERIC(12,4),
    price NUMERIC(12,4),
    is_training BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS tile_data (
    id BIGSERIAL PRIMARY KEY,
    tile_data_id TEXT NOT NULL,
    geo_taxonomy_id TEXT NOT NULL,
    tile_id TEXT NOT NULL,
    name TEXT,
    value NUMERIC
);

CREATE TABLE IF NOT EXISTS model (
    model_id BIGSERIAL PRIMARY KEY,
    model_name TEXT NOT NULL UNIQUE,
    description TEXT,
    geo_taxonomy_id TEXT NOT NULL,
    tile_data_id TEXT NOT NULL,
    transportation_trips_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_parameter (
    model_parameter_id TEXT NOT NULL,
    id BIGSERIAL PRIMARY KEY,
    model_id BIGINT NOT NULL,
    parameter_name TEXT NOT NULL,
    min_value NUMERIC,
    max_value NUMERIC,
    CONSTRAINT fk_model_parameter_model_id
        FOREIGN KEY (model_id)
        REFERENCES model (model_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS calibrated_value (
    id BIGSERIAL PRIMARY KEY,
    model_id BIGINT NOT NULL,
    variable_name TEXT,
    value NUMERIC,
    CONSTRAINT fk_calibrated_value_model_id
        FOREIGN KEY (model_id)
        REFERENCES model (model_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experiment (
    id BIGSERIAL PRIMARY KEY,
    model_id BIGINT NOT NULL,
    experiment_name TEXT NOT NULL,
    description TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    status TEXT,
    CONSTRAINT fk_experiment_model_id
        FOREIGN KEY (model_id)
        REFERENCES model (model_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experimental_result (
    id BIGSERIAL PRIMARY KEY,
    experiment_id BIGINT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC NOT NULL,
    notes TEXT,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_experimental_result_experiment_id
        FOREIGN KEY (experiment_id)
        REFERENCES experiment (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Indexes for common joins and filtering

CREATE INDEX IF NOT EXISTS idx_raw_transportation_trips_raw_id
    ON raw_transportation_trips (raw_transportation_trips_id);

CREATE INDEX IF NOT EXISTS idx_geo_taxonomy_geo_taxonomy_id
    ON geo_taxonomy (geo_taxonomy_id);

CREATE INDEX IF NOT EXISTS idx_geo_taxonomy_tile_id
    ON geo_taxonomy (tile_id);

CREATE INDEX IF NOT EXISTS idx_transportation_trips_trips_id
    ON transportation_trips (transportation_trips_id);

CREATE INDEX IF NOT EXISTS idx_transportation_trips_raw_id
    ON transportation_trips (raw_transportation_trips_id);

CREATE INDEX IF NOT EXISTS idx_transportation_trips_is_training
    ON transportation_trips (is_training);

CREATE INDEX IF NOT EXISTS idx_tile_data_tile_data_id
    ON tile_data (tile_data_id);

CREATE INDEX IF NOT EXISTS idx_tile_data_geo_taxonomy_id
    ON tile_data (geo_taxonomy_id);

CREATE INDEX IF NOT EXISTS idx_tile_data_tile_id
    ON tile_data (tile_id);

CREATE INDEX IF NOT EXISTS idx_model_parameter_model_id
    ON model_parameter (model_id);

CREATE INDEX IF NOT EXISTS idx_model_parameter_parameter_name
    ON model_parameter (parameter_name);

CREATE INDEX IF NOT EXISTS idx_calibrated_value_model_id
    ON calibrated_value (model_id);

CREATE INDEX IF NOT EXISTS idx_calibrated_value_variable_name
    ON calibrated_value (variable_name);

CREATE INDEX IF NOT EXISTS idx_experiment_model_id
    ON experiment (model_id);

CREATE INDEX IF NOT EXISTS idx_experiment_started_at
    ON experiment (started_at);

CREATE INDEX IF NOT EXISTS idx_experimental_result_experiment_id
    ON experimental_result (experiment_id);

CREATE INDEX IF NOT EXISTS idx_experimental_result_metric_name
    ON experimental_result (metric_name);

COMMIT;

BEGIN;

CREATE TABLE IF NOT EXISTS geo_taxonomy (
    geo_taxonomy_id BIGSERIAL PRIMARY KEY,
    taxonomy_name TEXT NOT NULL,
    tile_id TEXT NOT NULL,
    tile_coordinates_json JSONB NOT NULL,
    center_lat NUMERIC(10, 7) NOT NULL,
    center_lon NUMERIC(10, 7) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (taxonomy_name, tile_id)
);

CREATE TABLE IF NOT EXISTS raw_transportation_trips (
    raw_transportation_trips_id BIGSERIAL PRIMARY KEY,
    id BIGINT NOT NULL,
    start_lat NUMERIC(10, 7) NOT NULL,
    start_lon NUMERIC(10, 7) NOT NULL,
    start_state TEXT NULL,
    start_city TEXT NULL,
    start_zip_code TEXT NULL,
    end_lat NUMERIC(10, 7) NOT NULL,
    end_lon NUMERIC(10, 7) NOT NULL,
    end_state TEXT NULL,
    end_city TEXT NULL,
    end_zip_code TEXT NULL,
    distance NUMERIC(12, 4) NULL,
    price NUMERIC(12, 4) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS transportation_trips (
    transportation_trips_id BIGSERIAL PRIMARY KEY,
    raw_transportation_trips_id BIGINT NOT NULL UNIQUE,
    id BIGINT NOT NULL,
    start_lat NUMERIC(10, 7) NOT NULL,
    start_lon NUMERIC(10, 7) NOT NULL,
    end_lat NUMERIC(10, 7) NOT NULL,
    end_lon NUMERIC(10, 7) NOT NULL,
    distance NUMERIC(12, 4) NULL,
    price NUMERIC(12, 4) NOT NULL,
    is_training BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_transportation_trips_raw
        FOREIGN KEY (raw_transportation_trips_id)
        REFERENCES raw_transportation_trips (raw_transportation_trips_id),
    UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS tile_data (
    id BIGSERIAL PRIMARY KEY,
    tile_data_id BIGINT NOT NULL,
    geo_taxonomy_id BIGINT NOT NULL,
    tile_id TEXT NOT NULL,
    name TEXT NOT NULL,
    value NUMERIC(18, 6) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_tile_data_geo_taxonomy
        FOREIGN KEY (geo_taxonomy_id)
        REFERENCES geo_taxonomy (geo_taxonomy_id),
    UNIQUE (tile_data_id, tile_id, name),
    UNIQUE (tile_data_id, geo_taxonomy_id)
);

CREATE TABLE IF NOT EXISTS model (
    model_id BIGSERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NULL,
    model_description TEXT NULL,
    geo_taxonomy_id BIGINT NOT NULL UNIQUE,
    tile_data_id BIGINT NOT NULL UNIQUE,
    transportation_trips_id BIGINT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_model_geo_taxonomy
        FOREIGN KEY (geo_taxonomy_id)
        REFERENCES geo_taxonomy (geo_taxonomy_id),
    CONSTRAINT fk_model_transportation_trips
        FOREIGN KEY (transportation_trips_id)
        REFERENCES transportation_trips (transportation_trips_id),
    CONSTRAINT fk_model_tile_data
        FOREIGN KEY (tile_data_id, geo_taxonomy_id)
        REFERENCES tile_data (tile_data_id, geo_taxonomy_id),
    UNIQUE (model_name, model_version)
);

CREATE TABLE IF NOT EXISTS model_parameter (
    parameter_id BIGSERIAL PRIMARY KEY,
    model_id BIGINT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_description TEXT NULL,
    min_value NUMERIC(18, 6) NULL,
    max_value NUMERIC(18, 6) NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_model_parameter_model
        FOREIGN KEY (model_id)
        REFERENCES model (model_id),
    CHECK (min_value IS NULL OR max_value IS NULL OR min_value <= max_value),
    UNIQUE (model_id, parameter_name)
);

CREATE TABLE IF NOT EXISTS calibrated_value (
    calibrated_value_id BIGSERIAL PRIMARY KEY,
    model_id BIGINT NOT NULL,
    variable_name TEXT NOT NULL,
    calibrated_value NUMERIC(18, 8) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_calibrated_value_model
        FOREIGN KEY (model_id)
        REFERENCES model (model_id),
    UNIQUE (model_id, variable_name)
);

CREATE TABLE IF NOT EXISTS experiment (
    experiment_id BIGSERIAL PRIMARY KEY,
    model_id BIGINT NOT NULL,
    experiment_name TEXT NOT NULL,
    experiment_description TEXT NULL,
    started_at TIMESTAMPTZ NULL,
    completed_at TIMESTAMPTZ NULL,
    status TEXT NOT NULL DEFAULT 'planned',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_experiment_model
        FOREIGN KEY (model_id)
        REFERENCES model (model_id),
    CHECK (completed_at IS NULL OR started_at IS NULL OR completed_at >= started_at),
    CHECK (status IN ('planned', 'running', 'completed', 'failed')),
    UNIQUE (model_id, experiment_name)
);

CREATE TABLE IF NOT EXISTS experimental_result (
    experimental_result_id BIGSERIAL PRIMARY KEY,
    experiment_id BIGINT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value NUMERIC(18, 8) NOT NULL,
    metric_unit TEXT NULL,
    split_type TEXT NULL,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_experimental_result_experiment
        FOREIGN KEY (experiment_id)
        REFERENCES experiment (experiment_id),
    CHECK (split_type IS NULL OR split_type IN ('train', 'validation', 'test')),
    UNIQUE (experiment_id, metric_name, split_type)
);

CREATE INDEX IF NOT EXISTS idx_geo_taxonomy_tile_id
    ON geo_taxonomy (tile_id);

CREATE INDEX IF NOT EXISTS idx_geo_taxonomy_center
    ON geo_taxonomy (center_lat, center_lon);

CREATE INDEX IF NOT EXISTS idx_raw_trips_start_coords
    ON raw_transportation_trips (start_lat, start_lon);

CREATE INDEX IF NOT EXISTS idx_raw_trips_end_coords
    ON raw_transportation_trips (end_lat, end_lon);

CREATE INDEX IF NOT EXISTS idx_transportation_trips_training
    ON transportation_trips (is_training);

CREATE INDEX IF NOT EXISTS idx_transportation_trips_id
    ON transportation_trips (id);

CREATE INDEX IF NOT EXISTS idx_tile_data_lookup
    ON tile_data (geo_taxonomy_id, tile_id, name);

CREATE INDEX IF NOT EXISTS idx_model_parameter_model
    ON model_parameter (model_id);

CREATE INDEX IF NOT EXISTS idx_calibrated_value_model
    ON calibrated_value (model_id);

CREATE INDEX IF NOT EXISTS idx_experiment_model_status
    ON experiment (model_id, status);

CREATE INDEX IF NOT EXISTS idx_experimental_result_experiment
    ON experimental_result (experiment_id);

COMMIT;

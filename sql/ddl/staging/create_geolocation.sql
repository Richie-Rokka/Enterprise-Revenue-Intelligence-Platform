/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_geolocation.sql

Purpose:
    Creates the enterprise geolocation staging table.

Description:
    Stores raw geolocation reference records exactly as received from the
    source system. This table provides geographic lookup information used
    during downstream transformations.

Schema:
    staging

Dependencies:
    - create_schemas.sql
    - create_reference_tables.sql
    - seed_reference_data.sql

Execution Stage:
    Staging Layer

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.0.0
===============================================================================
*/

-- =============================================================================
-- GEOLOCATION STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.geolocation
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_geolocation_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    geolocation_zip_code_prefix INTEGER NOT NULL,

    geolocation_lat NUMERIC(10,7) NOT NULL,

    geolocation_lng NUMERIC(10,7) NOT NULL,

    geolocation_city VARCHAR(100),

    geolocation_state CHAR(2),

    ----------------------------------------------------------------------------
    -- DATA LINEAGE
    ----------------------------------------------------------------------------

    source_system_code VARCHAR(50) NOT NULL,

    source_file VARCHAR(255) NOT NULL,

    batch_id UUID NOT NULL,

    load_id UUID NOT NULL,

    ----------------------------------------------------------------------------
    -- SOURCE SYSTEM METADATA
    ----------------------------------------------------------------------------

    source_created_at TIMESTAMP,

    source_updated_at TIMESTAMP,

    ----------------------------------------------------------------------------
    -- ERIP OPERATIONAL METADATA
    ----------------------------------------------------------------------------

    ingested_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    row_hash VARCHAR(64) NOT NULL,

    etl_version VARCHAR(20) NOT NULL,

    validation_status_code VARCHAR(20)
        NOT NULL
        DEFAULT 'PENDING',

    record_status_code VARCHAR(20)
        NOT NULL
        DEFAULT 'ACTIVE',

    ----------------------------------------------------------------------------
    -- CONSTRAINTS
    ----------------------------------------------------------------------------

    CONSTRAINT pk_staging_geolocation
        PRIMARY KEY (staging_geolocation_sk),

    CONSTRAINT fk_geolocation_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system
        (source_system_code),

    CONSTRAINT fk_geolocation_validation_status
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status
        (validation_status_code),

    CONSTRAINT fk_geolocation_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status
        (record_status_code),

    CONSTRAINT fk_geolocation_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version
        (etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_geolocation_zip
ON staging.geolocation(geolocation_zip_code_prefix);

CREATE INDEX IF NOT EXISTS idx_geolocation_city
ON staging.geolocation(geolocation_city);

CREATE INDEX IF NOT EXISTS idx_geolocation_state
ON staging.geolocation(geolocation_state);

-- =============================================================================
-- GEOSPATIAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_geolocation_coordinates
ON staging.geolocation(geolocation_lat, geolocation_lng);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_geolocation_batch
ON staging.geolocation(batch_id);

CREATE INDEX IF NOT EXISTS idx_geolocation_load
ON staging.geolocation(load_id);

CREATE INDEX IF NOT EXISTS idx_geolocation_source
ON staging.geolocation(source_system_code);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_geolocation_ingested
ON staging.geolocation(ingested_at);

CREATE INDEX IF NOT EXISTS idx_geolocation_hash
ON staging.geolocation(row_hash);

CREATE INDEX IF NOT EXISTS idx_geolocation_validation
ON staging.geolocation(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_geolocation_record_status
ON staging.geolocation(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.geolocation IS
'Enterprise landing table for geographic reference data supporting downstream enrichment and spatial analytics.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.geolocation.staging_geolocation_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.geolocation.geolocation_zip_code_prefix IS
'ZIP/postal code prefix from the source system.';

COMMENT ON COLUMN staging.geolocation.geolocation_lat IS
'Latitude coordinate.';

COMMENT ON COLUMN staging.geolocation.geolocation_lng IS
'Longitude coordinate.';

COMMENT ON COLUMN staging.geolocation.geolocation_city IS
'City associated with the ZIP code prefix.';

COMMENT ON COLUMN staging.geolocation.geolocation_state IS
'State abbreviation associated with the ZIP code prefix.';

COMMENT ON COLUMN staging.geolocation.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.geolocation.source_file IS
'Physical file or API endpoint supplying the record.';

COMMENT ON COLUMN staging.geolocation.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.geolocation.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.geolocation.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.geolocation.source_updated_at IS
'Timestamp the record was last updated in the source system.';

COMMENT ON COLUMN staging.geolocation.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.geolocation.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.geolocation.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.geolocation.validation_status_code IS
'Current validation status of the record.';

COMMENT ON COLUMN staging.geolocation.record_status_code IS
'Current operational lifecycle status of the record.';

-- =============================================================================
-- DEPLOYMENT SUMMARY
-- =============================================================================

DO
$$
BEGIN

    RAISE NOTICE '';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE ' ERIP Warehouse Deployment';

    RAISE NOTICE '---------------------------------------------------------------';

    RAISE NOTICE ' Stage        : Staging Layer';

    RAISE NOTICE ' Object       : staging.geolocation';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : staging.product_category_translation';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
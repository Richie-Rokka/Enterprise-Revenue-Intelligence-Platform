/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_product.sql

Purpose:
    Creates the enterprise product staging table.

Description:
    Stores raw product records exactly as received from the source system.
    This table serves as the landing zone for product data prior to validation,
    standardization and dimensional modeling.

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
-- PRODUCT STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.product
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_product_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    product_id VARCHAR(50) NOT NULL,

    product_category_name VARCHAR(100),

    product_name_length INTEGER,

    product_description_length INTEGER,

    product_photos_qty INTEGER,

    product_weight_g NUMERIC(10,2),

    product_length_cm NUMERIC(10,2),

    product_height_cm NUMERIC(10,2),

    product_width_cm NUMERIC(10,2),

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

    CONSTRAINT pk_staging_product
        PRIMARY KEY (staging_product_sk),

    CONSTRAINT fk_product_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system
        (source_system_code),

    CONSTRAINT fk_product_validation_status
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status
        (validation_status_code),

    CONSTRAINT fk_product_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status
        (record_status_code),

    CONSTRAINT fk_product_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version
        (etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_product_business_key
ON staging.product(product_id);

CREATE INDEX IF NOT EXISTS idx_product_category
ON staging.product(product_category_name);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_product_batch
ON staging.product(batch_id);

CREATE INDEX IF NOT EXISTS idx_product_load
ON staging.product(load_id);

CREATE INDEX IF NOT EXISTS idx_product_source
ON staging.product(source_system_code);

CREATE INDEX IF NOT EXISTS idx_product_source_file
ON staging.product(source_file);

-- =============================================================================
-- CDC INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_product_hash
ON staging.product(row_hash);

CREATE INDEX IF NOT EXISTS idx_product_ingested
ON staging.product(ingested_at);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_product_validation
ON staging.product(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_product_record_status
ON staging.product(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.product IS
'Enterprise product landing table supporting auditing, lineage, replay, CDC and incremental loading.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.product.staging_product_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.product.product_id IS
'Product identifier supplied by the source system.';

COMMENT ON COLUMN staging.product.product_category_name IS
'Original product category from the source system.';

COMMENT ON COLUMN staging.product.product_name_length IS
'Length of the product name in characters.';

COMMENT ON COLUMN staging.product.product_description_length IS
'Length of the product description in characters.';

COMMENT ON COLUMN staging.product.product_photos_qty IS
'Number of product images.';

COMMENT ON COLUMN staging.product.product_weight_g IS
'Product weight in grams.';

COMMENT ON COLUMN staging.product.product_length_cm IS
'Product length in centimeters.';

COMMENT ON COLUMN staging.product.product_height_cm IS
'Product height in centimeters.';

COMMENT ON COLUMN staging.product.product_width_cm IS
'Product width in centimeters.';

COMMENT ON COLUMN staging.product.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.product.source_file IS
'Physical file or API endpoint supplying the record.';

COMMENT ON COLUMN staging.product.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.product.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.product.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.product.source_updated_at IS
'Timestamp the record was last updated in the source system.';

COMMENT ON COLUMN staging.product.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.product.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.product.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.product.validation_status_code IS
'Current validation status of the record.';

COMMENT ON COLUMN staging.product.record_status_code IS
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

    RAISE NOTICE ' Object       : staging.product';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : staging.seller';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
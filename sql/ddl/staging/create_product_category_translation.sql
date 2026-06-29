/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_product_category_translation.sql

Purpose:
    Creates the enterprise product category translation staging table.

Description:
    Stores raw product category translations exactly as received from the
    source system. This table provides the mapping between Portuguese
    product category names and their English equivalents.

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
-- PRODUCT CATEGORY TRANSLATION STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.product_category_translation
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_category_translation_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    product_category_name VARCHAR(100) NOT NULL,

    product_category_name_english VARCHAR(100) NOT NULL,

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

    CONSTRAINT pk_staging_category_translation
        PRIMARY KEY (staging_category_translation_sk),

    CONSTRAINT fk_category_translation_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system
        (source_system_code),

    CONSTRAINT fk_category_translation_validation_status
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status
        (validation_status_code),

    CONSTRAINT fk_category_translation_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status
        (record_status_code),

    CONSTRAINT fk_category_translation_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version
        (etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_category_name
ON staging.product_category_translation(product_category_name);

CREATE INDEX IF NOT EXISTS idx_category_name_english
ON staging.product_category_translation(product_category_name_english);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_category_batch
ON staging.product_category_translation(batch_id);

CREATE INDEX IF NOT EXISTS idx_category_load
ON staging.product_category_translation(load_id);

CREATE INDEX IF NOT EXISTS idx_category_source
ON staging.product_category_translation(source_system_code);

CREATE INDEX IF NOT EXISTS idx_category_source_file
ON staging.product_category_translation(source_file);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_category_ingested
ON staging.product_category_translation(ingested_at);

CREATE INDEX IF NOT EXISTS idx_category_hash
ON staging.product_category_translation(row_hash);

CREATE INDEX IF NOT EXISTS idx_category_validation
ON staging.product_category_translation(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_category_record_status
ON staging.product_category_translation(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.product_category_translation IS
'Enterprise landing table for product category translations supporting multilingual reporting and downstream dimensional modeling.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.product_category_translation.staging_category_translation_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.product_category_translation.product_category_name IS
'Original product category name from the source system.';

COMMENT ON COLUMN staging.product_category_translation.product_category_name_english IS
'English translation of the product category.';

COMMENT ON COLUMN staging.product_category_translation.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.product_category_translation.source_file IS
'Physical file or API endpoint supplying the record.';

COMMENT ON COLUMN staging.product_category_translation.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.product_category_translation.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.product_category_translation.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.product_category_translation.source_updated_at IS
'Timestamp the record was last updated in the source system.';

COMMENT ON COLUMN staging.product_category_translation.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.product_category_translation.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.product_category_translation.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.product_category_translation.validation_status_code IS
'Current validation status of the record.';

COMMENT ON COLUMN staging.product_category_translation.record_status_code IS
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

    RAISE NOTICE ' Object       : staging.product_category_translation';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : staging.order';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
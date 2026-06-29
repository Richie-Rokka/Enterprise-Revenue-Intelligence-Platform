/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_seller.sql

Purpose:
    Creates the enterprise seller staging table.

Description:
    Stores raw seller records exactly as received from the source system.
    This table serves as the landing zone for seller data before validation,
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
-- SELLER STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.seller
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_seller_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    seller_id VARCHAR(50) NOT NULL,

    seller_zip_code_prefix INTEGER,

    seller_city VARCHAR(100),

    seller_state CHAR(2),

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

    CONSTRAINT pk_staging_seller
        PRIMARY KEY (staging_seller_sk),

    CONSTRAINT fk_seller_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system
        (source_system_code),

    CONSTRAINT fk_seller_validation_status
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status
        (validation_status_code),

    CONSTRAINT fk_seller_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status
        (record_status_code),

    CONSTRAINT fk_seller_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version
        (etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_seller_business_key
ON staging.seller(seller_id);

CREATE INDEX IF NOT EXISTS idx_seller_city
ON staging.seller(seller_city);

CREATE INDEX IF NOT EXISTS idx_seller_state
ON staging.seller(seller_state);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_seller_batch
ON staging.seller(batch_id);

CREATE INDEX IF NOT EXISTS idx_seller_load
ON staging.seller(load_id);

CREATE INDEX IF NOT EXISTS idx_seller_source
ON staging.seller(source_system_code);

CREATE INDEX IF NOT EXISTS idx_seller_source_file
ON staging.seller(source_file);

-- =============================================================================
-- CDC INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_seller_hash
ON staging.seller(row_hash);

CREATE INDEX IF NOT EXISTS idx_seller_ingested
ON staging.seller(ingested_at);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_seller_validation
ON staging.seller(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_seller_record_status
ON staging.seller(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.seller IS
'Enterprise seller landing table supporting auditing, lineage, replay, CDC and incremental loading.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.seller.staging_seller_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.seller.seller_id IS
'Seller identifier supplied by the source system.';

COMMENT ON COLUMN staging.seller.seller_zip_code_prefix IS
'Seller postal code prefix.';

COMMENT ON COLUMN staging.seller.seller_city IS
'Seller city.';

COMMENT ON COLUMN staging.seller.seller_state IS
'Seller state abbreviation.';

COMMENT ON COLUMN staging.seller.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.seller.source_file IS
'Physical file or API endpoint supplying the record.';

COMMENT ON COLUMN staging.seller.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.seller.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.seller.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.seller.source_updated_at IS
'Timestamp the record was last updated in the source system.';

COMMENT ON COLUMN staging.seller.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.seller.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.seller.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.seller.validation_status_code IS
'Current validation status of the record.';

COMMENT ON COLUMN staging.seller.record_status_code IS
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

    RAISE NOTICE ' Object       : staging.seller';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : staging.geolocation';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
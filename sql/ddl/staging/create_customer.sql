/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_customer.sql

Purpose:
    Creates the enterprise customer staging table.

Description:
    The staging layer preserves raw source data exactly as received while
    enriching it with enterprise metadata required for lineage,
    governance, auditing, replay, incremental processing and
    Change Data Capture (CDC).

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
-- CUSTOMER STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.customer
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_customer_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    customer_id VARCHAR(50) NOT NULL,

    customer_unique_id VARCHAR(50),

    customer_zip_code_prefix INTEGER,

    customer_city VARCHAR(100),

    customer_state CHAR(2),

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

    CONSTRAINT pk_staging_customer
        PRIMARY KEY (staging_customer_sk),

    CONSTRAINT fk_customer_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system
        (source_system_code),

    CONSTRAINT fk_customer_validation_status
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status
        (validation_status_code),

    CONSTRAINT fk_customer_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status
        (record_status_code),

    CONSTRAINT fk_customer_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version
        (etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_customer_business_key
ON staging.customer(customer_id);

CREATE INDEX IF NOT EXISTS idx_customer_unique
ON staging.customer(customer_unique_id);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_customer_batch
ON staging.customer(batch_id);

CREATE INDEX IF NOT EXISTS idx_customer_load
ON staging.customer(load_id);

CREATE INDEX IF NOT EXISTS idx_customer_source
ON staging.customer(source_system_code);

CREATE INDEX IF NOT EXISTS idx_customer_source_file
ON staging.customer(source_file);

-- =============================================================================
-- CDC INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_customer_hash
ON staging.customer(row_hash);

CREATE INDEX IF NOT EXISTS idx_customer_ingested
ON staging.customer(ingested_at);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_customer_validation
ON staging.customer(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_customer_record_status
ON staging.customer(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.customer IS
'Enterprise customer landing table supporting auditing, replay, lineage, CDC and incremental loading.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.customer.staging_customer_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.customer.customer_id IS
'Customer identifier supplied by the source system.';

COMMENT ON COLUMN staging.customer.customer_unique_id IS
'Business customer identifier shared across multiple purchases.';

COMMENT ON COLUMN staging.customer.customer_zip_code_prefix IS
'Customer postal code prefix.';

COMMENT ON COLUMN staging.customer.customer_city IS
'Customer city.';

COMMENT ON COLUMN staging.customer.customer_state IS
'Customer state abbreviation.';

COMMENT ON COLUMN staging.customer.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.customer.source_file IS
'Physical file or API endpoint supplying the record.';

COMMENT ON COLUMN staging.customer.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.customer.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.customer.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.customer.source_updated_at IS
'Timestamp the record was last updated in the source system.';

COMMENT ON COLUMN staging.customer.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.customer.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.customer.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.customer.validation_status_code IS
'Current validation status of the record.';

COMMENT ON COLUMN staging.customer.record_status_code IS
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

    RAISE NOTICE ' Object       : staging.customer';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : staging.order';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
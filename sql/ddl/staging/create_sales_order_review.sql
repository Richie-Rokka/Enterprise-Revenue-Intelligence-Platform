/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_sales_order_review.sql

Purpose:
    Creates the enterprise sales order review staging table.

Description:
    Stores raw customer review records exactly as received from the source
    system. Each record represents customer feedback associated with a
    completed sales order.

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
-- SALES ORDER REVIEW STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.sales_order_review
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_sales_order_review_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    review_id VARCHAR(50) NOT NULL,

    order_id VARCHAR(50) NOT NULL,

    review_score INTEGER NOT NULL,

    review_comment_title TEXT,

    review_comment_message TEXT,

    review_creation_date TIMESTAMP,

    review_answer_timestamp TIMESTAMP,

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
        NOT NULL DEFAULT 'PENDING',

    record_status_code VARCHAR(20)
        NOT NULL DEFAULT 'ACTIVE',

    ----------------------------------------------------------------------------
    -- CONSTRAINTS
    ----------------------------------------------------------------------------

    CONSTRAINT pk_staging_sales_order_review
        PRIMARY KEY (staging_sales_order_review_sk),

    CONSTRAINT uq_sales_order_review_business
        UNIQUE (review_id, batch_id),

    CONSTRAINT fk_sor_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system(source_system_code),

    CONSTRAINT fk_sor_validation
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status(validation_status_code),

    CONSTRAINT fk_sor_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status(record_status_code),

    CONSTRAINT fk_sor_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version(etl_version),

    CONSTRAINT chk_review_score
        CHECK (review_score BETWEEN 1 AND 5)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sor_review_id
ON staging.sales_order_review(review_id);

CREATE INDEX IF NOT EXISTS idx_sor_order
ON staging.sales_order_review(order_id);

CREATE INDEX IF NOT EXISTS idx_sor_score
ON staging.sales_order_review(review_score);

CREATE INDEX IF NOT EXISTS idx_sor_creation_date
ON staging.sales_order_review(review_creation_date);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sor_batch
ON staging.sales_order_review(batch_id);

CREATE INDEX IF NOT EXISTS idx_sor_load
ON staging.sales_order_review(load_id);

CREATE INDEX IF NOT EXISTS idx_sor_source
ON staging.sales_order_review(source_system_code);

CREATE INDEX IF NOT EXISTS idx_sor_source_file
ON staging.sales_order_review(source_file);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sor_ingested
ON staging.sales_order_review(ingested_at);

CREATE INDEX IF NOT EXISTS idx_sor_hash
ON staging.sales_order_review(row_hash);

CREATE INDEX IF NOT EXISTS idx_sor_validation
ON staging.sales_order_review(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_sor_record_status
ON staging.sales_order_review(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.sales_order_review IS
'Enterprise landing table for customer review records supporting customer experience analytics, auditing, replay, CDC and incremental loading.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.sales_order_review.staging_sales_order_review_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.sales_order_review.review_id IS
'Unique review identifier from the source system.';

COMMENT ON COLUMN staging.sales_order_review.order_id IS
'Sales order identifier associated with the review.';

COMMENT ON COLUMN staging.sales_order_review.review_score IS
'Customer satisfaction rating ranging from 1 (lowest) to 5 (highest).';

COMMENT ON COLUMN staging.sales_order_review.review_comment_title IS
'Customer review title.';

COMMENT ON COLUMN staging.sales_order_review.review_comment_message IS
'Customer review message.';

COMMENT ON COLUMN staging.sales_order_review.review_creation_date IS
'Date the customer created the review.';

COMMENT ON COLUMN staging.sales_order_review.review_answer_timestamp IS
'Timestamp when the review became available in the source system.';

COMMENT ON COLUMN staging.sales_order_review.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.sales_order_review.source_file IS
'Source file or API endpoint containing the record.';

COMMENT ON COLUMN staging.sales_order_review.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.sales_order_review.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.sales_order_review.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.sales_order_review.source_updated_at IS
'Timestamp the record was last modified in the source system.';

COMMENT ON COLUMN staging.sales_order_review.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.sales_order_review.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.sales_order_review.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.sales_order_review.validation_status_code IS
'Current validation status.';

COMMENT ON COLUMN staging.sales_order_review.record_status_code IS
'Current operational lifecycle status.';

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

    RAISE NOTICE ' Object       : staging.sales_order_review';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : Analytics Warehouse';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
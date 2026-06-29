/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_sales_order_payment.sql

Purpose:
    Creates the enterprise sales order payment staging table.

Description:
    Stores raw payment records exactly as received from the source system.
    Each record represents a payment transaction associated with a sales order.

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
-- SALES ORDER PAYMENT STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.sales_order_payment
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_sales_order_payment_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    order_id VARCHAR(50) NOT NULL,

    payment_sequential INTEGER NOT NULL,

    payment_type VARCHAR(30) NOT NULL,

    payment_installments INTEGER NOT NULL,

    payment_value NUMERIC(12,2) NOT NULL,

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

    CONSTRAINT pk_staging_sales_order_payment
        PRIMARY KEY (staging_sales_order_payment_sk),

    CONSTRAINT uq_sales_order_payment_business
        UNIQUE (order_id, payment_sequential, batch_id),

    CONSTRAINT fk_sop_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system(source_system_code),

    CONSTRAINT fk_sop_validation
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status(validation_status_code),

    CONSTRAINT fk_sop_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status(record_status_code),

    CONSTRAINT fk_sop_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version(etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sop_order
ON staging.sales_order_payment(order_id);

CREATE INDEX IF NOT EXISTS idx_sop_payment_type
ON staging.sales_order_payment(payment_type);

CREATE INDEX IF NOT EXISTS idx_sop_installments
ON staging.sales_order_payment(payment_installments);

CREATE INDEX IF NOT EXISTS idx_sop_payment_value
ON staging.sales_order_payment(payment_value);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sop_batch
ON staging.sales_order_payment(batch_id);

CREATE INDEX IF NOT EXISTS idx_sop_load
ON staging.sales_order_payment(load_id);

CREATE INDEX IF NOT EXISTS idx_sop_source
ON staging.sales_order_payment(source_system_code);

CREATE INDEX IF NOT EXISTS idx_sop_source_file
ON staging.sales_order_payment(source_file);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sop_ingested
ON staging.sales_order_payment(ingested_at);

CREATE INDEX IF NOT EXISTS idx_sop_hash
ON staging.sales_order_payment(row_hash);

CREATE INDEX IF NOT EXISTS idx_sop_validation
ON staging.sales_order_payment(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_sop_record_status
ON staging.sales_order_payment(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.sales_order_payment IS
'Enterprise landing table for sales order payment transactions supporting payment analytics, auditing, replay, CDC and incremental loading.';

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN staging.sales_order_payment.staging_sales_order_payment_sk IS
'Enterprise surrogate ingestion key.';

COMMENT ON COLUMN staging.sales_order_payment.order_id IS
'Source system sales order identifier.';

COMMENT ON COLUMN staging.sales_order_payment.payment_sequential IS
'Sequence number identifying multiple payments for the same order.';

COMMENT ON COLUMN staging.sales_order_payment.payment_type IS
'Payment method used by the customer.';

COMMENT ON COLUMN staging.sales_order_payment.payment_installments IS
'Number of installments used for the payment.';

COMMENT ON COLUMN staging.sales_order_payment.payment_value IS
'Payment amount recorded by the source system.';

COMMENT ON COLUMN staging.sales_order_payment.source_system_code IS
'Registered source system code.';

COMMENT ON COLUMN staging.sales_order_payment.source_file IS
'Source file or API endpoint containing the record.';

COMMENT ON COLUMN staging.sales_order_payment.batch_id IS
'Enterprise ETL batch identifier.';

COMMENT ON COLUMN staging.sales_order_payment.load_id IS
'Unique ingestion execution identifier.';

COMMENT ON COLUMN staging.sales_order_payment.source_created_at IS
'Timestamp the record was created in the source system.';

COMMENT ON COLUMN staging.sales_order_payment.source_updated_at IS
'Timestamp the record was last modified in the source system.';

COMMENT ON COLUMN staging.sales_order_payment.ingested_at IS
'Timestamp ERIP ingested the record.';

COMMENT ON COLUMN staging.sales_order_payment.row_hash IS
'SHA-256 hash used for change detection.';

COMMENT ON COLUMN staging.sales_order_payment.etl_version IS
'ERIP ETL version responsible for loading the record.';

COMMENT ON COLUMN staging.sales_order_payment.validation_status_code IS
'Current validation status.';

COMMENT ON COLUMN staging.sales_order_payment.record_status_code IS
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

    RAISE NOTICE ' Object       : staging.sales_order_payment';

    RAISE NOTICE ' Status       : SUCCESS';

    RAISE NOTICE ' ERIP Version : 2.0.0';

    RAISE NOTICE ' Database     : %', current_database();

    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;

    RAISE NOTICE ' Next Stage   : staging.sales_order_review';

    RAISE NOTICE '===============================================================';

    RAISE NOTICE '';

END
$$;
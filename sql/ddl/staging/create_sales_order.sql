/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_sales_order.sql

Purpose:
    Creates the enterprise sales order staging table.

Description:
    Stores raw sales order records exactly as received from the source
    system. This table is the authoritative landing zone for transactional
    order data before validation, transformation and dimensional modeling.

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
-- SALES ORDER STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.sales_order
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_sales_order_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    order_id VARCHAR(50) NOT NULL,

    customer_id VARCHAR(50) NOT NULL,

    order_status VARCHAR(30) NOT NULL,

    order_purchase_timestamp TIMESTAMP,

    order_approved_at TIMESTAMP,

    order_delivered_carrier_date TIMESTAMP,

    order_delivered_customer_date TIMESTAMP,

    order_estimated_delivery_date TIMESTAMP,

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

    CONSTRAINT pk_staging_sales_order
        PRIMARY KEY (staging_sales_order_sk),

    CONSTRAINT uq_sales_order_business
        UNIQUE (order_id, batch_id),

    CONSTRAINT fk_sales_order_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system(source_system_code),

    CONSTRAINT fk_sales_order_validation
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status(validation_status_code),

    CONSTRAINT fk_sales_order_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status(record_status_code),

    CONSTRAINT fk_sales_order_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version(etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sales_order_customer
ON staging.sales_order(customer_id);

CREATE INDEX IF NOT EXISTS idx_sales_order_status
ON staging.sales_order(order_status);

CREATE INDEX IF NOT EXISTS idx_sales_order_purchase_date
ON staging.sales_order(order_purchase_timestamp);

CREATE INDEX IF NOT EXISTS idx_sales_order_estimated_delivery
ON staging.sales_order(order_estimated_delivery_date);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sales_order_batch
ON staging.sales_order(batch_id);

CREATE INDEX IF NOT EXISTS idx_sales_order_load
ON staging.sales_order(load_id);

CREATE INDEX IF NOT EXISTS idx_sales_order_source
ON staging.sales_order(source_system_code);

CREATE INDEX IF NOT EXISTS idx_sales_order_source_file
ON staging.sales_order(source_file);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_sales_order_ingested
ON staging.sales_order(ingested_at);

CREATE INDEX IF NOT EXISTS idx_sales_order_hash
ON staging.sales_order(row_hash);

CREATE INDEX IF NOT EXISTS idx_sales_order_validation
ON staging.sales_order(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_sales_order_record_status
ON staging.sales_order(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.sales_order IS
'Enterprise landing table for raw sales order transactions supporting auditing, lineage, replay, CDC and incremental loading.';

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
    RAISE NOTICE ' Object       : staging.sales_order';
    RAISE NOTICE ' Status       : SUCCESS';
    RAISE NOTICE ' ERIP Version : 2.0.0';
    RAISE NOTICE ' Database     : %', current_database();
    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;
    RAISE NOTICE ' Next Stage   : staging.sales_order_item';
    RAISE NOTICE '===============================================================';
    RAISE NOTICE '';
END
$$;
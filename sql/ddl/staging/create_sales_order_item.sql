/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_sales_order_item.sql

Purpose:
    Creates the enterprise sales order item staging table.

Description:
    Stores raw order line items exactly as received from the source system.
    Each record represents one product sold within a customer order and forms
    the primary transactional source for revenue analytics.

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
-- SALES ORDER ITEM STAGING TABLE
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.sales_order_item
(

    ----------------------------------------------------------------------------
    -- INGESTION SURROGATE KEY
    ----------------------------------------------------------------------------

    staging_sales_order_item_sk BIGSERIAL,

    ----------------------------------------------------------------------------
    -- SOURCE BUSINESS DATA
    ----------------------------------------------------------------------------

    order_id VARCHAR(50) NOT NULL,

    order_item_id INTEGER NOT NULL,

    product_id VARCHAR(50) NOT NULL,

    seller_id VARCHAR(50) NOT NULL,

    shipping_limit_date TIMESTAMP,

    price NUMERIC(12,2) NOT NULL,

    freight_value NUMERIC(12,2) NOT NULL,

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

    CONSTRAINT pk_staging_sales_order_item
        PRIMARY KEY (staging_sales_order_item_sk),

    CONSTRAINT uq_sales_order_item_business
        UNIQUE (order_id, order_item_id, batch_id),

    CONSTRAINT fk_soi_source_system
        FOREIGN KEY (source_system_code)
        REFERENCES metadata.ref_source_system(source_system_code),

    CONSTRAINT fk_soi_validation
        FOREIGN KEY (validation_status_code)
        REFERENCES metadata.ref_validation_status(validation_status_code),

    CONSTRAINT fk_soi_record_status
        FOREIGN KEY (record_status_code)
        REFERENCES metadata.ref_record_status(record_status_code),

    CONSTRAINT fk_soi_etl_version
        FOREIGN KEY (etl_version)
        REFERENCES metadata.ref_etl_version(etl_version)

);

-- =============================================================================
-- BUSINESS INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_soi_order
ON staging.sales_order_item(order_id);

CREATE INDEX IF NOT EXISTS idx_soi_product
ON staging.sales_order_item(product_id);

CREATE INDEX IF NOT EXISTS idx_soi_seller
ON staging.sales_order_item(seller_id);

CREATE INDEX IF NOT EXISTS idx_soi_shipping_date
ON staging.sales_order_item(shipping_limit_date);

-- =============================================================================
-- FINANCIAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_soi_price
ON staging.sales_order_item(price);

CREATE INDEX IF NOT EXISTS idx_soi_freight
ON staging.sales_order_item(freight_value);

-- =============================================================================
-- DATA LINEAGE INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_soi_batch
ON staging.sales_order_item(batch_id);

CREATE INDEX IF NOT EXISTS idx_soi_load
ON staging.sales_order_item(load_id);

CREATE INDEX IF NOT EXISTS idx_soi_source
ON staging.sales_order_item(source_system_code);

-- =============================================================================
-- OPERATIONAL INDEXES
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_soi_ingested
ON staging.sales_order_item(ingested_at);

CREATE INDEX IF NOT EXISTS idx_soi_hash
ON staging.sales_order_item(row_hash);

CREATE INDEX IF NOT EXISTS idx_soi_validation
ON staging.sales_order_item(validation_status_code);

CREATE INDEX IF NOT EXISTS idx_soi_record_status
ON staging.sales_order_item(record_status_code);

-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE staging.sales_order_item IS
'Enterprise landing table for sales order line items supporting revenue analytics, replay, CDC and incremental loading.';

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
    RAISE NOTICE ' Object       : staging.sales_order_item';
    RAISE NOTICE ' Status       : SUCCESS';
    RAISE NOTICE ' ERIP Version : 2.0.0';
    RAISE NOTICE ' Database     : %', current_database();
    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;
    RAISE NOTICE ' Next Stage   : staging.sales_order_payment';
    RAISE NOTICE '===============================================================';
    RAISE NOTICE '';
END
$$;
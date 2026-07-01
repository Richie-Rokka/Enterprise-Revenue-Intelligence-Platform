/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module:
    create_dim_customer.sql

Schema:
    analytics

Object:
    dim_customer

Purpose:
    Creates the Enterprise Customer Dimension.

Description:
    Stores customer master data using Slowly Changing Dimension
    Type 2 methodology to preserve historical attribute changes.

Business Process
----------------
Customer Analytics

Grain
-----
One record represents one customer version.

Primary Key
-----------
customer_sk

Business Key
------------
customer_id

SCD Strategy
------------
Type 2

Refresh Strategy
----------------
Incremental

Source
------
staging.customer

Author
------
Abodunrin Oketade

Platform
--------
Enterprise Revenue Intelligence Platform (ERIP)

Database
--------
PostgreSQL 18

Version
-------
3.0.0

===============================================================================
*/

-- =============================================================================
-- DROP TABLE
-- =============================================================================

DROP TABLE IF EXISTS analytics.dim_customer CASCADE;


-- =============================================================================
-- CREATE TABLE
-- =============================================================================

CREATE TABLE analytics.dim_customer
(

    --------------------------------------------------------------------------
    -- SURROGATE KEY
    --------------------------------------------------------------------------

    customer_sk                    BIGSERIAL          NOT NULL,

    --------------------------------------------------------------------------
    -- BUSINESS KEY
    --------------------------------------------------------------------------

    customer_id                    VARCHAR(50)        NOT NULL,

    --------------------------------------------------------------------------
    -- CUSTOMER ATTRIBUTES
    --------------------------------------------------------------------------

    customer_zip_code_prefix       INTEGER            NOT NULL,

    customer_city                  VARCHAR(100)       NOT NULL,

    customer_state                 CHAR(2)            NOT NULL,

    --------------------------------------------------------------------------
    -- HIERARCHY
    --------------------------------------------------------------------------

    customer_region                VARCHAR(50),

    customer_country               VARCHAR(100)
                                        DEFAULT 'Brazil',

    --------------------------------------------------------------------------
    -- SCD TYPE 2
    --------------------------------------------------------------------------

    effective_from                 DATE               NOT NULL,

    effective_to                   DATE               NOT NULL,

    is_current                     BOOLEAN            NOT NULL,

    record_version                 INTEGER            NOT NULL
                                        DEFAULT 1,

    --------------------------------------------------------------------------
    -- AUDIT
    --------------------------------------------------------------------------

    created_timestamp              TIMESTAMPTZ        NOT NULL
                                        DEFAULT CURRENT_TIMESTAMP,

    updated_timestamp              TIMESTAMPTZ        NOT NULL
                                        DEFAULT CURRENT_TIMESTAMP

);

-- =============================================================================
-- PRIMARY KEY
-- =============================================================================

ALTER TABLE analytics.dim_customer
ADD CONSTRAINT pk_dim_customer
PRIMARY KEY (customer_sk);


-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_customer
ADD CONSTRAINT uq_dim_customer_sk_version
UNIQUE
(
    customer_id,
    record_version
);


-- =============================================================================
-- CHECK CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_customer
ADD CONSTRAINT chk_dim_customer_record_version
CHECK
(
    record_version >= 1
);


ALTER TABLE analytics.dim_customer
ADD CONSTRAINT chk_dim_customer_effective_dates
CHECK
(
    effective_from <= effective_to
);


ALTER TABLE analytics.dim_customer
ADD CONSTRAINT chk_dim_customer_state
CHECK
(
    LENGTH(customer_state) = 2
);


-- =============================================================================
-- BUSINESS RULES
-- =============================================================================

-- Only one active record per customer
CREATE UNIQUE INDEX idx_dim_customer_current_record

ON analytics.dim_customer
(
    customer_id
)

WHERE is_current = TRUE;


-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================

CREATE INDEX idx_dim_customer_business_key

ON analytics.dim_customer
(
    customer_id
);


CREATE INDEX idx_dim_customer_state

ON analytics.dim_customer
(
    customer_state
);


CREATE INDEX idx_dim_customer_city

ON analytics.dim_customer
(
    customer_city
);


CREATE INDEX idx_dim_customer_region

ON analytics.dim_customer
(
    customer_region
);


CREATE INDEX idx_dim_customer_country

ON analytics.dim_customer
(
    customer_country
);


CREATE INDEX idx_dim_customer_effective_dates

ON analytics.dim_customer
(
    effective_from,
    effective_to
);


CREATE INDEX idx_dim_customer_current

ON analytics.dim_customer
(
    is_current
);


CREATE INDEX idx_dim_customer_version

ON analytics.dim_customer
(
    customer_id,
    record_version
);


CREATE INDEX idx_dim_customer_created

ON analytics.dim_customer
(
    created_timestamp
);

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN analytics.dim_customer.customer_sk IS
'Surrogate key uniquely identifying each customer version.';

COMMENT ON COLUMN analytics.dim_customer.customer_id IS
'Business key from the source system.';

COMMENT ON COLUMN analytics.dim_customer.customer_zip_code_prefix IS
'Customer ZIP code prefix from the source system.';

COMMENT ON COLUMN analytics.dim_customer.customer_city IS
'Customer city.';

COMMENT ON COLUMN analytics.dim_customer.customer_state IS
'Customer state abbreviation.';

COMMENT ON COLUMN analytics.dim_customer.customer_region IS
'Enterprise reporting region.';

COMMENT ON COLUMN analytics.dim_customer.customer_country IS
'Customer country. Default is Brazil.';

COMMENT ON COLUMN analytics.dim_customer.effective_from IS
'Date when this customer version became effective.';

COMMENT ON COLUMN analytics.dim_customer.effective_to IS
'Date when this customer version expires.';

COMMENT ON COLUMN analytics.dim_customer.is_current IS
'Indicates the active customer version.';

COMMENT ON COLUMN analytics.dim_customer.record_version IS
'SCD Type 2 version number.';

COMMENT ON COLUMN analytics.dim_customer.created_timestamp IS
'Timestamp when the row was created.';

COMMENT ON COLUMN analytics.dim_customer.updated_timestamp IS
'Timestamp when the row was last updated.';


-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE analytics.dim_customer IS
'Enterprise Customer Dimension implementing Slowly Changing Dimension (Type 2)
to preserve historical customer attribute changes.';


-- =============================================================================
-- VALIDATION QUERIES
-- =============================================================================

-- Verify table exists

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'analytics'
  AND table_name = 'dim_customer';


-- Verify constraints

SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'analytics'
  AND table_name = 'dim_customer'
ORDER BY constraint_type;


-- Verify indexes

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'analytics'
  AND tablename = 'dim_customer'
ORDER BY indexname;


-- Verify column metadata

SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'analytics'
  AND table_name = 'dim_customer'
ORDER BY ordinal_position;


-- =============================================================================
-- SAMPLE ANALYTICS QUERIES
-- =============================================================================

-- Current active customers

SELECT
    customer_id,
    customer_city,
    customer_state
FROM analytics.dim_customer
WHERE is_current = TRUE
ORDER BY customer_id;


-- Customer versions

SELECT
    customer_id,
    record_version,
    effective_from,
    effective_to,
    is_current
FROM analytics.dim_customer
ORDER BY
    customer_id,
    record_version;


-- Customers by state

SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM analytics.dim_customer
WHERE is_current = TRUE
GROUP BY customer_state
ORDER BY total_customers DESC;


-- Customers by region

SELECT
    customer_region,
    COUNT(*) AS total_customers
FROM analytics.dim_customer
WHERE is_current = TRUE
GROUP BY customer_region
ORDER BY customer_region;


-- =============================================================================
-- CHANGE LOG
-- =============================================================================
--
-- Version : 3.0.0
--
-- Initial enterprise implementation.
--
-- Features
-- --------
-- • Kimball SCD Type 2 implementation
-- • Surrogate key architecture
-- • Business key preservation
-- • Historical tracking
-- • Partial unique index for active records
-- • Enterprise auditing
-- • PostgreSQL optimized
--
-- =============================================================================
-- END OF FILE
-- =============================================================================
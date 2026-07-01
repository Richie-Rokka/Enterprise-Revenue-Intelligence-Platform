/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module:
    create_dim_seller.sql

Schema:
    analytics

Object:
    dim_seller

Purpose:
    Creates the Enterprise Seller Dimension.

Description:
    Stores seller master data using Slowly Changing Dimension
    Type 2 methodology to preserve historical seller changes.

Business Process
----------------
Seller Analytics

Grain
-----
One record represents one seller version.

Primary Key
-----------
seller_sk

Business Key
------------
seller_id

SCD Strategy
------------
Type 2

Refresh Strategy
----------------
Incremental

Source
------
staging.seller

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

DROP TABLE IF EXISTS analytics.dim_seller CASCADE;


-- =============================================================================
-- CREATE TABLE
-- =============================================================================

CREATE TABLE analytics.dim_seller
(

    --------------------------------------------------------------------------
    -- SURROGATE KEY
    --------------------------------------------------------------------------

    seller_sk                       BIGSERIAL           NOT NULL,

    --------------------------------------------------------------------------
    -- BUSINESS KEY
    --------------------------------------------------------------------------

    seller_id                       VARCHAR(50)         NOT NULL,

    --------------------------------------------------------------------------
    -- SELLER ATTRIBUTES
    --------------------------------------------------------------------------

    seller_zip_code_prefix          INTEGER             NOT NULL,

    seller_city                     VARCHAR(100)        NOT NULL,

    seller_state                    CHAR(2)             NOT NULL,

    --------------------------------------------------------------------------
    -- DERIVED ATTRIBUTES
    --------------------------------------------------------------------------

    seller_region                   VARCHAR(50),

    seller_country                  VARCHAR(100)
                                        DEFAULT 'Brazil',

    --------------------------------------------------------------------------
    -- SCD TYPE 2
    --------------------------------------------------------------------------

    effective_from                  DATE                NOT NULL,

    effective_to                    DATE                NOT NULL,

    is_current                      BOOLEAN             NOT NULL,

    record_version                  INTEGER             NOT NULL
                                        DEFAULT 1,

    --------------------------------------------------------------------------
    -- AUDIT
    --------------------------------------------------------------------------

    created_timestamp               TIMESTAMPTZ         NOT NULL
                                        DEFAULT CURRENT_TIMESTAMP,

    updated_timestamp               TIMESTAMPTZ         NOT NULL
                                        DEFAULT CURRENT_TIMESTAMP

);

-- =============================================================================
-- PRIMARY KEY
-- =============================================================================

ALTER TABLE analytics.dim_seller
ADD CONSTRAINT pk_dim_seller
PRIMARY KEY (seller_sk);


-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_seller
ADD CONSTRAINT uq_dim_seller_version
UNIQUE
(
    seller_id,
    record_version
);


-- =============================================================================
-- CHECK CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_seller
ADD CONSTRAINT chk_dim_seller_record_version
CHECK
(
    record_version >= 1
);


ALTER TABLE analytics.dim_seller
ADD CONSTRAINT chk_dim_seller_effective_dates
CHECK
(
    effective_from <= effective_to
);


ALTER TABLE analytics.dim_seller
ADD CONSTRAINT chk_dim_seller_state
CHECK
(
    LENGTH(seller_state) = 2
);


ALTER TABLE analytics.dim_seller
ADD CONSTRAINT chk_dim_seller_country
CHECK
(
    seller_country IS NOT NULL
);


-- =============================================================================
-- BUSINESS RULE
-- =============================================================================

CREATE UNIQUE INDEX idx_dim_seller_current_record

ON analytics.dim_seller
(
    seller_id
)

WHERE is_current = TRUE;


-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================

CREATE INDEX idx_dim_seller_business_key

ON analytics.dim_seller
(
    seller_id
);


CREATE INDEX idx_dim_seller_city

ON analytics.dim_seller
(
    seller_city
);


CREATE INDEX idx_dim_seller_state

ON analytics.dim_seller
(
    seller_state
);


CREATE INDEX idx_dim_seller_region

ON analytics.dim_seller
(
    seller_region
);


CREATE INDEX idx_dim_seller_country

ON analytics.dim_seller
(
    seller_country
);


CREATE INDEX idx_dim_seller_effective_dates

ON analytics.dim_seller
(
    effective_from,
    effective_to
);


CREATE INDEX idx_dim_seller_current

ON analytics.dim_seller
(
    is_current
);


CREATE INDEX idx_dim_seller_version

ON analytics.dim_seller
(
    seller_id,
    record_version
);


CREATE INDEX idx_dim_seller_created

ON analytics.dim_seller
(
    created_timestamp
);

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN analytics.dim_seller.seller_sk IS
'Surrogate key uniquely identifying each seller version.';

COMMENT ON COLUMN analytics.dim_seller.seller_id IS
'Business key from the source system.';

COMMENT ON COLUMN analytics.dim_seller.seller_zip_code_prefix IS
'Seller ZIP code prefix from the source system.';

COMMENT ON COLUMN analytics.dim_seller.seller_city IS
'Seller city.';

COMMENT ON COLUMN analytics.dim_seller.seller_state IS
'Seller state abbreviation.';

COMMENT ON COLUMN analytics.dim_seller.seller_region IS
'Enterprise reporting region.';

COMMENT ON COLUMN analytics.dim_seller.seller_country IS
'Seller country. Default is Brazil.';

COMMENT ON COLUMN analytics.dim_seller.effective_from IS
'Date this seller version became effective.';

COMMENT ON COLUMN analytics.dim_seller.effective_to IS
'Date this seller version expired.';

COMMENT ON COLUMN analytics.dim_seller.is_current IS
'Indicates whether this is the active seller version.';

COMMENT ON COLUMN analytics.dim_seller.record_version IS
'SCD Type 2 version number.';

COMMENT ON COLUMN analytics.dim_seller.created_timestamp IS
'Timestamp when the record was created.';

COMMENT ON COLUMN analytics.dim_seller.updated_timestamp IS
'Timestamp when the record was last updated.';


-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE analytics.dim_seller IS
'Enterprise Seller Dimension implementing Slowly Changing Dimension (Type 2)
to preserve historical seller attribute changes.';


-- =============================================================================
-- VALIDATION QUERIES
-- =============================================================================

-- Verify table exists

SELECT

    table_schema,

    table_name

FROM information_schema.tables

WHERE table_schema = 'analytics'

AND table_name = 'dim_seller';


-- Verify constraints

SELECT

    constraint_name,

    constraint_type

FROM information_schema.table_constraints

WHERE table_schema = 'analytics'

AND table_name = 'dim_seller'

ORDER BY constraint_type;


-- Verify indexes

SELECT

    indexname,

    indexdef

FROM pg_indexes

WHERE schemaname = 'analytics'

AND tablename = 'dim_seller'

ORDER BY indexname;


-- Verify metadata

SELECT

    ordinal_position,

    column_name,

    data_type,

    is_nullable

FROM information_schema.columns

WHERE table_schema = 'analytics'

AND table_name = 'dim_seller'

ORDER BY ordinal_position;


-- =============================================================================
-- SAMPLE ANALYTICS QUERIES
-- =============================================================================

-- Active sellers

SELECT

    seller_id,

    seller_city,

    seller_state,

    seller_region

FROM analytics.dim_seller

WHERE is_current = TRUE

ORDER BY seller_id;


-- Sellers by state

SELECT

    seller_state,

    COUNT(*) AS total_sellers

FROM analytics.dim_seller

WHERE is_current = TRUE

GROUP BY seller_state

ORDER BY total_sellers DESC;


-- Sellers by region

SELECT

    seller_region,

    COUNT(*) AS total_sellers

FROM analytics.dim_seller

WHERE is_current = TRUE

GROUP BY seller_region

ORDER BY seller_region;


-- Seller history

SELECT

    seller_id,

    record_version,

    effective_from,

    effective_to,

    is_current

FROM analytics.dim_seller

ORDER BY

    seller_id,

    record_version;


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
-- • Historical seller tracking
-- • Geographic hierarchy
-- • Enterprise indexing
-- • PostgreSQL optimized
--
-- =============================================================================
-- END OF FILE
-- =============================================================================
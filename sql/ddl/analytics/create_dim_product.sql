/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module:
    create_dim_product.sql

Schema:
    analytics

Object:
    dim_product

Purpose:
    Creates the Enterprise Product Dimension.

Description:
    Stores product master data using Slowly Changing Dimension
    Type 2 methodology to preserve historical product attribute changes.

Business Process
----------------
Product Analytics

Grain
-----
One record represents one product version.

Primary Key
-----------
product_sk

Business Key
------------
product_id

SCD Strategy
------------
Type 2

Refresh Strategy
----------------
Incremental

Source
------
staging.product
staging.product_category_translation

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

DROP TABLE IF EXISTS analytics.dim_product CASCADE;


-- =============================================================================
-- CREATE TABLE
-- =============================================================================

CREATE TABLE analytics.dim_product
(

    --------------------------------------------------------------------------
    -- SURROGATE KEY
    --------------------------------------------------------------------------

    product_sk                      BIGSERIAL           NOT NULL,

    --------------------------------------------------------------------------
    -- BUSINESS KEY
    --------------------------------------------------------------------------

    product_id                      VARCHAR(50)         NOT NULL,

    --------------------------------------------------------------------------
    -- PRODUCT ATTRIBUTES
    --------------------------------------------------------------------------

    product_category_name           VARCHAR(100),

    product_category_english        VARCHAR(100),

    product_weight_g                NUMERIC(10,2),

    product_length_cm               NUMERIC(10,2),

    product_height_cm               NUMERIC(10,2),

    product_width_cm                NUMERIC(10,2),

    --------------------------------------------------------------------------
    -- DERIVED ATTRIBUTES
    --------------------------------------------------------------------------

    product_volume_cm3              NUMERIC(18,2),

    product_size_class              VARCHAR(20),

    product_weight_class            VARCHAR(20),

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

ALTER TABLE analytics.dim_product
ADD CONSTRAINT pk_dim_product
PRIMARY KEY (product_sk);


-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_product
ADD CONSTRAINT uq_dim_product_version
UNIQUE
(
    product_id,
    record_version
);


-- =============================================================================
-- CHECK CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_record_version
CHECK
(
    record_version >= 1
);


ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_effective_dates
CHECK
(
    effective_from <= effective_to
);


ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_weight
CHECK
(
    product_weight_g IS NULL
    OR product_weight_g >= 0
);


ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_length
CHECK
(
    product_length_cm IS NULL
    OR product_length_cm >= 0
);


ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_height
CHECK
(
    product_height_cm IS NULL
    OR product_height_cm >= 0
);


ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_width
CHECK
(
    product_width_cm IS NULL
    OR product_width_cm >= 0
);


ALTER TABLE analytics.dim_product
ADD CONSTRAINT chk_dim_product_volume
CHECK
(
    product_volume_cm3 IS NULL
    OR product_volume_cm3 >= 0
);


-- =============================================================================
-- BUSINESS RULE
-- =============================================================================

CREATE UNIQUE INDEX idx_dim_product_current_record

ON analytics.dim_product
(
    product_id
)

WHERE is_current = TRUE;


-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================

CREATE INDEX idx_dim_product_business_key

ON analytics.dim_product
(
    product_id
);


CREATE INDEX idx_dim_product_category

ON analytics.dim_product
(
    product_category_name
);


CREATE INDEX idx_dim_product_category_en

ON analytics.dim_product
(
    product_category_english
);


CREATE INDEX idx_dim_product_weight

ON analytics.dim_product
(
    product_weight_g
);


CREATE INDEX idx_dim_product_size

ON analytics.dim_product
(
    product_size_class
);


CREATE INDEX idx_dim_product_weight_class

ON analytics.dim_product
(
    product_weight_class
);


CREATE INDEX idx_dim_product_effective_dates

ON analytics.dim_product
(
    effective_from,
    effective_to
);


CREATE INDEX idx_dim_product_current

ON analytics.dim_product
(
    is_current
);


CREATE INDEX idx_dim_product_version

ON analytics.dim_product
(
    product_id,
    record_version
);


CREATE INDEX idx_dim_product_created

ON analytics.dim_product
(
    created_timestamp
);

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN analytics.dim_product.product_sk IS
'Surrogate key uniquely identifying each product version.';

COMMENT ON COLUMN analytics.dim_product.product_id IS
'Business key from the source system.';

COMMENT ON COLUMN analytics.dim_product.product_category_name IS
'Original product category name from the source system.';

COMMENT ON COLUMN analytics.dim_product.product_category_english IS
'English translation of the product category.';

COMMENT ON COLUMN analytics.dim_product.product_weight_g IS
'Product weight in grams.';

COMMENT ON COLUMN analytics.dim_product.product_length_cm IS
'Product length in centimeters.';

COMMENT ON COLUMN analytics.dim_product.product_height_cm IS
'Product height in centimeters.';

COMMENT ON COLUMN analytics.dim_product.product_width_cm IS
'Product width in centimeters.';

COMMENT ON COLUMN analytics.dim_product.product_volume_cm3 IS
'Calculated product volume in cubic centimeters.';

COMMENT ON COLUMN analytics.dim_product.product_size_class IS
'Derived product size classification.';

COMMENT ON COLUMN analytics.dim_product.product_weight_class IS
'Derived product weight classification.';

COMMENT ON COLUMN analytics.dim_product.effective_from IS
'Date this product version became effective.';

COMMENT ON COLUMN analytics.dim_product.effective_to IS
'Date this product version expires.';

COMMENT ON COLUMN analytics.dim_product.is_current IS
'Indicates whether this is the active product version.';

COMMENT ON COLUMN analytics.dim_product.record_version IS
'SCD Type 2 version number.';

COMMENT ON COLUMN analytics.dim_product.created_timestamp IS
'Timestamp when the record was created.';

COMMENT ON COLUMN analytics.dim_product.updated_timestamp IS
'Timestamp when the record was last updated.';


-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE analytics.dim_product IS
'Enterprise Product Dimension implementing Slowly Changing Dimension (Type 2)
to preserve historical product attribute changes.';


-- =============================================================================
-- VALIDATION QUERIES
-- =============================================================================

-- Verify table exists

SELECT

    table_schema,

    table_name

FROM information_schema.tables

WHERE table_schema = 'analytics'

AND table_name = 'dim_product';


-- Verify constraints

SELECT

    constraint_name,

    constraint_type

FROM information_schema.table_constraints

WHERE table_schema = 'analytics'

AND table_name = 'dim_product'

ORDER BY constraint_type;


-- Verify indexes

SELECT

    indexname,

    indexdef

FROM pg_indexes

WHERE schemaname = 'analytics'

AND tablename = 'dim_product'

ORDER BY indexname;


-- Verify metadata

SELECT

    ordinal_position,

    column_name,

    data_type,

    is_nullable

FROM information_schema.columns

WHERE table_schema = 'analytics'

AND table_name = 'dim_product'

ORDER BY ordinal_position;


-- =============================================================================
-- SAMPLE ANALYTICS QUERIES
-- =============================================================================

-- Active products

SELECT

    product_id,

    product_category_english,

    product_size_class,

    product_weight_class

FROM analytics.dim_product

WHERE is_current = TRUE

ORDER BY product_id;


-- Product category distribution

SELECT

    product_category_english,

    COUNT(*) AS total_products

FROM analytics.dim_product

WHERE is_current = TRUE

GROUP BY product_category_english

ORDER BY total_products DESC;


-- Product size distribution

SELECT

    product_size_class,

    COUNT(*) AS total_products

FROM analytics.dim_product

WHERE is_current = TRUE

GROUP BY product_size_class

ORDER BY product_size_class;


-- Product weight distribution

SELECT

    product_weight_class,

    COUNT(*) AS total_products

FROM analytics.dim_product

WHERE is_current = TRUE

GROUP BY product_weight_class

ORDER BY product_weight_class;


-- Product history

SELECT

    product_id,

    record_version,

    effective_from,

    effective_to,

    is_current

FROM analytics.dim_product

ORDER BY

    product_id,

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
-- • Product category translation support
-- • Derived product volume
-- • Product size classification
-- • Product weight classification
-- • Historical version tracking
-- • Enterprise indexing
-- • PostgreSQL optimized
--
-- =============================================================================
-- END OF FILE
-- =============================================================================
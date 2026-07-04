/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module:
    create_fact_sales.sql

Schema:
    analytics

Object:
    fact_sales

Purpose:
    Creates the Enterprise Sales Fact Table.

Description:
    Stores transactional sales facts at the order-item level for
    enterprise reporting, forecasting, profitability analysis,
    seller performance, customer analytics and product analytics.

Business Process
----------------
Sales

Grain
-----
One record represents one product sold within one order.

Primary Key
-----------
sales_sk

Refresh Strategy
----------------
Incremental

Source
------
staging.orders
staging.order_items
staging.order_payments

Author
------
Abodunrin Oketade

Platform
--------
Enterprise Revenue Intelligence Platform (ERIP)

Version
-------
3.0.0

===============================================================================
*/


-- =============================================================================
-- DROP TABLE
-- =============================================================================

DROP TABLE IF EXISTS analytics.fact_sales CASCADE;


-- =============================================================================
-- CREATE TABLE
-- =============================================================================

CREATE TABLE analytics.fact_sales
(

    ----------------------------------------------------------------------------
    -- SURROGATE KEY
    ----------------------------------------------------------------------------

    sales_sk                    BIGSERIAL           NOT NULL,

    ----------------------------------------------------------------------------
    -- BUSINESS KEYS
    ----------------------------------------------------------------------------

    order_id                    VARCHAR(50)         NOT NULL,

    order_item_id               INTEGER             NOT NULL,

    ----------------------------------------------------------------------------
    -- DIMENSION KEYS
    ----------------------------------------------------------------------------

    date_key                    INTEGER             NOT NULL,

    customer_sk                 BIGINT              NOT NULL,

    product_sk                  BIGINT              NOT NULL,

    seller_sk                   BIGINT              NOT NULL,

    ----------------------------------------------------------------------------
    -- DEGENERATE DIMENSIONS
    ----------------------------------------------------------------------------

    payment_type                VARCHAR(30),

    order_status                VARCHAR(30),

    ----------------------------------------------------------------------------
    -- ADDITIVE MEASURES
    ----------------------------------------------------------------------------

    quantity                    INTEGER             NOT NULL DEFAULT 1,

    item_price                  NUMERIC(12,2)       NOT NULL,

    freight_value               NUMERIC(12,2)       NOT NULL,

    gross_sales_amount          NUMERIC(14,2)       NOT NULL,

    net_sales_amount            NUMERIC(14,2)       NOT NULL,

    payment_value               NUMERIC(14,2),

    ----------------------------------------------------------------------------
    -- DERIVED MEASURES
    ----------------------------------------------------------------------------

    average_selling_price       NUMERIC(14,2),

    freight_percentage          NUMERIC(8,4),

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------

    created_timestamp           TIMESTAMPTZ
                                    NOT NULL
                                    DEFAULT CURRENT_TIMESTAMP

);

-- =============================================================================
-- PRIMARY KEY
-- =============================================================================

ALTER TABLE analytics.fact_sales
ADD CONSTRAINT pk_fact_sales
PRIMARY KEY (sales_sk);


-- =============================================================================
-- BUSINESS KEY
-- =============================================================================

ALTER TABLE analytics.fact_sales
ADD CONSTRAINT uq_fact_sales_order_item
UNIQUE
(
    order_id,
    order_item_id
);


-- =============================================================================
-- FOREIGN KEYS
-- =============================================================================

ALTER TABLE analytics.fact_sales
ADD CONSTRAINT fk_fact_sales_date
FOREIGN KEY
(
    date_key
)
REFERENCES analytics.dim_date
(
    date_key
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT fk_fact_sales_customer
FOREIGN KEY
(
    customer_sk
)
REFERENCES analytics.dim_customer
(
    customer_sk
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT fk_fact_sales_product
FOREIGN KEY
(
    product_sk
)
REFERENCES analytics.dim_product
(
    product_sk
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT fk_fact_sales_seller
FOREIGN KEY
(
    seller_sk
)
REFERENCES analytics.dim_seller
(
    seller_sk
);


-- =============================================================================
-- CHECK CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_quantity
CHECK
(
    quantity > 0
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_item_price
CHECK
(
    item_price >= 0
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_freight
CHECK
(
    freight_value >= 0
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_gross_sales
CHECK
(
    gross_sales_amount >= 0
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_net_sales
CHECK
(
    net_sales_amount >= 0
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_payment
CHECK
(
    payment_value IS NULL
    OR payment_value >= 0
);


ALTER TABLE analytics.fact_sales
ADD CONSTRAINT chk_fact_sales_freight_pct
CHECK
(
    freight_percentage IS NULL
    OR freight_percentage >= 0
);


-- =============================================================================
-- STAR SCHEMA INDEXES
-- =============================================================================

CREATE INDEX idx_fact_sales_date

ON analytics.fact_sales
(
    date_key
);


CREATE INDEX idx_fact_sales_customer

ON analytics.fact_sales
(
    customer_sk
);


CREATE INDEX idx_fact_sales_product

ON analytics.fact_sales
(
    product_sk
);


CREATE INDEX idx_fact_sales_seller

ON analytics.fact_sales
(
    seller_sk
);


-- =============================================================================
-- REPORTING INDEXES
-- =============================================================================

CREATE INDEX idx_fact_sales_order

ON analytics.fact_sales
(
    order_id
);


CREATE INDEX idx_fact_sales_status

ON analytics.fact_sales
(
    order_status
);


CREATE INDEX idx_fact_sales_payment_type

ON analytics.fact_sales
(
    payment_type
);


CREATE INDEX idx_fact_sales_date_customer

ON analytics.fact_sales
(
    date_key,
    customer_sk
);


CREATE INDEX idx_fact_sales_date_product

ON analytics.fact_sales
(
    date_key,
    product_sk
);


CREATE INDEX idx_fact_sales_date_seller

ON analytics.fact_sales
(
    date_key,
    seller_sk
);


CREATE INDEX idx_fact_sales_created

ON analytics.fact_sales
(
    created_timestamp
);

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN analytics.fact_sales.sales_sk IS
'Surrogate key uniquely identifying each sales transaction.';

COMMENT ON COLUMN analytics.fact_sales.order_id IS
'Business order identifier from the source system.';

COMMENT ON COLUMN analytics.fact_sales.order_item_id IS
'Order item sequence within the order.';

COMMENT ON COLUMN analytics.fact_sales.date_key IS
'Foreign key to the Date Dimension.';

COMMENT ON COLUMN analytics.fact_sales.customer_sk IS
'Foreign key to the Customer Dimension.';

COMMENT ON COLUMN analytics.fact_sales.product_sk IS
'Foreign key to the Product Dimension.';

COMMENT ON COLUMN analytics.fact_sales.seller_sk IS
'Foreign key to the Seller Dimension.';

COMMENT ON COLUMN analytics.fact_sales.payment_type IS
'Payment method used for the order.';

COMMENT ON COLUMN analytics.fact_sales.order_status IS
'Current order status.';

COMMENT ON COLUMN analytics.fact_sales.quantity IS
'Quantity sold.';

COMMENT ON COLUMN analytics.fact_sales.item_price IS
'Unit selling price.';

COMMENT ON COLUMN analytics.fact_sales.freight_value IS
'Freight charge for the order item.';

COMMENT ON COLUMN analytics.fact_sales.gross_sales_amount IS
'Gross sales before deductions.';

COMMENT ON COLUMN analytics.fact_sales.net_sales_amount IS
'Net sales amount after calculations.';

COMMENT ON COLUMN analytics.fact_sales.payment_value IS
'Amount paid by the customer.';

COMMENT ON COLUMN analytics.fact_sales.average_selling_price IS
'Average selling price per unit.';

COMMENT ON COLUMN analytics.fact_sales.freight_percentage IS
'Freight expressed as a percentage of gross sales.';

COMMENT ON COLUMN analytics.fact_sales.created_timestamp IS
'Timestamp when the fact record was created.';


-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE analytics.fact_sales IS
'Enterprise Sales Fact Table supporting Revenue Intelligence,
Forecasting, Executive Reporting, Customer Analytics,
Product Analytics and Seller Performance.';


-- =============================================================================
-- VALIDATION QUERIES
-- =============================================================================

-- Verify table exists

SELECT

    table_schema,

    table_name

FROM information_schema.tables

WHERE table_schema = 'analytics'

AND table_name = 'fact_sales';


-- Verify constraints

SELECT

    constraint_name,

    constraint_type

FROM information_schema.table_constraints

WHERE table_schema = 'analytics'

AND table_name = 'fact_sales'

ORDER BY constraint_type;


-- Verify indexes

SELECT

    indexname,

    indexdef

FROM pg_indexes

WHERE schemaname = 'analytics'

AND tablename = 'fact_sales'

ORDER BY indexname;


-- Verify metadata

SELECT

    ordinal_position,

    column_name,

    data_type,

    is_nullable

FROM information_schema.columns

WHERE table_schema = 'analytics'

AND table_name = 'fact_sales'

ORDER BY ordinal_position;


-- =============================================================================
-- SAMPLE ANALYTICS QUERIES
-- =============================================================================

-- Total Revenue

SELECT

    SUM(net_sales_amount) AS total_revenue

FROM analytics.fact_sales;


-- Revenue by Month

SELECT

    d.year_month,

    SUM(f.net_sales_amount) AS revenue

FROM analytics.fact_sales f

INNER JOIN analytics.dim_date d

ON f.date_key = d.date_key

GROUP BY d.year_month

ORDER BY d.year_month;


-- Revenue by Product Category

SELECT

    p.product_category_english,

    SUM(f.net_sales_amount) AS revenue

FROM analytics.fact_sales f

INNER JOIN analytics.dim_product p

ON f.product_sk = p.product_sk

GROUP BY p.product_category_english

ORDER BY revenue DESC;


-- Revenue by Seller

SELECT

    s.seller_state,

    SUM(f.net_sales_amount) AS revenue

FROM analytics.fact_sales f

INNER JOIN analytics.dim_seller s

ON f.seller_sk = s.seller_sk

GROUP BY s.seller_state

ORDER BY revenue DESC;


-- Revenue by Customer State

SELECT

    c.customer_state,

    SUM(f.net_sales_amount) AS revenue

FROM analytics.fact_sales f

INNER JOIN analytics.dim_customer c

ON f.customer_sk = c.customer_sk

GROUP BY c.customer_state

ORDER BY revenue DESC;


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
-- • Star schema fact table
-- • Order-item grain
-- • Four conformed dimensions
-- • Fully additive measures
-- • Enterprise indexing
-- • PostgreSQL optimized
-- • Power BI ready
-- • Revenue Intelligence ready
-- • Executive Reporting ready
--
-- =============================================================================
-- END OF FILE
-- =============================================================================
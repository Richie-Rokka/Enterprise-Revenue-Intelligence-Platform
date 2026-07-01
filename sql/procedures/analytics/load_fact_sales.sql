/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_fact_sales.sql
Schema      : analytics
Object      : load_fact_sales
Purpose     : Load Enterprise Sales Fact Table
Strategy    : Incremental / Idempotent (DELETE + INSERT)
Grain       : One Row Per Order Item
Platform    : PostgreSQL 18
Version     : 4.1.0

Source Tables
-------------
raw.orders
raw.order_items
raw.order_payments

Dimension Tables
----------------
analytics.dim_customer
analytics.dim_product
analytics.dim_seller
analytics.dim_date

Target
------
analytics.fact_sales

===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.load_fact_sales()

LANGUAGE plpgsql

AS
$$

DECLARE

    v_run_id BIGINT;

    v_start_time TIMESTAMPTZ := clock_timestamp();
    v_end_time TIMESTAMPTZ;

    v_rows_staged INTEGER := 0;
    v_rows_deleted INTEGER := 0;
    v_rows_inserted INTEGER := 0;
    v_rows_processed INTEGER := 0;

    v_duration_seconds NUMERIC(12,3);

BEGIN

    ----------------------------------------------------------------------------
    -- STEP 0 : INITIALIZE ETL RUN
    ----------------------------------------------------------------------------

    SELECT nextval('analytics.etl_run_history_run_id_seq')
    INTO v_run_id;

    ----------------------------------------------------------------------------
    -- STEP 1 : CREATE STAGING TABLE
    ----------------------------------------------------------------------------

    DROP TABLE IF EXISTS tmp_fact_sales_stage;

    CREATE TEMP TABLE tmp_fact_sales_stage
    (
        order_id VARCHAR(50),
        order_item_id INTEGER,

        date_key INTEGER,
        customer_sk INTEGER,
        product_sk INTEGER,
        seller_sk INTEGER,

        payment_type TEXT,
        order_status VARCHAR(30),

        quantity INTEGER,

        item_price NUMERIC(12,2),
        freight_value NUMERIC(12,2),

        gross_sales_amount NUMERIC(12,2),
        net_sales_amount NUMERIC(12,2),

        payment_value NUMERIC(12,2),
        average_selling_price NUMERIC(12,2),
        freight_percentage NUMERIC(10,4)

    )
    ON COMMIT DROP;

    ----------------------------------------------------------------------------
    -- STEP 2 : BUILD STAGING DATASET
    ----------------------------------------------------------------------------

    WITH payment_summary AS
    (

        SELECT
            op.order_id,
            SUM(op.payment_value)::NUMERIC(12,2) AS payment_value,
            STRING_AGG(
                DISTINCT op.payment_type,
                ', '
                ORDER BY op.payment_type
            ) AS payment_type

        FROM raw.order_payments op

        GROUP BY op.order_id

    ),

    source_sales AS
    (

        SELECT
            oi.order_id,
            oi.order_item_id,
            oi.product_id,
            oi.seller_id,
            o.customer_id,
            DATE(o.order_purchase_timestamp) AS order_date,
            o.order_status,
            oi.price AS item_price,
            oi.freight_value,
            ps.payment_type,
            ps.payment_value

        FROM raw.order_items oi

        INNER JOIN raw.orders o
            ON oi.order_id = o.order_id

        LEFT JOIN payment_summary ps
            ON oi.order_id = ps.order_id

    ),

    resolved_dimensions AS
    (

        SELECT
            s.order_id,
            s.order_item_id,

            dd.date_key,
            dc.customer_sk,
            dp.product_sk,
            ds.seller_sk,

            s.payment_type,
            s.order_status,

            1 AS quantity,

            s.item_price,
            s.freight_value,

            (s.item_price + s.freight_value)::NUMERIC(12,2)
                AS gross_sales_amount,

            s.item_price::NUMERIC(12,2)
                AS net_sales_amount,

            COALESCE(s.payment_value,0)::NUMERIC(12,2)
                AS payment_value,

            s.item_price::NUMERIC(12,2)
                AS average_selling_price,

            CASE
                WHEN s.item_price = 0 THEN NULL
                ELSE ROUND(
                        (s.freight_value / s.item_price)::NUMERIC,
                        4
                     )
            END AS freight_percentage

        FROM source_sales s

        INNER JOIN analytics.dim_date dd
            ON dd.calendar_date = s.order_date

        INNER JOIN analytics.dim_customer dc
            ON dc.customer_id = s.customer_id
           AND dc.is_current = TRUE

        INNER JOIN analytics.dim_product dp
            ON dp.product_id = s.product_id
           AND dp.is_current = TRUE

        INNER JOIN analytics.dim_seller ds
            ON ds.seller_id = s.seller_id
           AND ds.is_current = TRUE

    )

    INSERT INTO tmp_fact_sales_stage
    (
        order_id, order_item_id,
        date_key, customer_sk, product_sk, seller_sk,
        payment_type, order_status,
        quantity,
        item_price, freight_value,
        gross_sales_amount, net_sales_amount,
        payment_value,
        average_selling_price,
        freight_percentage
    )

    SELECT
        order_id, order_item_id,
        date_key, customer_sk, product_sk, seller_sk,
        payment_type, order_status,
        quantity,
        item_price, freight_value,
        gross_sales_amount, net_sales_amount,
        payment_value,
        average_selling_price,
        freight_percentage

    FROM resolved_dimensions;

    GET DIAGNOSTICS v_rows_staged = ROW_COUNT;

    ----------------------------------------------------------------------------
    -- STEP 3 : DELETE EXISTING BUSINESS KEYS
    ----------------------------------------------------------------------------

    DELETE FROM analytics.fact_sales f

    USING tmp_fact_sales_stage s

    WHERE f.order_id = s.order_id
      AND f.order_item_id = s.order_item_id;

    GET DIAGNOSTICS v_rows_deleted = ROW_COUNT;

    ----------------------------------------------------------------------------
    -- STEP 4 : INSERT REFRESHED FACT ROWS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.fact_sales
    (
        order_id, order_item_id,
        date_key, customer_sk, product_sk, seller_sk,
        payment_type, order_status,
        quantity,
        item_price, freight_value,
        gross_sales_amount, net_sales_amount,
        payment_value,
        average_selling_price,
        freight_percentage,
        created_timestamp
    )

    SELECT
        s.order_id,
        s.order_item_id,
        s.date_key,
        s.customer_sk,
        s.product_sk,
        s.seller_sk,
        s.payment_type,
        s.order_status,
        s.quantity,
        s.item_price,
        s.freight_value,
        s.gross_sales_amount,
        s.net_sales_amount,
        s.payment_value,
        s.average_selling_price,
        s.freight_percentage,
        CURRENT_TIMESTAMP

    FROM tmp_fact_sales_stage s;

    GET DIAGNOSTICS v_rows_inserted = ROW_COUNT;

    ----------------------------------------------------------------------------
    -- STEP 5 : EXECUTION METRICS
    ----------------------------------------------------------------------------

    v_rows_processed := v_rows_staged;

    v_end_time := clock_timestamp();

    v_duration_seconds :=
    ROUND
    (
        EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC,
        3
    );

    ----------------------------------------------------------------------------
    -- STEP 6 : UPDATE OPTIMIZER STATISTICS
    ----------------------------------------------------------------------------

    ANALYZE analytics.fact_sales;

    ----------------------------------------------------------------------------
    -- STEP 7 : RECORD ETL RUN HISTORY (PARENT TABLE)
    ----------------------------------------------------------------------------

    INSERT INTO analytics.etl_run_history
    (
        run_id,
        pipeline_name,
        start_time,
        end_time,
        duration_seconds,
        status,
        total_tables,
        total_rows_loaded,
        created_at
    )

    VALUES
    (
        v_run_id,
        'analytics.load_fact_sales',
        v_start_time,
        v_end_time,
        v_duration_seconds,
        'SUCCESS',
        1,
        v_rows_inserted,
        CURRENT_TIMESTAMP
    );

    ----------------------------------------------------------------------------
    -- STEP 8 : RECORD TABLE LOAD HISTORY (CHILD TABLE)
    ----------------------------------------------------------------------------

    INSERT INTO analytics.table_load_history
    (
        run_id,
        table_name,
        rows_loaded,
        load_status,
        load_duration_seconds,
        created_at
    )

    VALUES
    (
        v_run_id,
        'analytics.fact_sales',
        v_rows_inserted,
        'SUCCESS',
        v_duration_seconds,
        CURRENT_TIMESTAMP
    );

    ----------------------------------------------------------------------------
    -- STEP 9 : EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ANALYTICS - FACT SALES LOAD';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Platform              : PostgreSQL 18';
    RAISE NOTICE 'Procedure             : analytics.load_fact_sales';
    RAISE NOTICE 'Run ID                : %', v_run_id;
    RAISE NOTICE 'Status                : SUCCESS';
    RAISE NOTICE 'Target Table          : analytics.fact_sales';
    RAISE NOTICE 'Rows Staged           : %', v_rows_staged;
    RAISE NOTICE 'Rows Deleted          : %', v_rows_deleted;
    RAISE NOTICE 'Rows Inserted         : %', v_rows_inserted;
    RAISE NOTICE 'Rows Processed        : %', v_rows_processed;
    RAISE NOTICE 'Started               : %', v_start_time;
    RAISE NOTICE 'Completed             : %', v_end_time;
    RAISE NOTICE 'Execution Time (sec)  : %', v_duration_seconds;
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

    EXCEPTION

    WHEN OTHERS THEN

        v_end_time := clock_timestamp();

        v_duration_seconds :=
        ROUND
        (
            EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC,
            3
        );

    BEGIN

        INSERT INTO analytics.etl_run_history
        (
            run_id,
            pipeline_name,
            start_time,
            end_time,
            duration_seconds,
            status,
            total_tables,
            total_rows_loaded,
            created_at
        )

        VALUES
        (
            v_run_id,
            'analytics.load_fact_sales',
            v_start_time,
            v_end_time,
            v_duration_seconds,
            'FAILED',
            1,
            v_rows_inserted,
            CURRENT_TIMESTAMP
        );

    EXCEPTION
        WHEN OTHERS THEN
            NULL;
    END;

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ANALYTICS - FACT SALES LOAD FAILED';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Run ID               : %', v_run_id;
    RAISE NOTICE 'SQLSTATE             : %', SQLSTATE;
    RAISE NOTICE 'Error                : %', SQLERRM;
    RAISE NOTICE 'Execution Time (sec) : %', v_duration_seconds;
    RAISE NOTICE '============================================================';

    RAISE;

END;

$$;

----------------------------------------------------------------------------
-- EXAMPLE EXECUTION
----------------------------------------------------------------------------

CALL analytics.load_fact_sales();

----------------------------------------------------------------------------
-- VALIDATION QUERIES
----------------------------------------------------------------------------


-- Total Fact Rows

SELECT
    COUNT(*) AS total_rows
FROM analytics.fact_sales;

----------------------------------------------------------------------------
-- Duplicate Business Keys (Should Return Zero Rows)
----------------------------------------------------------------------------

SELECT
    order_id,
    order_item_id,
    COUNT(*) AS duplicate_count
FROM analytics.fact_sales
GROUP BY
    order_id,
    order_item_id
HAVING COUNT(*) > 1;

----------------------------------------------------------------------------
-- Revenue Reconciliation
----------------------------------------------------------------------------

SELECT
    SUM(gross_sales_amount) AS gross_sales_amount,
    SUM(net_sales_amount) AS net_sales_amount,
    SUM(freight_value) AS total_freight,
    SUM(payment_value) AS total_payments
FROM analytics.fact_sales;

----------------------------------------------------------------------------
-- Monthly Revenue
----------------------------------------------------------------------------

SELECT
    d.year_month,
    COUNT(*) AS order_items,
    SUM(f.quantity) AS quantity_sold,
    SUM(f.net_sales_amount) AS revenue,
    SUM(f.gross_sales_amount) AS gross_revenue
FROM analytics.fact_sales f

INNER JOIN analytics.dim_date d
    ON f.date_key = d.date_key

GROUP BY
    d.year_month

ORDER BY
    d.year_month;

----------------------------------------------------------------------------
-- Product Performance
----------------------------------------------------------------------------

SELECT
    p.product_category_english,
    COUNT(*) AS order_items,
    SUM(f.quantity) AS quantity_sold,
    SUM(f.net_sales_amount) AS revenue,
    AVG(f.average_selling_price) AS average_selling_price

FROM analytics.fact_sales f

INNER JOIN analytics.dim_product p
    ON f.product_sk = p.product_sk

GROUP BY
    p.product_category_english

ORDER BY
    revenue DESC;

----------------------------------------------------------------------------
-- Seller Performance
----------------------------------------------------------------------------

SELECT
    s.seller_region,
    COUNT(*) AS order_items,
    SUM(f.net_sales_amount) AS revenue,
    SUM(f.freight_value) AS freight_amount

FROM analytics.fact_sales f

INNER JOIN analytics.dim_seller s
    ON f.seller_sk = s.seller_sk

GROUP BY
    s.seller_region

ORDER BY
    revenue DESC;

----------------------------------------------------------------------------
-- Customer Performance
----------------------------------------------------------------------------

SELECT
    c.customer_region,
    COUNT(DISTINCT f.customer_sk) AS unique_customers,
    COUNT(*) AS order_items,
    SUM(f.net_sales_amount) AS revenue

FROM analytics.fact_sales f

INNER JOIN analytics.dim_customer c
    ON f.customer_sk = c.customer_sk

GROUP BY
    c.customer_region

ORDER BY
    revenue DESC;

----------------------------------------------------------------------------
-- Order Status Distribution
----------------------------------------------------------------------------

SELECT
    order_status,
    COUNT(*) AS total_order_items,
    SUM(net_sales_amount) AS revenue

FROM analytics.fact_sales

GROUP BY
    order_status

ORDER BY
    revenue DESC;

----------------------------------------------------------------------------
-- Payment Type Analysis
----------------------------------------------------------------------------

SELECT
    payment_type,
    COUNT(*) AS order_items,
    SUM(payment_value) AS payment_amount

FROM analytics.fact_sales

GROUP BY
    payment_type

ORDER BY
    payment_amount DESC;

----------------------------------------------------------------------------
-- Freight Analysis
----------------------------------------------------------------------------

SELECT
    ROUND(AVG(freight_percentage),4) AS average_freight_percentage,
    SUM(freight_value) AS total_freight,
    AVG(freight_value) AS average_freight,
    MAX(freight_value) AS maximum_freight

FROM analytics.fact_sales;

----------------------------------------------------------------------------
-- Missing Dimension Keys
----------------------------------------------------------------------------

SELECT
    SUM(CASE WHEN customer_sk IS NULL THEN 1 ELSE 0 END) AS missing_customer_keys,
    SUM(CASE WHEN product_sk IS NULL THEN 1 ELSE 0 END) AS missing_product_keys,
    SUM(CASE WHEN seller_sk IS NULL THEN 1 ELSE 0 END) AS missing_seller_keys,
    SUM(CASE WHEN date_key IS NULL THEN 1 ELSE 0 END) AS missing_date_keys
FROM analytics.fact_sales;

----------------------------------------------------------------------------
-- Fact Table Summary
----------------------------------------------------------------------------

SELECT
    MIN(created_timestamp) AS first_load_timestamp,
    MAX(created_timestamp) AS latest_load_timestamp,
    COUNT(*) AS total_fact_rows,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_sk) AS total_customers,
    COUNT(DISTINCT product_sk) AS total_products,
    COUNT(DISTINCT seller_sk) AS total_sellers
FROM analytics.fact_sales;

----------------------------------------------------------------------------
-- CHANGE LOG
----------------------------------------------------------------------------

/*

Version        : 4.1.0
Platform       : PostgreSQL 18
Object         : analytics.load_fact_sales

Enhancements
------------
• Enterprise CTE architecture
• One row per order item
• Aggregated payment summary
• Temporary staging table
• DELETE + INSERT incremental strategy
• Idempotent loading
• SCD Type 2 dimension resolution
• Enterprise audit logging
• ETL run history integration
• Table load history integration
• Optimizer statistics refresh
• Enterprise execution summary
• Validation suite
• Compact SQL formatting
• PostgreSQL 18 compatible

*/

----------------------------------------------------------------------------
-- END OF FILE
----------------------------------------------------------------------------
/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_dim_date.sql
Schema      : analytics
Object      : load_dim_date
Purpose     : Load Enterprise Date Dimension
Strategy    : Incremental / Idempotent
Source      : System Generated
Author      : Abodunrin Oketade
Version     : 3.1.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.load_dim_date
(
    IN p_start_year INTEGER,
    IN p_end_year   INTEGER
)

LANGUAGE plpgsql

AS
$$

DECLARE
    v_start_date DATE;
    v_end_date DATE;

    v_total_dates INTEGER := 0;
    v_existing_rows INTEGER := 0;
    v_rows_inserted INTEGER := 0;

    v_start_time TIMESTAMPTZ;
    v_end_time TIMESTAMPTZ;

BEGIN

    v_start_time := clock_timestamp();

    ----------------------------------------------------------------------------
    -- VALIDATION
    ----------------------------------------------------------------------------

    IF p_start_year > p_end_year THEN
        RAISE EXCEPTION
            'Start year (%) cannot be greater than End year (%)',
            p_start_year,
            p_end_year;
    END IF;

    IF p_start_year < 1900 THEN
        RAISE EXCEPTION
            'Start year must be >= 1900.';
    END IF;

    IF p_end_year > 2100 THEN
        RAISE EXCEPTION
            'End year must be <= 2100.';
    END IF;

    ----------------------------------------------------------------------------
    -- DATE RANGE
    ----------------------------------------------------------------------------

    v_start_date := MAKE_DATE(p_start_year, 1, 1);
    v_end_date := MAKE_DATE(p_end_year, 12, 31);

    v_total_dates := (v_end_date - v_start_date) + 1;

    ----------------------------------------------------------------------------
    -- EXISTING ROWS
    ----------------------------------------------------------------------------

    SELECT COUNT(*)
    INTO v_existing_rows
    FROM analytics.dim_date
    WHERE calendar_date BETWEEN v_start_date AND v_end_date;

    ----------------------------------------------------------------------------
    -- LOAD MISSING DATES ONLY
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_date (
        date_key, calendar_date, day_of_month, day_name,
        day_name_short, day_of_week, day_of_year, week_of_month,
        week_of_year, iso_week, month_number, month_number_in_quarter,
        month_name, month_name_short, month_start_date, month_end_date,
        days_in_month, quarter_number, quarter_name, quarter_start_date,
        quarter_end_date, semester_number, semester_name, year_number,
        year_start_date, year_end_date, is_leap_year, is_weekday,
        is_weekend, is_business_day, is_month_start, is_month_end,
        is_quarter_start, is_quarter_end, is_year_start, is_year_end,
        is_first_half_year, is_second_half_year, fiscal_year,
        fiscal_quarter, fiscal_month, year_month, year_quarter,
        month_sort_key, quarter_sort_key, year_sort_key,
        is_holiday, holiday_name, created_timestamp, updated_timestamp
    )

    SELECT
        TO_CHAR(d.calendar_date, 'YYYYMMDD')::INTEGER,
        d.calendar_date,
        EXTRACT(DAY FROM d.calendar_date)::SMALLINT,
        TO_CHAR(d.calendar_date, 'FMDay'),
        TO_CHAR(d.calendar_date, 'Dy'),
        EXTRACT(ISODOW FROM d.calendar_date)::SMALLINT,
        EXTRACT(DOY FROM d.calendar_date)::SMALLINT,
        ((EXTRACT(DAY FROM d.calendar_date) - 1) / 7 + 1)::SMALLINT,
        EXTRACT(WEEK FROM d.calendar_date)::SMALLINT,
        EXTRACT(WEEK FROM d.calendar_date)::SMALLINT,
        EXTRACT(MONTH FROM d.calendar_date)::SMALLINT,
        ((EXTRACT(MONTH FROM d.calendar_date) - 1) % 3 + 1)::SMALLINT,
        TO_CHAR(d.calendar_date, 'FMMonth'),
        TO_CHAR(d.calendar_date, 'Mon'),
        DATE_TRUNC('month', d.calendar_date)::DATE,
        (DATE_TRUNC('month', d.calendar_date) + INTERVAL '1 month - 1 day')::DATE,
        EXTRACT(
            DAY FROM (
                DATE_TRUNC('month', d.calendar_date)
                + INTERVAL '1 month - 1 day'
            )
        )::SMALLINT,
        EXTRACT(QUARTER FROM d.calendar_date)::SMALLINT,
        'Q' || EXTRACT(QUARTER FROM d.calendar_date),
        DATE_TRUNC('quarter', d.calendar_date)::DATE,
        (DATE_TRUNC('quarter', d.calendar_date) + INTERVAL '3 months - 1 day')::DATE,
        CASE WHEN EXTRACT(MONTH FROM d.calendar_date) <= 6 THEN 1 ELSE 2 END,
        CASE WHEN EXTRACT(MONTH FROM d.calendar_date) <= 6 THEN 'H1' ELSE 'H2' END,
        EXTRACT(YEAR FROM d.calendar_date)::SMALLINT,
        DATE_TRUNC('year', d.calendar_date)::DATE,
        MAKE_DATE(EXTRACT(YEAR FROM d.calendar_date)::INTEGER, 12, 31),

        CASE
            WHEN (
                EXTRACT(YEAR FROM d.calendar_date)::INTEGER % 400 = 0
                OR (
                    EXTRACT(YEAR FROM d.calendar_date)::INTEGER % 4 = 0
                    AND EXTRACT(YEAR FROM d.calendar_date)::INTEGER % 100 <> 0
                )
            )
            THEN TRUE
            ELSE FALSE
        END,

        EXTRACT(ISODOW FROM d.calendar_date) <= 5,
        EXTRACT(ISODOW FROM d.calendar_date) >= 6,
        EXTRACT(ISODOW FROM d.calendar_date) <= 5,

        d.calendar_date = DATE_TRUNC('month', d.calendar_date)::DATE,
        d.calendar_date = (DATE_TRUNC('month', d.calendar_date) + INTERVAL '1 month - 1 day')::DATE,
        d.calendar_date = DATE_TRUNC('quarter', d.calendar_date)::DATE,
        d.calendar_date = (DATE_TRUNC('quarter', d.calendar_date) + INTERVAL '3 months - 1 day')::DATE,
        d.calendar_date = DATE_TRUNC('year', d.calendar_date)::DATE,
        d.calendar_date = MAKE_DATE(EXTRACT(YEAR FROM d.calendar_date)::INTEGER, 12, 31),

        EXTRACT(MONTH FROM d.calendar_date) <= 6,
        EXTRACT(MONTH FROM d.calendar_date) >= 7,

        EXTRACT(YEAR FROM d.calendar_date)::SMALLINT,
        EXTRACT(QUARTER FROM d.calendar_date)::SMALLINT,
        EXTRACT(MONTH FROM d.calendar_date)::SMALLINT,

        TO_CHAR(d.calendar_date, 'YYYY-MM'),
        TO_CHAR(d.calendar_date, 'YYYY') || '-Q' || EXTRACT(QUARTER FROM d.calendar_date),

        (
            EXTRACT(YEAR FROM d.calendar_date)::INTEGER * 100
            + EXTRACT(MONTH FROM d.calendar_date)::INTEGER
        ),

        (
            EXTRACT(YEAR FROM d.calendar_date)::INTEGER * 10
            + EXTRACT(QUARTER FROM d.calendar_date)::INTEGER
        ),

        EXTRACT(YEAR FROM d.calendar_date)::INTEGER,

        FALSE,
        NULL,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM (
        SELECT generate_series(
            v_start_date,
            v_end_date,
            INTERVAL '1 day'
        )::DATE AS calendar_date
    ) d

    ON CONFLICT (date_key)
    DO NOTHING;

    ----------------------------------------------------------------------------
    -- CAPTURE METRICS
    ----------------------------------------------------------------------------

    GET DIAGNOSTICS v_rows_inserted = ROW_COUNT;

    ANALYZE analytics.dim_date;

    ----------------------------------------------------------------------------
    -- EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    v_end_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ANALYTICS - DATE DIMENSION LOAD';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Status           : SUCCESS';
    RAISE NOTICE 'Target Table     : analytics.dim_date';
    RAISE NOTICE 'Date Range       : % -> %', v_start_date, v_end_date;
    RAISE NOTICE 'Dates Requested  : %', v_total_dates;
    RAISE NOTICE 'Already Existing : %', v_existing_rows;
    RAISE NOTICE 'Rows Inserted    : %', v_rows_inserted;
    RAISE NOTICE 'Total Available  : %', v_existing_rows + v_rows_inserted;
    RAISE NOTICE 'Execution Time   : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION

    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP ANALYTICS - DATE DIMENSION LOAD FAILED';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'SQLSTATE : %', SQLSTATE;
        RAISE NOTICE 'MESSAGE  : %', SQLERRM;
        RAISE NOTICE '============================================================';
        RAISE NOTICE '';

        RAISE;

END;

$$;


-- ============================================================================
-- EXAMPLE EXECUTION
-- ============================================================================

CALL analytics.load_dim_date(2015, 2045);


-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Total rows

SELECT COUNT(*) AS total_dates
FROM analytics.dim_date;


-- Date range

SELECT
MIN(calendar_date) AS minimum_date,
MAX(calendar_date) AS maximum_date
FROM analytics.dim_date;


-- Missing dates

SELECT COUNT(*) AS missing_dates
FROM (
    SELECT generate_series(
        (SELECT MIN(calendar_date) FROM analytics.dim_date),
        (SELECT MAX(calendar_date) FROM analytics.dim_date),
        INTERVAL '1 day'
    )::DATE AS calendar_date
) d
LEFT JOIN analytics.dim_date x
    ON d.calendar_date = x.calendar_date
WHERE x.calendar_date IS NULL;


-- Leap year validation

SELECT
    year_number,
    COUNT(*) AS days_in_year
FROM analytics.dim_date
GROUP BY year_number
ORDER BY year_number;


-- Business day summary

SELECT
    is_business_day,
    COUNT(*) AS total_days
FROM analytics.dim_date
GROUP BY is_business_day;


-- Sample data

SELECT *
FROM analytics.dim_date
ORDER BY calendar_date
LIMIT 20;


-- ============================================================================
-- CHANGE LOG
-- ============================================================================
--
-- Version : 3.1.0
--
-- Improvements
-- ------------
-- • Removed TRUNCATE TABLE
-- • Idempotent loading strategy
-- • ON CONFLICT (date_key) DO NOTHING
-- • Safe with foreign key constraints
-- • Enterprise execution metrics
-- • Improved validation queries
-- • PostgreSQL optimizer refresh
-- • Unlimited reruns supported
--
-- ============================================================================
-- END OF FILE
-- ============================================================================
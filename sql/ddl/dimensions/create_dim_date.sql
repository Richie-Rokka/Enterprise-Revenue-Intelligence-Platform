/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module:
    create_dim_date.sql

Schema:
    analytics

Object:
    dim_date

Purpose:
    Creates the Enterprise Date Dimension.

Description:
    The Enterprise Date Dimension provides standardized calendar,
    fiscal, business and analytical attributes for all enterprise
    reporting.

Business Process
----------------
Enterprise Time Intelligence

Grain
-----
One record represents one calendar day.

Primary Key
-----------
date_key

Natural Key
-----------
calendar_date

SCD Strategy
------------
Type 0

Refresh Strategy
----------------
Full Refresh

Source
------
System Generated

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

DROP TABLE IF EXISTS analytics.dim_date CASCADE;


-- =============================================================================
-- CREATE TABLE
-- =============================================================================

CREATE TABLE analytics.dim_date
(

    -------------------------------------------------------------------------
    -- KEYS
    -------------------------------------------------------------------------

    date_key                        INTEGER             NOT NULL,

    calendar_date                   DATE                NOT NULL,


    -------------------------------------------------------------------------
    -- DAY ATTRIBUTES
    -------------------------------------------------------------------------

    day_of_month                    SMALLINT            NOT NULL,

    day_name                        VARCHAR(15)         NOT NULL,

    day_name_short                  VARCHAR(3)          NOT NULL,

    day_of_week                     SMALLINT            NOT NULL,

    day_of_year                     SMALLINT            NOT NULL,

    week_of_month                   SMALLINT            NOT NULL,

    week_of_year                    SMALLINT            NOT NULL,

    iso_week                        SMALLINT            NOT NULL,


    -------------------------------------------------------------------------
    -- MONTH ATTRIBUTES
    -------------------------------------------------------------------------

    month_number                    SMALLINT            NOT NULL,

    month_number_in_quarter         SMALLINT            NOT NULL,

    month_name                      VARCHAR(20)         NOT NULL,

    month_name_short                VARCHAR(3)          NOT NULL,

    month_start_date                DATE                NOT NULL,

    month_end_date                  DATE                NOT NULL,

    days_in_month                   SMALLINT            NOT NULL,


    -------------------------------------------------------------------------
    -- QUARTER ATTRIBUTES
    -------------------------------------------------------------------------

    quarter_number                  SMALLINT            NOT NULL,

    quarter_name                    VARCHAR(2)          NOT NULL,

    quarter_start_date              DATE                NOT NULL,

    quarter_end_date                DATE                NOT NULL,


    -------------------------------------------------------------------------
    -- SEMESTER
    -------------------------------------------------------------------------

    semester_number                 SMALLINT            NOT NULL,

    semester_name                   VARCHAR(2)          NOT NULL,


    -------------------------------------------------------------------------
    -- YEAR
    -------------------------------------------------------------------------

    year_number                     SMALLINT            NOT NULL,

    year_start_date                 DATE                NOT NULL,

    year_end_date                   DATE                NOT NULL,

    is_leap_year                    BOOLEAN             NOT NULL,


    -------------------------------------------------------------------------
    -- BUSINESS CALENDAR
    -------------------------------------------------------------------------

    is_weekday                      BOOLEAN             NOT NULL,

    is_weekend                      BOOLEAN             NOT NULL,

    is_business_day                 BOOLEAN             NOT NULL,

    is_month_start                  BOOLEAN             NOT NULL,

    is_month_end                    BOOLEAN             NOT NULL,

    is_quarter_start                BOOLEAN             NOT NULL,

    is_quarter_end                  BOOLEAN             NOT NULL,

    is_year_start                   BOOLEAN             NOT NULL,

    is_year_end                     BOOLEAN             NOT NULL,

    is_first_half_year              BOOLEAN             NOT NULL,

    is_second_half_year             BOOLEAN             NOT NULL,


    -------------------------------------------------------------------------
    -- FISCAL CALENDAR
    -------------------------------------------------------------------------

    fiscal_year                     SMALLINT            NOT NULL,

    fiscal_quarter                  SMALLINT            NOT NULL,

    fiscal_month                    SMALLINT            NOT NULL,


    -------------------------------------------------------------------------
    -- ANALYTICS
    -------------------------------------------------------------------------

    year_month                      CHAR(7)             NOT NULL,

    year_quarter                    CHAR(7)             NOT NULL,

    month_sort_key                  INTEGER             NOT NULL,

    quarter_sort_key                INTEGER             NOT NULL,

    year_sort_key                   INTEGER             NOT NULL,


    -------------------------------------------------------------------------
    -- HOLIDAY SUPPORT
    -------------------------------------------------------------------------

    is_holiday                      BOOLEAN             NOT NULL
                                        DEFAULT FALSE,

    holiday_name                    VARCHAR(100),


    -------------------------------------------------------------------------
    -- AUDIT
    -------------------------------------------------------------------------

    created_timestamp               TIMESTAMPTZ         NOT NULL
                                        DEFAULT CURRENT_TIMESTAMP,

    updated_timestamp               TIMESTAMPTZ         NOT NULL
                                        DEFAULT CURRENT_TIMESTAMP

);

-- =============================================================================
-- PRIMARY KEY
-- =============================================================================

ALTER TABLE analytics.dim_date
ADD CONSTRAINT pk_dim_date
PRIMARY KEY (date_key);


-- =============================================================================
-- UNIQUE CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_date
ADD CONSTRAINT uq_dim_date_calendar_date
UNIQUE (calendar_date);


-- =============================================================================
-- CHECK CONSTRAINTS
-- =============================================================================

ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_day_of_month
CHECK
(
    day_of_month BETWEEN 1 AND 31
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_day_of_week
CHECK
(
    day_of_week BETWEEN 1 AND 7
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_day_of_year
CHECK
(
    day_of_year BETWEEN 1 AND 366
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_week_of_month
CHECK
(
    week_of_month BETWEEN 1 AND 6
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_week_of_year
CHECK
(
    week_of_year BETWEEN 1 AND 53
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_iso_week
CHECK
(
    iso_week BETWEEN 1 AND 53
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_month_number
CHECK
(
    month_number BETWEEN 1 AND 12
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_month_number_in_quarter
CHECK
(
    month_number_in_quarter BETWEEN 1 AND 3
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_quarter_number
CHECK
(
    quarter_number BETWEEN 1 AND 4
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_semester_number
CHECK
(
    semester_number BETWEEN 1 AND 2
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_fiscal_month
CHECK
(
    fiscal_month BETWEEN 1 AND 12
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_fiscal_quarter
CHECK
(
    fiscal_quarter BETWEEN 1 AND 4
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_year_month
CHECK
(
    year_month ~ '^[0-9]{4}-[0-9]{2}$'
);


ALTER TABLE analytics.dim_date
ADD CONSTRAINT chk_dim_date_year_quarter
CHECK
(
    year_quarter ~ '^[0-9]{4}-Q[1-4]$'
);


-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================

CREATE INDEX idx_dim_date_calendar_date
ON analytics.dim_date
(
    calendar_date
);


CREATE INDEX idx_dim_date_year
ON analytics.dim_date
(
    year_number
);


CREATE INDEX idx_dim_date_month
ON analytics.dim_date
(
    year_number,
    month_number
);


CREATE INDEX idx_dim_date_quarter
ON analytics.dim_date
(
    year_number,
    quarter_number
);


CREATE INDEX idx_dim_date_year_month
ON analytics.dim_date
(
    year_month
);


CREATE INDEX idx_dim_date_year_quarter
ON analytics.dim_date
(
    year_quarter
);


CREATE INDEX idx_dim_date_business_day
ON analytics.dim_date
(
    is_business_day
);


CREATE INDEX idx_dim_date_weekend
ON analytics.dim_date
(
    is_weekend
);


CREATE INDEX idx_dim_date_holiday
ON analytics.dim_date
(
    is_holiday
);


CREATE INDEX idx_dim_date_fiscal
ON analytics.dim_date
(
    fiscal_year,
    fiscal_quarter,
    fiscal_month
);


CREATE INDEX idx_dim_date_sort_keys
ON analytics.dim_date
(
    year_sort_key,
    quarter_sort_key,
    month_sort_key
);

-- =============================================================================
-- COLUMN COMMENTS
-- =============================================================================

COMMENT ON COLUMN analytics.dim_date.date_key IS
'Enterprise surrogate key in YYYYMMDD format.';

COMMENT ON COLUMN analytics.dim_date.calendar_date IS
'Calendar date represented by this row.';

COMMENT ON COLUMN analytics.dim_date.day_of_month IS
'Day number within the month.';

COMMENT ON COLUMN analytics.dim_date.day_name IS
'Full day name.';

COMMENT ON COLUMN analytics.dim_date.day_name_short IS
'Three-letter day abbreviation.';

COMMENT ON COLUMN analytics.dim_date.day_of_week IS
'ISO weekday where Monday = 1 and Sunday = 7.';

COMMENT ON COLUMN analytics.dim_date.day_of_year IS
'Sequential day within the calendar year.';

COMMENT ON COLUMN analytics.dim_date.week_of_month IS
'Week number within the month.';

COMMENT ON COLUMN analytics.dim_date.week_of_year IS
'Calendar week number.';

COMMENT ON COLUMN analytics.dim_date.iso_week IS
'ISO-8601 week number.';

COMMENT ON COLUMN analytics.dim_date.month_number IS
'Calendar month number.';

COMMENT ON COLUMN analytics.dim_date.month_number_in_quarter IS
'Month position within the quarter (1-3).';

COMMENT ON COLUMN analytics.dim_date.month_name IS
'Full month name.';

COMMENT ON COLUMN analytics.dim_date.month_name_short IS
'Three-letter month abbreviation.';

COMMENT ON COLUMN analytics.dim_date.month_start_date IS
'First day of the month.';

COMMENT ON COLUMN analytics.dim_date.month_end_date IS
'Last day of the month.';

COMMENT ON COLUMN analytics.dim_date.days_in_month IS
'Number of calendar days in the month.';

COMMENT ON COLUMN analytics.dim_date.quarter_number IS
'Calendar quarter number.';

COMMENT ON COLUMN analytics.dim_date.quarter_name IS
'Quarter label (Q1-Q4).';

COMMENT ON COLUMN analytics.dim_date.quarter_start_date IS
'First day of the quarter.';

COMMENT ON COLUMN analytics.dim_date.quarter_end_date IS
'Last day of the quarter.';

COMMENT ON COLUMN analytics.dim_date.semester_number IS
'Semester number (1 or 2).';

COMMENT ON COLUMN analytics.dim_date.semester_name IS
'Semester label (H1 or H2).';

COMMENT ON COLUMN analytics.dim_date.year_number IS
'Calendar year.';

COMMENT ON COLUMN analytics.dim_date.year_start_date IS
'First day of the calendar year.';

COMMENT ON COLUMN analytics.dim_date.year_end_date IS
'Last day of the calendar year.';

COMMENT ON COLUMN analytics.dim_date.is_leap_year IS
'TRUE when the year is a leap year.';

COMMENT ON COLUMN analytics.dim_date.is_business_day IS
'TRUE when the date is considered a business day.';

COMMENT ON COLUMN analytics.dim_date.is_weekend IS
'TRUE for Saturday and Sunday.';

COMMENT ON COLUMN analytics.dim_date.is_holiday IS
'TRUE when the date is designated as a holiday.';

COMMENT ON COLUMN analytics.dim_date.holiday_name IS
'Holiday description when applicable.';

COMMENT ON COLUMN analytics.dim_date.year_month IS
'Year-Month formatted as YYYY-MM.';

COMMENT ON COLUMN analytics.dim_date.year_quarter IS
'Year-Quarter formatted as YYYY-Qn.';

COMMENT ON COLUMN analytics.dim_date.created_timestamp IS
'Row creation timestamp.';

COMMENT ON COLUMN analytics.dim_date.updated_timestamp IS
'Row modification timestamp.';


-- =============================================================================
-- TABLE COMMENT
-- =============================================================================

COMMENT ON TABLE analytics.dim_date IS
'Enterprise Date Dimension supporting Revenue Intelligence, Executive Reporting,
Forecasting, Workforce Planning, Power BI Semantic Models, Time Intelligence,
Cohort Analysis and Machine Learning.';


-- =============================================================================
-- VALIDATION QUERIES
-- =============================================================================

-- Verify table definition

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'analytics'
AND table_name = 'dim_date';


-- Verify primary key

SELECT
    constraint_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'analytics'
AND table_name = 'dim_date'
ORDER BY constraint_type;


-- Verify indexes

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname='analytics'
AND tablename='dim_date'
ORDER BY indexname;


-- Verify column metadata

SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema='analytics'
AND table_name='dim_date'
ORDER BY ordinal_position;


-- =============================================================================
-- SAMPLE ANALYTICS QUERIES
-- =============================================================================

-- Business days per year

SELECT
    year_number,
    COUNT(*) AS business_days
FROM analytics.dim_date
WHERE is_business_day
GROUP BY year_number
ORDER BY year_number;


-- Month distribution

SELECT
    year_number,
    month_number,
    month_name,
    COUNT(*) AS days_in_month
FROM analytics.dim_date
GROUP BY
    year_number,
    month_number,
    month_name
ORDER BY
    year_number,
    month_number;


-- Quarter distribution

SELECT
    year_number,
    quarter_name,
    COUNT(*) AS days_in_quarter
FROM analytics.dim_date
GROUP BY
    year_number,
    quarter_name
ORDER BY
    year_number,
    quarter_name;


-- Leap year validation

SELECT
    year_number,
    COUNT(*) AS total_days
FROM analytics.dim_date
GROUP BY year_number
ORDER BY year_number;


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
-- • Intelligent YYYYMMDD surrogate key
-- • Calendar hierarchy
-- • Fiscal hierarchy
-- • Semester hierarchy
-- • Business calendar
-- • Holiday-ready architecture
-- • Enterprise constraints
-- • Enterprise indexing
-- • Power BI optimized
-- • Forecasting ready
-- • Machine Learning ready
-- • PostgreSQL optimized
--
-- =============================================================================
-- END OF FILE
-- =============================================================================
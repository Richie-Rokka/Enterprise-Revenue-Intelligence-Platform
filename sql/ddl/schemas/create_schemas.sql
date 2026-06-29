/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_schemas.sql

Purpose:
    Creates the core database schemas required by the Enterprise Revenue
    Intelligence Platform.

Schemas:
    - staging      : Landing zone for raw source data
    - analytics    : Enterprise dimensional data warehouse
    - monitoring   : Audit, pipeline execution, and data quality framework
    - metadata     : Platform metadata, deployment history, and registry

Dependencies:
    None

Execution:
    Executed by WarehouseManager during warehouse deployment.

Author:
    Abodunrin Oketade

Version:
    2.0.0
===============================================================================
*/

-- ============================================================================
-- Create Staging Schema
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS staging;

COMMENT ON SCHEMA staging IS
'Landing area for raw source system data before validation and transformation.';


-- ============================================================================
-- Create Analytics Schema
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS analytics;

COMMENT ON SCHEMA analytics IS
'Enterprise dimensional warehouse containing fact tables, dimensions, and analytical models.';


-- ============================================================================
-- Create Monitoring Schema
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS monitoring;

COMMENT ON SCHEMA monitoring IS
'Audit framework containing ETL history, pipeline monitoring, execution metrics, and data quality results.';


-- ============================================================================
-- Create Metadata Schema
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS metadata;

COMMENT ON SCHEMA metadata IS
'Platform metadata including warehouse versioning, deployment history, object registry, and configuration metadata.';


-- ============================================================================
-- Deployment Summary
-- ============================================================================

DO
$$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '===============================================================';
    RAISE NOTICE ' ERIP Warehouse Deployment';
    RAISE NOTICE '---------------------------------------------------------------';
    RAISE NOTICE ' Stage        : Schema Initialization';
    RAISE NOTICE ' Status       : SUCCESS';
    RAISE NOTICE ' Database     : %', current_database();
    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;
    RAISE NOTICE ' Schemas      : staging, analytics, monitoring, metadata';
    RAISE NOTICE '===============================================================';
    RAISE NOTICE '';
END
$$;
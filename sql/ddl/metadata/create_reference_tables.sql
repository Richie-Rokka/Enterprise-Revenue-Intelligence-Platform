/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    create_reference_tables.sql

Purpose:
    Creates enterprise reference tables used throughout the platform.

Description:
    These tables provide standardized reference values used for
    validation, governance, auditing and referential integrity.

Dependencies:
    create_schemas.sql

Execution Stage:
    Metadata Initialization

Author:
    Abodunrin Oketade

Version:
    2.0.0
===============================================================================
*/

-- ============================================================================
-- Validation Status Reference
-- ============================================================================

CREATE TABLE IF NOT EXISTS metadata.ref_validation_status
(
    validation_status_code VARCHAR(20) PRIMARY KEY,
    validation_status_name VARCHAR(100) NOT NULL,
    description            TEXT,
    display_order          INTEGER NOT NULL,
    is_active              BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE metadata.ref_validation_status IS
'Permitted validation states used throughout ERIP.';


-- ============================================================================
-- Record Status Reference
-- ============================================================================

CREATE TABLE IF NOT EXISTS metadata.ref_record_status
(
    record_status_code VARCHAR(20) PRIMARY KEY,
    record_status_name VARCHAR(100) NOT NULL,
    description        TEXT,
    display_order      INTEGER NOT NULL,
    is_active          BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE metadata.ref_record_status IS
'Operational lifecycle status for warehouse records.';


-- ============================================================================
-- Source System Reference
-- ============================================================================

CREATE TABLE IF NOT EXISTS metadata.ref_source_system
(
    source_system_code VARCHAR(50) PRIMARY KEY,
    source_system_name VARCHAR(150) NOT NULL,
    description        TEXT,
    is_active          BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE metadata.ref_source_system IS
'Registered source systems that feed the platform.';


-- ============================================================================
-- ETL Version Reference
-- ============================================================================

CREATE TABLE IF NOT EXISTS metadata.ref_etl_version
(
    etl_version VARCHAR(20) PRIMARY KEY,
    description TEXT,
    release_date DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE metadata.ref_etl_version IS
'Registered ETL framework versions.';


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
    RAISE NOTICE ' Stage        : Metadata Initialization';
    RAISE NOTICE ' Status       : SUCCESS';
    RAISE NOTICE ' Object       : Reference Tables';
    RAISE NOTICE ' Database     : %', current_database();
    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;
    RAISE NOTICE ' Next Stage   : Seed Reference Data';
    RAISE NOTICE '===============================================================';
    RAISE NOTICE '';

END
$$;
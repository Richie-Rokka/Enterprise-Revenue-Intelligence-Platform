/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

File:
    seed_reference_data.sql

Purpose:
    Seeds enterprise reference tables.

Dependencies:
    create_reference_tables.sql

Execution Stage:
    Metadata Seed

Author:
    Abodunrin Oketade

Version:
    2.0.0
===============================================================================
*/

-- ============================================================================
-- Validation Status
-- ============================================================================

INSERT INTO metadata.ref_validation_status
VALUES
('PENDING','Pending Validation','Awaiting validation',1,TRUE),
('VALID','Valid','Passed validation',2,TRUE),
('INVALID','Invalid','Failed validation',3,TRUE),
('REJECTED','Rejected','Rejected during processing',4,TRUE)
ON CONFLICT DO NOTHING;


-- ============================================================================
-- Record Status
-- ============================================================================

INSERT INTO metadata.ref_record_status
VALUES
('ACTIVE','Active','Current active record',1,TRUE),
('UPDATED','Updated','Superseded by newer version',2,TRUE),
('DELETED','Deleted','Soft deleted record',3,TRUE),
('ARCHIVED','Archived','Archived historical record',4,TRUE)
ON CONFLICT DO NOTHING;


-- ============================================================================
-- Source Systems
-- ============================================================================

INSERT INTO metadata.ref_source_system
VALUES
('OLIST','Olist Marketplace','Brazilian E-Commerce Dataset',TRUE)
ON CONFLICT DO NOTHING;


-- ============================================================================
-- ETL Version
-- ============================================================================

INSERT INTO metadata.ref_etl_version
VALUES
('2.0.0',
 'Initial Enterprise Platform Release',
 CURRENT_DATE,
 TRUE)
ON CONFLICT DO NOTHING;


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
    RAISE NOTICE ' Stage        : Reference Data Seeding';
    RAISE NOTICE ' Status       : SUCCESS';
    RAISE NOTICE ' Database     : %', current_database();
    RAISE NOTICE ' Executed At  : %', CURRENT_TIMESTAMP;
    RAISE NOTICE ' Next Stage   : Create Staging Tables';
    RAISE NOTICE '===============================================================';
    RAISE NOTICE '';

END
$$;
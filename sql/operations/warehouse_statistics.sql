/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : warehouse_statistics.sql
Schema      : analytics
Object      : warehouse_statistics
Purpose     : Enterprise Warehouse Statistics Report
Description : Collects operational statistics for the Enterprise Revenue
              Intelligence Platform including table sizes, index sizes,
              scan statistics, maintenance status and storage utilization.

Business Process : Warehouse Monitoring
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.warehouse_statistics()
LANGUAGE plpgsql
AS
$$
DECLARE

    ----------------------------------------------------------------------------
    -- EXECUTION
    ----------------------------------------------------------------------------
    v_start_time                 TIMESTAMPTZ := clock_timestamp();

    ----------------------------------------------------------------------------
    -- DATABASE
    ----------------------------------------------------------------------------
    v_database_name              TEXT;
    v_database_size              TEXT;

    ----------------------------------------------------------------------------
    -- TABLE COUNTS
    ----------------------------------------------------------------------------
    v_table_count                INTEGER;
    v_index_count                INTEGER;

BEGIN

    ----------------------------------------------------------------------------
    -- DATABASE
    ----------------------------------------------------------------------------
    SELECT current_database()
    INTO v_database_name;

    SELECT pg_size_pretty
    (
        pg_database_size(current_database())
    )
    INTO v_database_size;

    ----------------------------------------------------------------------------
    -- OBJECT COUNTS
    ----------------------------------------------------------------------------
    SELECT COUNT(*)
    INTO v_table_count
    FROM information_schema.tables
    WHERE table_schema = 'analytics';

    SELECT COUNT(*)
    INTO v_index_count
    FROM pg_indexes
    WHERE schemaname = 'analytics';

    ----------------------------------------------------------------------------
    -- HEADER
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '===========================================================';
    RAISE NOTICE 'ERIP Warehouse Statistics';
    RAISE NOTICE '===========================================================';

    RAISE NOTICE '';
    RAISE NOTICE '[DATABASE]';
    RAISE NOTICE 'Database      : %', v_database_name;
    RAISE NOTICE 'Database Size : %', v_database_size;

    RAISE NOTICE '';
    RAISE NOTICE '[OBJECTS]';
    RAISE NOTICE 'Tables        : %', v_table_count;
    RAISE NOTICE 'Indexes       : %', v_index_count;

    ----------------------------------------------------------------------------
    -- TABLE STATISTICS
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[TABLE STATISTICS]';

    FOR
        v_database_name,
        v_database_size
    IN

        SELECT
            relname,

            pg_size_pretty
            (
                pg_total_relation_size(c.oid)
            )

        FROM pg_class c

        INNER JOIN pg_namespace n
                ON c.relnamespace = n.oid

        WHERE n.nspname = 'analytics'
          AND c.relkind = 'r'

        ORDER BY
            pg_total_relation_size(c.oid) DESC

    LOOP

        RAISE NOTICE
            '% : %',
            RPAD(v_database_name,25,' '),
            v_database_size;

    END LOOP;

        ----------------------------------------------------------------------------
    -- INDEX STATISTICS
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[INDEX STATISTICS]';

    FOR
        v_database_name,
        v_database_size
    IN

        SELECT
            indexname,

            pg_size_pretty
            (
                pg_relation_size(indexname::regclass)
            )

        FROM pg_indexes
        WHERE schemaname = 'analytics'

        ORDER BY
            pg_relation_size(indexname::regclass) DESC

    LOOP

        RAISE NOTICE
            '% : %',
            RPAD(v_database_name,35,' '),
            v_database_size;

    END LOOP;

    ----------------------------------------------------------------------------
    -- TABLE ACCESS STATISTICS
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[TABLE ACCESS STATISTICS]';

    FOR
        v_database_name,
        v_database_size
    IN

        SELECT
            relname,

            CONCAT
            (
                'Seq Scan=',
                seq_scan,
                ', Index Scan=',
                idx_scan
            )

        FROM pg_stat_user_tables

        WHERE schemaname = 'analytics'

        ORDER BY relname

    LOOP

        RAISE NOTICE
            '% : %',
            RPAD(v_database_name,25,' '),
            v_database_size;

    END LOOP;

    ----------------------------------------------------------------------------
    -- VACUUM / ANALYZE STATUS
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[MAINTENANCE STATUS]';

    FOR
        v_database_name,
        v_database_size
    IN

        SELECT
            relname,

            CONCAT
            (
                'Last Vacuum=',
                COALESCE(last_vacuum::TEXT,'Never'),
                ', Last Analyze=',
                COALESCE(last_analyze::TEXT,'Never')
            )

        FROM pg_stat_user_tables

        WHERE schemaname = 'analytics'

        ORDER BY relname

    LOOP

        RAISE NOTICE
            '% : %',
            RPAD(v_database_name,25,' '),
            v_database_size;

    END LOOP;

        ----------------------------------------------------------------------------
    -- INDEX USAGE
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[INDEX USAGE]';

    FOR
        v_database_name,
        v_database_size
    IN

        SELECT
            indexrelname,

            CONCAT
            (
                'Scans=',
                idx_scan,
                ', Tuples Read=',
                idx_tup_read,
                ', Tuples Fetched=',
                idx_tup_fetch
            )

        FROM pg_stat_user_indexes

        WHERE schemaname = 'analytics'

        ORDER BY idx_scan DESC

    LOOP

        RAISE NOTICE
            '% : %',
            RPAD(v_database_name,35,' '),
            v_database_size;

    END LOOP;

    ----------------------------------------------------------------------------
    -- EXECUTION SUMMARY
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '===========================================================';
    RAISE NOTICE 'Warehouse Statistics Completed';
    RAISE NOTICE 'Execution Time : %',
        clock_timestamp() - v_start_time;
    RAISE NOTICE '===========================================================';

EXCEPTION
    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '===========================================================';
        RAISE NOTICE 'Warehouse Statistics Failed';
        RAISE NOTICE 'Error : %', SQLERRM;
        RAISE NOTICE '===========================================================';

        RAISE;

END;
$$;

-------------------------------------------------------------------------------
-- USAGE
-------------------------------------------------------------------------------

-- Display warehouse statistics
-- CALL analytics.warehouse_statistics();

-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------
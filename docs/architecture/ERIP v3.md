# Enterprise Revenue Intelligence Platform (ERIP)

## Version 3.0 Architecture Specification

**Status:** Draft (Architecture Baseline)

------------------------------------------------------------------------

# 1. Vision

ERIP is an enterprise-grade Revenue Intelligence Platform designed to
ingest, transform, validate, warehouse, and expose business data through
a semantic layer for analytics and BI.

Core principles:

-   Separation of concerns
-   Single Responsibility Principle
-   Modular architecture
-   Extensibility
-   High-performance bulk loading
-   Reusable components
-   Production observability

------------------------------------------------------------------------

# 2. High-Level Architecture

``` text
                +----------------------+
                |      Platform        |
                +----------+-----------+
                           |
                    Pipeline Engine
                           |
                 +---------+---------+
                 |                   |
          Warehouse Stage     Semantic Stage
                 |
           ETL / Ingestion
                 |
  +--------------+--------------+
  |              |              |
Readers     Transformers   Validators
  |              |              |
  +--------------+--------------+
                 |
          Metadata Builder
                 |
           PostgreSQL COPY
                 |
          Analytics Warehouse
                 |
          Semantic SQL Views
                 |
         Power BI / APIs / ML
```

------------------------------------------------------------------------

# 3. Platform Layers

## Platform Layer

Responsible for orchestration only.

Components: - Platform - Pipeline - Stage Registry - Service Container -
Execution Context

The platform never knows where data comes from.

------------------------------------------------------------------------

## ETL Layer

Responsible for converting raw data into validated analytical datasets.

### Readers

Supported connectors:

-   CSV
-   Excel
-   API
-   PostgreSQL
-   SQL Server
-   Snowflake
-   BigQuery
-   Parquet
-   Streaming (future)

Every reader returns a Pandas DataFrame.

------------------------------------------------------------------------

### Transformers

Responsibilities:

-   Standardize columns
-   Business rules
-   Type conversion
-   Null normalization
-   Duplicate removal

Reusable logic belongs in `transformations.py`.

------------------------------------------------------------------------

### Validators

Responsibilities:

-   Schema validation
-   Required columns
-   Null checks
-   Business rules
-   Referential integrity
-   Data quality

Validators operate on DataFrames.

------------------------------------------------------------------------

### Metadata Builder

Responsible for:

-   Batch ID
-   Load ID
-   Row Hash
-   Source metadata
-   ETL version

No database dependency.

------------------------------------------------------------------------

### Loader

The existing BaseLoader remains the loading engine.

Responsibilities:

-   COPY
-   Transactions
-   Commit/Rollback
-   Persistence

Responsibilities removed over time:

-   CSV reading
-   Cleaning
-   Validation
-   Metadata generation

------------------------------------------------------------------------

# 4. Warehouse Layer

Responsibilities:

-   DDL deployment
-   Dimensions
-   Facts
-   Constraints
-   Validation

Warehouse receives already validated data.

------------------------------------------------------------------------

# 5. Semantic Layer

Responsibilities:

-   Deploy dependency-aware views
-   Business metrics
-   Reporting abstraction
-   Power BI semantic model

Semantic never reads raw data.

------------------------------------------------------------------------

# 6. Dependency Rules

Allowed dependency flow:

``` text
Platform
    ↓
Warehouse Stage
    ↓
ETL
    ↓
Readers
    ↓
Transformers
    ↓
Validators
    ↓
Metadata Builder
    ↓
Loader
    ↓
Warehouse
    ↓
Semantic
```

No component may depend upward.

------------------------------------------------------------------------

# 7. Folder Structure

``` text
src/
├── core/
├── config/
├── database/
├── etl/
│   ├── extract/
│   ├── transform/
│   ├── validate/
│   ├── metadata/
│   └── load/
├── warehouse/
├── semantic/
├── orchestration/
├── observability/
└── utils/
```

------------------------------------------------------------------------

# 8. Engineering Standards

-   One responsibility per class
-   No duplicated business logic
-   Shared utilities before copy/paste
-   Keep orchestration separate from implementation
-   Prefer composition over inheritance where appropriate
-   Refactor by extracting responsibilities instead of rewriting working
    code

------------------------------------------------------------------------

# 9. Future Roadmap

Phase 1 - Reader framework - Metadata extraction - Loader refactoring

Phase 2 - Incremental loading - Data quality framework - Audit framework

Phase 3 - Scheduling - Streaming ingestion - Monitoring dashboards

Phase 4 - Executive BI - API layer - ML-ready feature pipelines

------------------------------------------------------------------------

# 10. Architecture Principles

1.  Platform orchestrates.
2.  Readers ingest.
3.  Transformers standardize.
4.  Validators enforce quality.
5.  Metadata Builder enriches.
6.  Loader persists.
7.  Warehouse stores.
8.  Semantic exposes.
9.  BI consumes.

Every component should be independently testable, reusable, and
replaceable without changing the overall platform architecture.

Master/reference entities → singular (customer, product, seller)

Transactional entities → plural (orders, order_items, order_payments, order_reviews)

Reference/lookup tables → descriptive singular (product_category_translation, geolocation)

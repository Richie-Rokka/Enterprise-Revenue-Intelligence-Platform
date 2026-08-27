# Enterprise Revenue Intelligence Platform (ERIP)

## Version 4.5 Architecture Specification

**Version:** 4.5.0  
**Architecture Status:** Stable Committed Baseline  
**Repository Tag:** `v4.5.0`  
**Architecture Scope:** Core Platform through Semantic Analytics Layer

---

# 1. Architecture Purpose

The Enterprise Revenue Intelligence Platform (ERIP) is an enterprise-oriented analytics platform designed to transform raw operational data into validated, structured, reusable analytical assets.

The v4.5 architecture represents the stable committed baseline of the platform and covers the implementation of:

- Platform configuration and initialization
- Database connectivity and execution
- Runtime lifecycle management
- Enterprise ETL pipelines
- Dataset registration
- Data extraction, transformation, validation, and loading
- Data quality management
- Warehouse management
- Monitoring and observability
- Dependency-aware orchestration
- Semantic management
- Analytical views
- Standardized KPI and metric development
- SQL-based dashboard assets

The architecture intentionally separates these responsibilities into distinct platform domains to improve maintainability, testability, and extensibility.

The v4.5 baseline does **not** include the later uncommitted intelligence framework extensions or a completed business-facing dashboard application.

---

# 2. Architecture Principles

## 2.1 Separation of Responsibilities

Each platform domain owns a specific responsibility.

```text
ETL             → Data extraction, transformation, validation, and staging loads
Warehouse       → Analytical storage and dimensional structures
Semantic        → Business-facing analytical abstractions
Metrics         → Standardized KPI and analytical calculations
Orchestration   → Platform execution and stage coordination
Quality         → Data quality rules and validation
Monitoring      → Platform and execution monitoring
Observability   → Logging, timing, diagnostics, and execution visibility
Runtime         → Lifecycle and runtime state management
Presentation    → Structured presentation of platform output
```

No single framework should absorb responsibilities belonging to another without explicit architectural justification.

## 2.2 Dependency Direction

Dependencies move toward lower-level infrastructure and reusable abstractions. Higher-level orchestration coordinates components but should not contain transformation, warehouse, semantic, or metric business logic.

```text
Platform / Orchestration
          │
          ├──────────────┬───────────────┐
          ▼              ▼               ▼
         ETL         Warehouse        Semantic
          │              │               │
          ▼              ▼               ▼
      Source Data    Analytics Data   Analytical Views
                                         │
                                         ▼
                                   Metrics & KPIs
                                         │
                                         ▼
                                  SQL Dashboard Assets
```

## 2.3 Reusable Components

Shared platform responsibilities are implemented as reusable managers, registries, validators, execution contexts, and abstractions.

## 2.4 Explicit Orchestration

Pipeline execution is coordinated through dedicated orchestration components rather than allowing individual frameworks to control the full platform lifecycle.

The orchestration layer provides:

- Pipeline coordination
- Stage registration
- Stage execution
- Execution context
- Dependency ordering
- Execution results

## 2.5 Validation Before Analytical Consumption

Data validation is performed before downstream analytical assets are relied upon. The architecture distinguishes:

- ETL validation
- Data quality validation
- Warehouse validation
- Semantic validation
- SQL-level validation

---

# 3. High-Level Architecture

The committed v4.5 architecture consists of interconnected platform domains.

```text
                              ┌──────────────────────┐
                              │     PLATFORM CORE    │
                              │                      │
                              │ Configuration        │
                              │ Database             │
                              │ Services             │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │       RUNTIME        │
                              │                      │
                              │ Lifecycle            │
                              │ Context              │
                              │ Metrics              │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │    ORCHESTRATION     │
                              │                      │
                              │ Pipeline             │
                              │ Stage Registry       │
                              │ Execution Context    │
                              └──────────┬───────────┘
                                         │
               ┌─────────────────────────┼─────────────────────────┐
               │                         │                         │
               ▼                         ▼                         ▼
       ┌──────────────┐          ┌──────────────┐         ┌──────────────┐
       │     ETL      │          │   QUALITY    │         │  MONITORING  │
       │ Extract      │          │ Rules        │         │ Registry     │
       │ Transform    │          │ Validation   │         │ Validation   │
       │ Validate     │          │ Scorecard    │         │ Models       │
       │ Load         │          │              │         │              │
       └──────┬───────┘          └──────────────┘         └──────────────┘
              │
              ▼
       ┌──────────────┐
       │   STAGING    │
       │    DATA      │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │  WAREHOUSE   │
       │ Dimensions   │
       │ Facts        │
       │ Procedures   │
       │ Validation   │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │   SEMANTIC   │
       │ Registry     │
       │ Manager      │
       │ Validator    │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │   ANALYTICS  │
       │ Views        │
       │ KPIs         │
       │ Metrics      │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ SQL DASHBOARD│
       │    ASSETS    │
       └──────────────┘

       CROSS-CUTTING CAPABILITIES
       ─────────────────────────
       Observability • Validation • Presentation
```

The diagram represents architectural responsibilities rather than a strict linear execution sequence.

---

# 4. Platform Core

The platform core provides shared infrastructure used across ERIP.

```text
src/
├── config/
├── core/
└── database/
```

## Configuration

The configuration domain manages platform configuration, including database, logging, pipeline, and quality settings.

```text
config/
├── database.yaml
├── logging.yaml
├── pipeline.yaml
└── quality.yaml
```

The configuration framework provides centralized access to runtime configuration and prevents implementation details from being hard-coded across platform components.

## Core Services

Committed components include:

```text
src/core/
├── platform.py
└── services.py
```

The platform core acts as the common infrastructure boundary between framework components.

## Database

```text
src/database/
├── connection.py
├── database_executor.py
└── health.py
```

Responsibilities include:

- Database connectivity
- SQL execution
- Database health checks
- Controlled access to PostgreSQL resources

Database access remains separate from domain-specific ETL, warehouse, and semantic logic.

---

# 5. Runtime Architecture

The runtime framework manages platform lifecycle and execution state.

```text
src/runtime/
├── context.py
├── lifecycle.py
├── manager.py
├── metrics.py
└── models.py
```

Responsibilities include:

- Runtime initialization
- Lifecycle management
- Execution context
- Runtime metrics
- Runtime state representation

---

# 6. Enterprise ETL Architecture

The ETL framework is responsible for transforming raw datasets into validated staging data.

```text
src/etl/
├── context.py
├── dataset_registry.py
├── execution.py
├── job.py
├── manager.py
├── pipeline.py
├── results.py
├── extract/
├── transform/
├── validate/
├── metadata/
└── load/
```

The v4.5 implementation follows:

```text
Dataset
   │
   ▼
Extractor
   │
   ▼
Transformer
   │
   ▼
Validator
   │
   ▼
Loader
   │
   ▼
Staging Table
```

Execution metrics and pipeline state are captured through ETL context and result objects.

## 6.1 Dataset Registry

The Dataset Registry centralizes dataset definitions and pipeline metadata, associating datasets with extraction, transformation, validation, and loading logic.

## 6.2 Extraction

The committed extraction implementation includes a reusable extractor abstraction and CSV-based extraction.

```text
src/etl/extract/
├── base_extractor.py
├── csv_extractor.py
├── load_raw_data.py
└── reader_registry.py
```

The architecture supports extension to additional source types, but the stable v4.5 implementation is centered on CSV ingestion.

## 6.3 Transformation

```text
src/etl/transform/
├── base_transformer.py
├── customer_transformer.py
├── geolocation_transformer.py
├── order_items_transformer.py
├── payment_transformer.py
├── product_transformer.py
├── review_transformer.py
├── sales_order_transformer.py
├── seller_transformer.py
└── transformations.py
```

Responsibilities include column standardization, type handling, null normalization, duplicate handling, dataset-specific transformation, and shared transformation utilities.

## 6.4 ETL Validation

```text
src/etl/validate/
├── base_validator.py
├── customer_validator.py
├── geolocation_validator.py
├── order_items_validator.py
├── orders_validator.py
├── payment_validator.py
├── product_validator.py
├── review_validator.py
└── seller_validator.py
```

The framework supports dataset-specific validation while maintaining a common validation interface.

## 6.5 Loading

```text
src/etl/load/
├── base_loader.py
├── copy_loader.py
├── load_customer.py
├── load_geolocation.py
├── load_order_items.py
├── load_order_payments.py
├── load_order_reviews.py
├── load_orders.py
├── load_product.py
├── load_product_category_translation.py
├── load_seller.py
└── load_staging.py
```

The loading architecture separates persistence from extraction, transformation, and validation. PostgreSQL bulk loading is supported through COPY-based loading.

---

# 7. Data Quality Architecture

The quality framework is implemented as a dedicated platform domain.

```text
src/quality/
├── manager.py
├── models.py
├── registry.py
├── rules.py
├── scorecard.py
└── validator.py
```

The architecture supports:

- Quality rule registration
- Rule execution
- Validation
- Quality scoring
- Quality result models
- Centralized quality management

SQL quality checks provide additional warehouse-level validation.

```text
sql/quality/
├── 001_check_duplicate_customers.sql
├── 002_check_null_customer_names.sql
├── 003_check_duplicate_products.sql
├── 004_check_orphan_fact_sales.sql
├── 005_check_negative_payment.sql
├── 006_check_payment_totals.sql
├── 007_check_negative_revenue.sql
├── 008_check_missing_product_category.sql
├── 009_check_duplicate_orders.sql
└── 010_quality_summary.sql
```

---

# 8. Warehouse Architecture

```text
src/warehouse/
├── manager.py
├── registry.py
└── validator.py
```

The warehouse implementation includes schema creation, staging tables, dimension tables, fact tables, constraints, reference data, load procedures, and operational validation.

## 8.1 Staging Layer

Implemented staging entities include:

```text
staging.customer
staging.geolocation
staging.product
staging.product_category_translation
staging.sales_order
staging.sales_order_item
staging.sales_order_payment
staging.sales_order_review
staging.seller
```

## 8.2 Analytical Warehouse

Dimensions:

```text
analytics.dim_customer
analytics.dim_date
analytics.dim_product
analytics.dim_seller
```

Primary analytical fact:

```text
analytics.fact_sales
```

The analytical grain is one row per order item.

## 8.3 Warehouse Procedures

```text
sql/procedures/
├── load_dim_customer.sql
├── load_dim_date.sql
├── load_dim_product.sql
├── load_dim_seller.sql
└── load_fact_sales.sql
```

## 8.4 Warehouse Operations

```text
sql/operations/
├── monitoring_statistics.sql
├── refresh_metadata.sql
├── refresh_warehouse.sql
├── reset_warehouse.sql
├── validate_warehouse.sql
├── warehouse_health.sql
└── warehouse_statistics.sql
```

---

# 9. Monitoring and Observability

## Monitoring

```text
src/monitoring/
├── manager.py
├── models.py
├── registry.py
└── validator.py
```

Database monitoring tables include:

```text
sql/monitoring/
├── create_etl_run_history.sql
├── create_pipeline_execution_history.sql
├── create_quality_rule_history.sql
├── create_table_load_history.sql
└── create_validation_history.sql
```

## Observability

```text
src/observability/
├── formatter.py
├── logger.py
├── memory.py
├── summary.py
└── timer.py
```

Observability supports logging, execution timing, runtime summaries, memory visibility, and structured execution output.

Monitoring answers:

> Is the platform operating correctly?

Observability helps answer:

> What happened during execution and why?

---

# 10. Orchestration Architecture

```text
src/orchestration/
├── execution_context.py
├── pipeline.py
├── register_stages.py
├── stage.py
├── stage_registry.py
├── stage_result.py
└── stages/
```

Implemented stages:

```text
stages/
├── etl_stage.py
├── monitoring_stage.py
├── quality_stage.py
├── semantic_stage.py
└── warehouse_stage.py
```

The orchestration architecture provides stage registration, pipeline coordination, execution context, stage results, and ordered execution.

Orchestration coordinates framework execution but does not own ETL transformations, warehouse SQL logic, semantic definitions, or analytical calculations.

---

# 11. Semantic Architecture

```text
src/semantic/
├── manager.py
├── registry.py
└── validator.py
```

The semantic layer is responsible for:

- Semantic asset registration
- Managed semantic deployment
- Semantic validation
- Business-oriented analytical abstractions

The semantic framework consumes analytical warehouse structures rather than raw source data.

## 11.1 Analytical Views

The committed v4.5 implementation includes:

```text
vw_customer_sales
vw_daily_sales
vw_delivery_performance
vw_logistics_performance
vw_monthly_sales
vw_product_performance
vw_revenue_dashboard
vw_review_performance
vw_sales
vw_seller_performance
```

---

# 12. Semantic Analytics and Metrics Architecture

The v4.5 milestone introduced a standardized analytics layer on top of the semantic and warehouse foundations.

```text
Analytics Warehouse
        │
        ▼
Analytical / Semantic Views
        │
        ▼
Domain KPI Definitions
        │
        ▼
Executive KPI Definitions
        │
        ▼
SQL Dashboard Assets
```

Domain metric areas:

```text
Customer
Revenue
Product
Seller
Operations
Executive
```

Committed structure:

```text
sql/metrics/
├── customer/
├── executive/
├── finance/
├── operations/
├── product/
└── seller/
```

---

# 13. SQL Dashboard Assets

```text
sql/dashboards/
├── customer_dashboard.sql
├── executive_dashboard.sql
├── operations_dashboard.sql
├── product_dashboard.sql
├── sales_dashboard.sql
└── seller_dsahboards.sql
```

These assets represent the analytical query layer intended to support dashboard and reporting use cases.

They should not be interpreted as evidence of a completed Power BI dashboard or business-facing application.

```text
Warehouse
    ↓
Semantic / Analytics Views
    ↓
Metrics
    ↓
SQL Dashboard Assets
    ↓
Future Presentation Application
```

The final business-facing dashboard or Revenue Operations Cockpit remains outside the stable v4.5 baseline.

---

# 14. Presentation Architecture

```text
src/presentation/
├── base_presenter.py
├── console.py
├── formatter.py
├── monitoring_presenter.py
├── quality_presenter.py
├── report.py
├── runtime_presenter.py
├── semantic_presenter.py
├── theme.py
└── warehouse_presenter.py
```

This framework presents platform execution and framework outputs. It is distinct from a completed executive dashboard application.

---

# 15. Validation Architecture

Validation is implemented across multiple layers.

```text
ETL Validation
      │
      ▼
Data Quality Validation
      │
      ▼
Warehouse Validation
      │
      ▼
Semantic Validation
      │
      ▼
SQL Analytics Validation
```

Repository-level validation assets include:

```text
validation/
├── base.py
├── models.py
├── runner.py
├── test_constraints.py
├── test_database.py
├── test_indexes.py
├── test_metadata.py
├── test_reference_data.py
├── test_schemas.py
├── test_staging_tables.py
└── test_warehouse.py
```

Phase 9 also includes:

```text
sql/validation/validate_phase9.sql
```

---

# 16. Repository Architecture

```text
Enterprise-Revenue-Intelligence-Platform/
│
├── config/
├── data/raw/
├── docs/
│   └── architecture/
├── scripts/
├── sql/
│   ├── dashboards/
│   ├── ddl/
│   ├── metrics/
│   ├── monitoring/
│   ├── operations/
│   ├── procedures/
│   ├── quality/
│   ├── reference/
│   ├── validation/
│   └── views/
├── src/
│   ├── config/
│   ├── core/
│   ├── database/
│   ├── etl/
│   ├── monitoring/
│   ├── observability/
│   ├── orchestration/
│   ├── presentation/
│   ├── quality/
│   ├── runtime/
│   ├── semantic/
│   └── warehouse/
├── validation/
├── main.py
├── pyproject.toml
└── requirements.txt
```

---

# 17. Stable Architecture Boundaries

## ETL does not own warehouse modeling

ETL prepares and loads validated source datasets. Warehouse procedures and structures own analytical dimensional modeling.

## Warehouse does not own semantic definitions

The warehouse stores analytical structures. The semantic layer provides reusable business-facing abstractions.

## Semantic does not own dashboard presentation

Semantic assets provide reusable analytical views. Metric definitions and dashboard SQL build on those assets.

## Metrics do not replace the semantic layer

Metrics consume semantic or analytical datasets. Metric logic should not recreate semantic framework responsibilities.

## Orchestration does not contain domain logic

The orchestration framework coordinates execution. Dataset transformation, quality rules, warehouse procedures, and semantic definitions remain within their respective domains.

---

# 18. Implemented Stable Scope

The stable `v4.5.0` architecture includes:

### Platform
- Configuration
- Core services
- Database integration
- Runtime lifecycle

### ETL
- Dataset registry
- CSV extraction
- Dataset transformation
- Dataset validation
- COPY-based loading
- ETL pipeline execution
- ETL management

### Data Quality
- Quality rules
- Registry
- Validation
- Scorecards

### Warehouse
- Staging layer
- Dimensions
- Fact table
- Loading procedures
- Warehouse validation
- Warehouse operations

### Monitoring and Observability
- Monitoring manager
- Monitoring registry
- Execution history
- Logging
- Timing
- Memory tracking
- Execution summaries

### Orchestration
- Pipeline execution
- Stage registry
- Execution context
- ETL stage
- Warehouse stage
- Semantic stage
- Quality stage
- Monitoring stage

### Semantic and Analytics
- Semantic management
- Semantic registry
- Semantic validation
- Analytical SQL views
- Domain KPIs
- Executive KPIs
- SQL dashboard assets

---

# 19. Explicitly Outside the v4.5 Stable Baseline

The following should not be represented as completed v4.5 functionality:

- Uncommitted intelligence framework work
- Intelligence-specific orchestration stages
- Post-v4.5 semantic query services
- Uncommitted payment performance extensions
- Uncommitted warehouse loading stages
- A completed Revenue Operations Cockpit
- A completed Power BI dashboard
- Production deployment
- Scheduled automation
- Streaming ingestion
- API services
- Machine learning pipelines

Some of these areas were explored or initiated after `v4.5.0`, but they are not part of the stable committed architecture.

---

# 20. Future Architecture Direction

Future development should extend the stable architecture rather than redesign frozen platform foundations.

```text
Stable v4.5 Platform
        │
        ├── Semantic Analytics
        │
        ▼
Extended Intelligence / Query Capabilities
        │
        ▼
Business-Facing Presentation Layer
        │
        ▼
Automation and Operations
        │
        ▼
Production and Portfolio Readiness
```

Future work should preserve the established boundaries between:

- Orchestration
- ETL
- Warehouse
- Semantic definitions
- Metrics
- Presentation

---

# 21. Architecture Status

**Current canonical architecture:** v4.5.0  
**Repository baseline:** Stable committed state  
**Later development:** On hold and uncommitted  
**Architecture redesign required:** No

The v4.5 architecture remains the authoritative representation of the stable ERIP platform.

Future work should extend this architecture through documented additions rather than retroactively redefining the completed platform.

---

# Architecture Summary

```text
SOURCE DATA
    │
    ▼
ENTERPRISE ETL
Extract → Transform → Validate → Load
    │
    ▼
STAGING
    │
    ▼
ANALYTICS WAREHOUSE
Dimensions + Fact Sales
    │
    ▼
SEMANTIC FRAMEWORK
Managed Business Abstractions
    │
    ▼
ANALYTICAL VIEWS
    │
    ▼
DOMAIN & EXECUTIVE METRICS
    │
    ▼
SQL DASHBOARD ASSETS
    │
    ▼
FUTURE BUSINESS-FACING PRESENTATION
```

**Cross-cutting platform capabilities:**

```text
Configuration
Runtime
Data Quality
Monitoring
Observability
Validation
Presentation
```

This document defines the **stable, committed v4.5 architecture** of the Enterprise Revenue Intelligence Platform.

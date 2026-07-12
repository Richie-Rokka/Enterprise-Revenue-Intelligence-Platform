# Enterprise Revenue Intelligence Platform (ERIP)

# ETL_MIGRATION_GUIDE.md

**Version:** 1.0.0  
**Status:** Active Development Standard  
**Applies From:** Phase 8 Onward

---

# Purpose

This document defines the standard process for migrating datasets into the Enterprise ETL Framework.

The framework architecture is now considered **stable**.

From this point onward, implementation focuses on onboarding additional datasets without redesigning the platform.

---

# Guiding Principle

> **Complete the platform, not the architecture.**

The Customer pipeline is the reference implementation for all future datasets.

Every remaining dataset must follow the same implementation pattern.

---

# Architecture

```
Dataset Registry
        │
        ▼
ETLManager
        │
        ▼
ETLPipeline
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
PostgreSQL
```

---

# Component Responsibilities

## DatasetRegistry

Responsible for:

- registering datasets
- building ETLPipeline objects
- acting as the single source of truth for dataset definitions

DatasetRegistry must never perform ETL work.

---

## ETLManager

Responsible for:

- registering datasets
- executing pipelines
- aggregating PipelineResult objects
- producing ETLSummary

ETLManager must never perform:

- extraction
- transformation
- validation
- loading

---

## ETLPipeline

Responsible for orchestration only.

Execution sequence:

```
Extract

↓

Transform

↓

Validate

↓

Load

↓

PipelineResult
```

The pipeline must not contain dataset-specific logic.

---

## Extractor

Responsibilities

- read source data
- create DataFrame
- update extraction metrics
- return DataFrame

Must never:

- transform data
- validate data
- load data

---

## Transformer

Responsibilities

- business transformations
- column standardization
- normalization
- duplicate removal
- metadata generation

Must never:

- read files
- write database

---

## Validator

Responsibilities

- validate transformed dataset
- enforce business rules
- update validation metrics

Must never:

- transform data
- load data

---

## Loader

Responsibilities

- add enterprise metadata
- execute PostgreSQL COPY
- manage transactions
- return LoadResult

Must never:

- extract data
- transform data
- validate data

---

# ETLContext Ownership

ETLContext is the single shared runtime object.

Every ETL component receives the same ETLContext instance.

Ownership of runtime metrics is fixed.

| Metric | Owner |
|----------|---------|
| rows_extracted | Extractor |
| rows_transformed | Transformer |
| rows_validated | Validator |
| rows_loaded | Loader |
| status | Loader (pipeline completion) |

The pipeline must never update runtime metrics.

---

# Runtime Flow

```
CSVExtractor

↓

CustomerTransformer

↓

CustomerValidator

↓

CustomerLoader

↓

LoadResult

↓

PipelineResult

↓

ETLSummary
```

---

# Result Objects

## LoadResult

Represents loader execution.

Contains:

- target_table
- rows_loaded
- rows_rejected
- batch_id
- load_id
- duration_seconds
- success

---

## PipelineResult

Represents one dataset execution.

Contains:

- pipeline_name
- rows_extracted
- rows_transformed
- rows_validated
- LoadResult

---

# Dataset Migration Standard

Every dataset migration must follow exactly the same process.

---

## Step 1

Create Transformer

Example

```
customer_transformer.py
```

---

## Step 2

Create Validator

Example

```
customer_validator.py
```

---

## Step 3

Update Loader

Implement

```
load(dataframe)
```

Return

```
LoadResult
```

---

## Step 4

Register dataset

Example

```
DatasetRegistry.register_customer()
```

---

## Step 5

Update

```
register_all()
```

---

## Step 6

Smoke Test

```
python -m scripts.test_customer_pipeline
```

---

## Step 7

Verify

Expected output

```
Rows Extracted

↓

Rows Transformed

↓

Rows Validated

↓

Rows Loaded

↓

SUCCESS
```

---

# Migration Order

The migration order is fixed.

1. Customer ✅
2. Orders
3. Products
4. Sellers
5. Order Items
6. Payments
7. Reviews
8. Geolocation

Do not change this order.

---

# Frozen Components

The following modules are considered stable.

```
context.py

pipeline.py

manager.py

dataset_registry.py

base_loader.py

csv_extractor.py
```

Do not redesign these files.

Only defect fixes are permitted.

---

# Logging Standard

Use parameterized logging.

Preferred

```python
logger.info(
    "Rows loaded: %s",
    f"{rows_loaded:,}",
)
```

Avoid

```python
logger.info(
    f"Rows loaded: {rows_loaded:,}"
)
```

Never use

```python
logger.info(
    "Rows loaded: %,d",
    rows_loaded,
)
```

---

# Error Handling

Exceptions propagate upward.

```
Extractor

↓

Transformer

↓

Validator

↓

Loader

↓

Pipeline

↓

Manager
```

ETLContext records failure.

Exceptions are re-raised.

Never silently swallow exceptions.

---

# Testing Standard

Every migrated dataset must have a smoke test.

Example

```
scripts/

    test_customer_pipeline.py

    test_orders_pipeline.py

    test_products_pipeline.py
```

Each smoke test must verify

- extraction
- transformation
- validation
- loading
- SUCCESS status

---

# Definition of Done

A dataset migration is complete only when:

- Dataset registered
- Pipeline builds successfully
- Pipeline executes successfully
- PostgreSQL COPY succeeds
- Smoke test passes
- Metrics match expected row counts
- Status = SUCCESS

---

# Ground Rules

Do not redesign architecture.

Do not rename packages.

Do not move modules.

Do not modify frozen phases.

Do not introduce new abstractions without strong justification.

Maintain backward compatibility during migration.

Fix defects in place.

Proceed incrementally.

---

# Project Objective

The objective of ERIP is to deliver a production-grade Enterprise Revenue Intelligence Platform that demonstrates enterprise software engineering practices.

The platform should showcase:

- Enterprise ETL Architecture
- Modular Design
- PostgreSQL Data Warehouse
- Enterprise Data Quality
- Runtime Monitoring
- Metadata Management
- Analytics Layer
- Executive Dashboards
- Production Readiness

Architecture stability is now considered achieved.

The remaining work is implementation.
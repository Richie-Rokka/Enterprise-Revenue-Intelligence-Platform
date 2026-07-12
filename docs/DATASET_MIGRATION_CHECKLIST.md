# Enterprise Revenue Intelligence Platform (ERIP)

# DATASET_MIGRATION_CHECKLIST.md

**Version:** 1.0.0  
**Status:** Active Development Standard  
**Phase:** Phase 8 – Enterprise ETL Orchestration

---

# Purpose

This checklist defines the mandatory migration process for onboarding a dataset into the Enterprise ETL Framework.

The objective is to ensure every dataset follows an identical implementation pattern while preserving the frozen ETL architecture.

---

# Migration Workflow

```
Register Dataset

        ↓

Build ETLPipeline

        ↓

Extract

        ↓

Transform

        ↓

Validate

        ↓

Load

        ↓

Smoke Test

        ↓

Verify

        ↓

Freeze Dataset
```

---

# Dataset Information

| Item | Value |
|------|-------|
| Dataset Name | __________________ |
| Source File | __________________ |
| Target Table | __________________ |
| Migration Sprint | __________________ |
| Date Completed | __________________ |
| Engineer | __________________ |

---

# Migration Checklist

## 1. Dataset Analysis

- [ ] Review source dataset
- [ ] Identify required columns
- [ ] Identify business rules
- [ ] Identify duplicate strategy
- [ ] Identify null handling
- [ ] Identify datatype conversions

---

## 2. Transformer

Create

```
src/etl/transform/<dataset>_transformer.py
```

Checklist

- [ ] Standardize columns
- [ ] Validate required columns
- [ ] Normalize business values
- [ ] Normalize strings
- [ ] Convert datatypes
- [ ] Remove duplicates
- [ ] Sort dataset
- [ ] Update ETLContext rows_transformed
- [ ] Record metadata
- [ ] Enterprise logging implemented

Verification

- [ ] Transformer imports successfully

---

## 3. Validator

Create

```
src/etl/validate/<dataset>_validator.py
```

Checklist

- [ ] Inherit BaseValidator
- [ ] Accept ETLContext
- [ ] Update rows_validated
- [ ] Implement dataset-specific validation
- [ ] Enterprise logging implemented

Verification

- [ ] Validator imports successfully

---

## 4. Loader

Update

```
src/etl/load/load_<dataset>.py
```

Checklist

- [ ] Accept ETLContext
- [ ] Remove legacy transformation logic
- [ ] Remove legacy validation logic
- [ ] Remove standalone execution
- [ ] Use BaseLoader.load()
- [ ] Return LoadResult

Verification

- [ ] Loader imports successfully

---

## 5. Dataset Registration

Update

```
src/etl/dataset_registry.py
```

Checklist

- [ ] Import Transformer
- [ ] Import Validator
- [ ] Import Loader
- [ ] Implement register_<dataset>()
- [ ] Update register_all()

Verification

- [ ] Dataset appears in registered_datasets()

Expected

```
['customer', 'orders', '<dataset>']
```

---

## 6. Pipeline Construction

Checklist

- [ ] Build ETLPipeline

Verification

```python
pipeline = DatasetRegistry.build_pipeline("<dataset>")
```

Expected

```
ETLPipeline
```

---

## 7. Smoke Test

Create

```
scripts/test_<dataset>_pipeline.py
```

Checklist

- [ ] Register datasets
- [ ] Build pipeline
- [ ] Execute pipeline
- [ ] Print PipelineResult
- [ ] Print execution metrics

Verification

```
python -m scripts.test_<dataset>_pipeline
```

---

## 8. Execution Verification

Verify

- [ ] Extraction completed
- [ ] Transformation completed
- [ ] Validation completed
- [ ] Loading completed
- [ ] PostgreSQL COPY completed
- [ ] Status = SUCCESS

Expected

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

## 9. Data Verification

Verify

- [ ] Row counts match source
- [ ] No unexpected duplicates
- [ ] No rejected rows
- [ ] Metadata generated
- [ ] Target table populated
- [ ] Primary keys valid

---

## 10. Performance Verification

Record

| Metric | Value |
|---------|-------|
| Rows Extracted | |
| Rows Loaded | |
| Execution Time | |
| Memory Usage | |
| Status | |

---

## 11. Code Review

Verify

- [ ] Enterprise logging standard followed
- [ ] Type hints complete
- [ ] Docstrings complete
- [ ] Version updated
- [ ] No legacy code introduced
- [ ] No architecture modifications

---

## 12. Freeze Dataset

Dataset is considered complete only when:

- [ ] Smoke test passes
- [ ] PostgreSQL COPY succeeds
- [ ] Execution metrics verified
- [ ] ETLPipeline execution verified
- [ ] DatasetRegistry verified
- [ ] ETLManager verified
- [ ] Status = SUCCESS

Mark

```
Dataset Status

✅ COMPLETE
```

---

# Migration Order

The migration sequence is frozen.

| Order | Dataset | Status |
|-------:|---------|:------:|
| 1 | Customer | ✅ Complete |
| 2 | Orders | ✅ Complete |
| 3 | Products | ⬜ Pending |
| 4 | Sellers | ⬜ Pending |
| 5 | Order Items | ⬜ Pending |
| 6 | Payments | ⬜ Pending |
| 7 | Reviews | ⬜ Pending |
| 8 | Geolocation | ⬜ Pending |

Do not change this order.

---

# Frozen Framework

The following modules are architecture-frozen.

```
src/etl/context.py

src/etl/pipeline.py

src/etl/manager.py

src/etl/dataset_registry.py

src/etl/load/base_loader.py

src/etl/extract/csv_extractor.py
```

Permitted changes:

- Bug fixes
- Performance improvements
- Documentation

Not permitted:

- Package restructuring
- Module relocation
- New framework abstractions
- Architectural redesign

---

# Definition of Done

A dataset migration is complete when all of the following are true:

- ✅ Transformer implemented
- ✅ Validator implemented
- ✅ Loader migrated
- ✅ Dataset registered
- ✅ Pipeline builds successfully
- ✅ Pipeline executes successfully
- ✅ PostgreSQL COPY succeeds
- ✅ Smoke test passes
- ✅ Metrics verified
- ✅ Status = SUCCESS

Only then should the dataset be marked as **Complete** and the migration proceed to the next dataset.

---

# Enterprise Engineering Principle

> **The framework is frozen.**
>
> Every new dataset must adapt to the framework.
>
> The framework must not be redesigned to accommodate a dataset.

This principle ensures architectural stability, consistent implementation, and production-grade engineering across the Enterprise Revenue Intelligence Platform (ERIP).
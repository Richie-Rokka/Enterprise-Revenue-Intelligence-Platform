# Enterprise Revenue Intelligence Platform (ERIP)

# Metrics Development Standard

**Document ID:** ERIP-STD-METRICS-001  
**Version:** 1.0.0  
**Status:** APPROVED  
**Phase:** Phase 9 – Enterprise Metrics Layer  
**Author:** ERIP Engineering  
**Last Updated:** July 2026

---

# 1. Purpose

This document defines the engineering standards for developing enterprise business metrics within the Enterprise Revenue Intelligence Platform (ERIP).

The objective is to ensure that every metric:

- is consistent
- is reusable
- is documented
- is performant
- follows enterprise SQL standards
- supports Executive Analytics

This standard applies to every SQL artifact created under:

```text
sql/metrics/
```

---

# 2. Scope

This standard governs:

- Executive KPIs
- Financial Metrics
- Customer Metrics
- Product Metrics
- Seller Metrics
- Operational Metrics

It does **not** apply to:

- DDL
- ETL Procedures
- Semantic Views
- Data Quality Rules

---

# 3. Architecture

Enterprise Analytics follows a layered architecture.

```text
Enterprise Data Warehouse
        │
        ▼
Semantic Views
(sql/views)
        │
        ▼
Business Metrics
(sql/metrics)
        │
        ▼
Executive Dashboards
(Power BI / Tableau / Excel)
```

Metrics shall consume semantic views rather than warehouse tables.

---

# 4. Golden Rule

## Metrics MUST NOT query warehouse tables directly.

Correct

```text
fact_sales

↓

vw_sales

↓

sales_kpis.sql
```

Incorrect

```text
fact_sales

↓

sales_kpis.sql
```

Business logic belongs in the Semantic Layer.

Metrics consume Semantic Views.

---

# 5. Directory Structure

```text
sql/

metrics/

├── executive/
├── finance/
├── customer/
├── product/
├── seller/
└── operations/
```

---

# 6. Metric Categories

## Executive

Enterprise scorecards.

Examples

- Revenue
- Gross Sales
- Net Sales
- Total Orders
- Active Customers

---

## Finance

Examples

- Average Order Value
- Payment Mix
- Revenue Growth
- Refund Rate

---

## Customer

Examples

- Customer Lifetime Value
- Repeat Purchase Rate
- Retention
- Churn

---

## Product

Examples

- Product Revenue
- Product Margin
- Product Ranking

---

## Seller

Examples

- Seller Revenue
- Seller Rating
- Fulfillment Performance

---

## Operations

Examples

- Delivery SLA
- Delivery Time
- Review Score
- Logistics Performance

---

# 7. File Naming

All filenames use lowercase snake_case.

Examples

```text
executive_kpis.sql

sales_kpis.sql

customer_kpis.sql

delivery_metrics.sql
```

Avoid

```text
RevenueKPIs.sql

Executive.sql

SalesDashboard.sql
```

---

# 8. SQL Header Standard

Every metrics file shall begin with:

```sql
/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      :
Schema      : analytics
Object      :
Purpose     :
Author      : ERIP
Version     :

Description
-----------
...

Dependencies
------------
...

Business Grain
--------------
...

===============================================================================
*/
```

---

# 9. SQL Formatting

Keywords

```sql
SELECT

FROM

WHERE

GROUP BY

ORDER BY
```

Uppercase.

Identifiers

```sql
snake_case
```

Indentation

4 spaces.

Maximum line length

120 characters.

---

# 10. CTE Structure

Metrics shall use layered CTEs.

Example

```text
base_data

↓

business_logic

↓

aggregations

↓

final_output
```

Avoid deeply nested SQL.

Readable SQL is preferred over compact SQL.

---

# 11. Naming Standards

Metric aliases shall be business friendly.

Good

```text
total_revenue

average_order_value

active_customers

repeat_customer_rate
```

Avoid

```text
sum_amt

avg_ord

metric1
```

---

# 12. Null Handling

Use COALESCE where appropriate.

Example

```sql
COALESCE(total_revenue,0)
```

Do not expose NULL values in executive metrics unless business meaning requires it.

---

# 13. Division Safety

Every division shall prevent divide-by-zero.

Example

```sql
NULLIF(order_count,0)
```

---

# 14. Numeric Precision

Currency

```text
NUMERIC(18,2)
```

Percentages

```text
ROUND(value,2)
```

Ratios

```text
ROUND(value,4)
```

---

# 15. Dates

Use the enterprise Date Dimension whenever possible.

Avoid raw timestamp calculations inside metrics.

---

# 16. Performance Standards

Metrics shall

- avoid SELECT *
- avoid repeated calculations
- avoid unnecessary DISTINCT
- leverage Semantic Views
- leverage indexed warehouse tables indirectly

Large calculations should be performed once within CTEs.

---

# 17. Documentation

Every metric shall document

Purpose

Business Definition

Calculation

Dependencies

Expected Consumers

Example

```text
Metric

Average Order Value

Definition

Revenue / Orders
```

---

# 18. Versioning

Semantic changes

Minor Version

Breaking calculation changes

Major Version

Documentation updates

Patch Version

Example

```text
1.0.0

1.1.0

2.0.0
```

---

# 19. Testing Requirements

Every metric must be validated for

✓ SQL compilation

✓ Business correctness

✓ Null handling

✓ Duplicate handling

✓ Performance

✓ Expected row counts

---

# 20. Review Checklist

Before approval verify

- Naming
- Documentation
- SQL formatting
- Business definition
- Performance
- Dependencies
- Version
- Testing

---

# 21. Coding Rules

Metrics SHALL

✓ Consume Semantic Views

✓ Be deterministic

✓ Be reusable

✓ Be documented

✓ Follow this standard

Metrics SHALL NOT

✗ Query staging tables

✗ Duplicate Semantic Layer logic

✗ Hardcode business constants

✗ Use SELECT *

✗ Introduce undocumented calculations

---

# 22. Gold Standard

The following file establishes the reference implementation for all future metrics.

```text
sql/metrics/executive/executive_kpis.sql
```

Every future metrics artifact shall conform to the structure, formatting, and engineering practices established by this file.

---

# 23. Architecture Baseline

The Enterprise Metrics Layer extends the Phase 8 ETL architecture.

```text
Warehouse
        │
        ▼
Semantic Views
        │
        ▼
Enterprise Metrics
        │
        ▼
Executive Dashboards
```

The Metrics Layer shall not alter the responsibilities of the Warehouse or Semantic layers.

---

# 24. Approval

| Item | Status |
|------|:------:|
| Enterprise Standard | ✅ |
| Architecture Approved | ✅ |
| Phase | 9 |
| Status | ACTIVE |

---

## Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | July 2026 | Initial Enterprise Metrics Development Standard |
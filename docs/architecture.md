# Platform Architecture

## Overview

The Real-Time Product Intelligence Platform simulates a modern analytics engineering workflow designed to process event-driven product and revenue data into trusted analytical insights.

The platform includes:
- event generation
- warehouse modeling
- analytical marts
- orchestration
- data quality validation
- executive dashboards

---

## Architecture Flow

```txt
Event Generator
      ↓
Raw Event Layer (Parquet)
      ↓
DuckDB Warehouse
      ↓
Staging Transformations
      ↓
Analytics Marts
      ↓
Data Quality Monitoring
      ↓
Executive Dashboard
```

---

## Components

### Event Generator

Simulates user and product activity events including:
- app opens
- product views
- cart activity
- purchases
- refunds

Generated using:
- Python
- Faker

---

### Warehouse Layer

DuckDB is used as the analytical warehouse engine.

Responsibilities:
- raw ingestion
- staging transformations
- mart generation
- analytical aggregations

---

### Data Quality Layer

Automated validation layer responsible for:
- null validation
- invalid event detection
- revenue consistency checks
- future timestamp detection

---

### Analytics Marts

The platform generates:
- revenue marts
- funnel analytics marts
- executive KPI summaries

---

### Orchestration

Pipeline orchestration is handled using Prefect.

The orchestration layer automates:
- event generation
- warehouse builds
- quality monitoring

---

### Dashboard Layer

Interactive executive dashboard built with:
- Streamlit
- Plotly

Provides:
- revenue intelligence
- funnel monitoring
- product analytics
- data quality visibility
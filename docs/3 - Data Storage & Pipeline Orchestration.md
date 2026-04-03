# Data Storage & Pipeline Orchestration

## 1. Overview

This phase focuses on designing and implementing the storage layer of the pipeline, as well as integrating all components into a fully automated system.

The goal is to transform processed data into a structured relational format and ensure reliable, repeatable pipeline execution.

---

## 2. Objective

The objective of this phase is to:

* Store processed job data in a relational database (PostgreSQL)
* Design a normalized schema for analytical queries
* Ensure data integrity using constraints and relationships
* Build a complete end-to-end pipeline (ingestion → processing → storage)
* Implement incremental and automated execution

---

## 3. Database Design

The database is designed using a normalized schema to separate entities and avoid redundancy.

### Tables:

#### jobs (fact table)

* job_id (PRIMARY KEY)
* title
* description
* company_id (FOREIGN KEY)
* location_id (FOREIGN KEY)
* contract_type
* category
* job_role
* salary_min
* salary_max
* salary_avg
* created_at
* ingestion_timestamp

#### companies

* company_id (PRIMARY KEY)
* name (UNIQUE)

#### locations

* location_id (PRIMARY KEY)
* name
* country
* UNIQUE(name, country)

---

## 4. Data Loading Strategy

Data is loaded from processed Parquet files into PostgreSQL using a multi-step approach:

1. Insert unique companies
2. Insert unique locations
3. Build mappings (name → id)
4. Enrich dataset with foreign keys
5. Insert jobs data

### Key features:

* Duplicate handling using `ON CONFLICT DO NOTHING`
* Referential integrity enforced via foreign keys
* Data validation through preprocessing and enrichment

---

## 5. Pipeline Integration

The pipeline is fully orchestrated through a central entry point:

```
src/pipeline/run_pipeline.py
```

### Execution flow:

1. Ingestion → fetch data from API
2. Processing → transform raw data into structured format
3. Storage → load data into PostgreSQL

---

## 6. Incremental Processing

The pipeline avoids reprocessing existing data by checking:

```
data/processed/adzuna/YYYY-MM-DD/jobs.parquet
```

If the file exists, the pipeline skips execution for that date.

---

## 7. Incremental Ingestion

The pipeline avoids redundant API calls by verifying:

```
data/raw/adzuna/YYYY-MM-DD/
```

If raw data already exists, ingestion is skipped.

---

## 8. Automation

The pipeline is designed for daily execution.

### Implementation:

* Dynamic date handling using current system date
* Scheduled execution using system scheduler (Task Scheduler)

This ensures continuous data collection and updates.

---

## 9. Design Decisions

### Separation of Concerns

Each layer is independent:

* ingestion → data collection
* processing → transformation
* storage → persistence
* pipeline → orchestration

---

### Idempotency

The pipeline can be safely re-run without:

* duplicating data
* reprocessing existing partitions

---

### Partition-Based Design

Data is organized by date, enabling:

* incremental processing
* time-based analysis
* efficient storage management

---

## 10. Current Status

At the end of this phase, the system includes:

* A fully functional PostgreSQL database
* A normalized schema with constraints
* A complete data loading pipeline
* Incremental execution logic
* Automated daily runs

This completes the core data engineering pipeline.

The next phase focuses on extracting insights and building an analytics layer.

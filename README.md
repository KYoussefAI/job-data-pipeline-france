# Job Data Pipeline – France 🇫🇷

## Problem & Motivation

Understanding the job market is critical for students, professionals, and organizations making career and hiring decisions.

In the field of data, roles such as Data Engineer, Data Analyst, and Data Scientist are evolving rapidly, but there is limited structured visibility into how demand for these roles changes over time in a specific market like France.

Most available job data is:

* fragmented across platforms
* not stored historically
* difficult to analyze over time

As a result, answering questions such as:

* Which data roles are most in demand?
* How is demand evolving over time?
* What locations have the highest concentration of opportunities?
* How do salary ranges vary across roles?

becomes difficult without building a dedicated data system.

This project addresses this gap by building a system that continuously collects and structures job market data for analysis.

---

## Project Objective

The objective of this project is to design and implement a data pipeline that continuously collects and structures job market data in France, enabling time-based analysis and insights.

This system transforms raw job listings into a structured dataset that can support:

* trend analysis over time
* comparison between roles
* geographic distribution analysis
* salary exploration

---

## Why This Project Matters

This project illustrates how data engineering enables real-world decision-making.

By building a reliable and automated data pipeline, this system allows:

* students to better understand which roles to target
* professionals to track market demand
* analysts to extract insights from evolving job trends

It also reflects a realistic data engineering use case:

> transforming unstructured external data into a structured, queryable system that supports analysis.

## 1. Overview

This project builds a data pipeline to track and analyze the evolution of data-related job demand in France over time.

## 2. Current Status

* Phase 1: Problem Definition & Data Source Design → Completed
* Phase 2: Data Processing & Transformation → Completed
* Phase 3: Data Storage & Automation → Completed
* Next Phase: Analytics & Dashboard

---

## 3. Pipeline Architecture

```
        +-------------+
        |  Adzuna API |
        +-------------+
               ↓
        +----------------------+
        | Ingestion Layer      |
        | fetch_jobs.py        |
        +----------------------+
               ↓
        +----------------------+
        | Raw Data Storage     |
        | data/raw/adzuna/     |
        +----------------------+
               ↓
        +----------------------+
        | Processing Layer     |
        | reader → extractor → |
        | transformer → writer |
        +----------------------+
               ↓
        +----------------------+
        | Processed Data       |
        | data/processed/      |
        +----------------------+
               ↓
        +----------------------+
        | Storage Layer        |
        | PostgreSQL           |
        +----------------------+
               ↓
        +----------------------+
        | Pipeline Orchestration|
        | run_pipeline.py      |
        +----------------------+
```

---

## 4. Project Structure

```
job-data-pipeline-france/
│
├── data/                          # Raw and processed data (ignored in Git)
│   ├── raw/
│   │   └── adzuna/
│   │       └── YYYY-MM-DD/
│   │           └── *.json
│   │
│   └── processed/
│       └── adzuna/
│           └── YYYY-MM-DD/
│               └── jobs.parquet
│
├── docs/                          # Project documentation
│   ├── problem_and_data_design.md
│   ├── data_processing.md
│   └── data_storage.md
│
├── src/
│   ├── ingestion/
│   │   └── fetch_jobs.py
│   │
│   ├── processing/
│   │   ├── reader.py
│   │   ├── extractor.py
│   │   ├── transformer.py
│   │   ├── writer.py
│   │   └── process_jobs.py
│   │
│   ├── storage/
│   │   └── load_jobs.py
│   │
│   └── pipeline/
│       └── run_pipeline.py
│
├── .env                           # API & DB credentials (not committed)
├── README.md
```

---

## 5. Data Source

The project uses the Adzuna Job Search API, which provides structured job listings across France.

### Key Features:

* Keyword-based job search
* Pagination support
* Structured JSON responses
* Coverage of multiple job platforms

---

## 6. Ingestion Strategy

* Queries:

  * data engineer
  * data analyst
  * data scientist

* Location:

  * France

* Pagination:

  * Multiple pages per query

* Frequency:

  * Daily execution

---

## 7. Raw Data Design

Raw data is stored without modification to preserve data integrity.

### Structure:

```
data/raw/adzuna/YYYY-MM-DD/
```

Each file contains:

* query
* page
* ingestion_timestamp
* full API response

---

## 8. Processing Layer

The processing pipeline transforms raw JSON data into a structured dataset.

### Features:

* Modular architecture (reader → extractor → transformer → writer)
* Safe handling of missing data
* Schema standardization
* Type conversion (timestamps, numeric fields)
* Feature engineering (salary_avg, ingestion_date)
* Deduplication (job_id)

### Output:

```
data/processed/adzuna/YYYY-MM-DD/jobs.parquet
```

---

## 9. Storage Layer (PostgreSQL)

A normalized relational schema is used to ensure clean and efficient data storage.

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

## 10. Data Loading Strategy

Data is loaded into PostgreSQL using a structured pipeline:

1. Insert unique companies
2. Insert unique locations
3. Build mappings (name → id)
4. Enrich dataset with foreign keys
5. Insert jobs

### Key Features:

* Duplicate prevention using `ON CONFLICT DO NOTHING`
* Referential integrity via foreign keys
* Data validation before insertion

---

## 11. Pipeline Orchestration

The entire pipeline is controlled by:

```
src/pipeline/run_pipeline.py
```

### Execution Flow:

1. Ingestion
2. Processing
3. Storage

---

## 12. Incremental Pipeline

The pipeline processes only new data.

### Processing Check:

```
data/processed/adzuna/YYYY-MM-DD/jobs.parquet
```

If the file exists → processing is skipped.

---

## 13. Incremental Ingestion

The pipeline avoids unnecessary API calls.

### Check:

```
data/raw/adzuna/YYYY-MM-DD/
```

If data exists → ingestion is skipped.

---

## 14. Automation

The pipeline is designed for daily automated execution.

### Features:

* Dynamic date handling
* Idempotent execution (safe re-runs)
* Integration with system scheduler (e.g., Task Scheduler)

---

## 15. Design Principles

* Separation of concerns (ingestion / processing / storage / orchestration)
* Immutable raw data
* Partition-based design (by date)
* Idempotent pipeline execution
* Minimal and practical technology stack

---

## 16. How to Run

### 1. Create `.env`

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_api_key
DB_PASSWORD=your_password
```

---

### 2. Install dependencies

```
pip install requests python-dotenv pandas pyarrow psycopg2
```

---

### 3. Run pipeline

```
python -m src.pipeline.run_pipeline
```

---

## 17. Next Steps

* Build analytical queries (SQL)
* Create aggregated metrics
* Develop a dashboard (Streamlit)
* Extract insights from job market data

---

## 18. Project Goal

This project aims to demonstrate:

* Real-world data pipeline design
* Data engineering best practices
* End-to-end system thinking
* Practical, production-oriented implementation

---

## 19. Final Status

The system is now:

* Fully end-to-end
* Automated
* Incremental
* Structured and scalable

The next phase focuses on transforming data into actionable insights.


---

## 1. Overview

This project implements a complete end-to-end data engineering pipeline to analyze the evolution of data-related job demand in France over time.

The system is designed to collect, store, process, and structure job market data in a scalable and reliable way, enabling future analytical insights and visualization.

---

## 2. Current Status

* Phase 1: Problem Definition & Data Source Design → Completed
* Phase 2: Data Processing & Transformation → Completed
* Phase 3: Data Storage & Automation → Completed
* Next Phase: Analytics & Dashboard

---

## 3. Pipeline Architecture

```
        +-------------+
        |  Adzuna API |
        +-------------+
               ↓
        +----------------------+
        | Ingestion Layer      |
        | fetch_jobs.py        |
        +----------------------+
               ↓
        +----------------------+
        | Raw Data Storage     |
        | data/raw/adzuna/     |
        +----------------------+
               ↓
        +----------------------+
        | Processing Layer     |
        | reader → extractor → |
        | transformer → writer |
        +----------------------+
               ↓
        +----------------------+
        | Processed Data       |
        | data/processed/      |
        +----------------------+
               ↓
        +----------------------+
        | Storage Layer        |
        | PostgreSQL           |
        +----------------------+
               ↓
        +----------------------+
        | Pipeline Orchestration|
        | run_pipeline.py      |
        +----------------------+
```

---

## 4. Project Structure

```
job-data-pipeline-france/
│
├── data/                          # Raw and processed data (ignored in Git)
│   ├── raw/
│   │   └── adzuna/
│   │       └── YYYY-MM-DD/
│   │           └── *.json
│   │
│   └── processed/
│       └── adzuna/
│           └── YYYY-MM-DD/
│               └── jobs.parquet
│
├── docs/                          # Project documentation
│   ├── problem_and_data_design.md
│   ├── data_processing.md
│   └── data_storage.md
│
├── src/
│   ├── ingestion/
│   │   └── fetch_jobs.py
│   │
│   ├── processing/
│   │   ├── reader.py
│   │   ├── extractor.py
│   │   ├── transformer.py
│   │   ├── writer.py
│   │   └── process_jobs.py
│   │
│   ├── storage/
│   │   └── load_jobs.py
│   │
│   └── pipeline/
│       └── run_pipeline.py
│
├── .env                           # API & DB credentials (not committed)
├── README.md
```

---

## 5. Data Source

The project uses the Adzuna Job Search API, which provides structured job listings across France.

### Key Features:

* Keyword-based job search
* Pagination support
* Structured JSON responses
* Coverage of multiple job platforms

---

## 6. Ingestion Strategy

* Queries:

  * data engineer
  * data analyst
  * data scientist

* Location:

  * France

* Pagination:

  * Multiple pages per query

* Frequency:

  * Daily execution

---

## 7. Raw Data Design

Raw data is stored without modification to preserve data integrity.

### Structure:

```
data/raw/adzuna/YYYY-MM-DD/
```

Each file contains:

* query
* page
* ingestion_timestamp
* full API response

---

## 8. Processing Layer

The processing pipeline transforms raw JSON data into a structured dataset.

### Features:

* Modular architecture (reader → extractor → transformer → writer)
* Safe handling of missing data
* Schema standardization
* Type conversion (timestamps, numeric fields)
* Feature engineering (salary_avg, ingestion_date)
* Deduplication (job_id)

### Output:

```
data/processed/adzuna/YYYY-MM-DD/jobs.parquet
```

---

## 9. Storage Layer (PostgreSQL)

A normalized relational schema is used to ensure clean and efficient data storage.

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

## 10. Data Loading Strategy

Data is loaded into PostgreSQL using a structured pipeline:

1. Insert unique companies
2. Insert unique locations
3. Build mappings (name → id)
4. Enrich dataset with foreign keys
5. Insert jobs

### Key Features:

* Duplicate prevention using `ON CONFLICT DO NOTHING`
* Referential integrity via foreign keys
* Data validation before insertion

---

## 11. Pipeline Orchestration

The entire pipeline is controlled by:

```
src/pipeline/run_pipeline.py
```

### Execution Flow:

1. Ingestion
2. Processing
3. Storage

---

## 12. Incremental Pipeline

The pipeline processes only new data.

### Processing Check:

```
data/processed/adzuna/YYYY-MM-DD/jobs.parquet
```

If the file exists → processing is skipped.

---

## 13. Incremental Ingestion

The pipeline avoids unnecessary API calls.

### Check:

```
data/raw/adzuna/YYYY-MM-DD/
```

If data exists → ingestion is skipped.

---

## 14. Automation

The pipeline is designed for daily automated execution.

### Features:

* Dynamic date handling
* Idempotent execution (safe re-runs)
* Integration with system scheduler (e.g., Task Scheduler)

---

## 15. Design Principles

* Separation of concerns (ingestion / processing / storage / orchestration)
* Immutable raw data
* Partition-based design (by date)
* Idempotent pipeline execution
* Minimal and practical technology stack

---

## 16. How to Run

### 1. Create `.env`

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_api_key
DB_PASSWORD=your_password
```

---

### 2. Install dependencies

```
pip install requests python-dotenv pandas pyarrow psycopg2
```

---

### 3. Run pipeline

```
python -m src.pipeline.run_pipeline
```

---

## 17. Next Steps

* Build analytical queries (SQL)
* Create aggregated metrics
* Develop a dashboard (Streamlit)
* Extract insights from job market data

---

## 18. Project Goal

This project aims to demonstrate:

* Real-world data pipeline design
* Data engineering best practices
* End-to-end system thinking
* Practical, production-oriented implementation

---

## 19. Final Status

The system is now:

* Fully end-to-end
* Automated
* Incremental
* Structured and scalable

The next phase focuses on transforming data into actionable insights.

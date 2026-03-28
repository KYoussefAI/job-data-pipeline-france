# Problem Definition & Data Source Design

## 1. Overview

This phase defines the foundation of the project: identifying the problem, selecting the data source, and designing how data will be collected and stored.

The goal is to build a reliable data ingestion system that supports future analysis of job market trends in France.

---

## 2. Problem Statement

The objective of this project is to analyze the evolution of data-related job demand in France over time.

The system is designed to answer key questions such as:

* Which data roles are most in demand?
* How does demand evolve over time?
* What are the main geographic job distributions?
* What skills are frequently requested?

To enable this, job data must be collected consistently and stored in a structured, time-aware manner.

---

## 3. Data Source

The project uses the **Adzuna Job Search API**, a REST API that aggregates job listings from multiple sources.

### Why this source:

* Provides structured job data
* Covers the French job market
* Includes useful fields (title, company, location, description, etc.)
* Supports filtering and pagination

---

## 4. Data Collection Strategy

The ingestion strategy is designed to ensure controlled and relevant data collection.

### Queries (job roles)

* Data Engineer
* Data Analyst
* Data Scientist

### Location

* France (country-level filtering)

### Pagination

* Multiple pages per query to ensure broader coverage

### Frequency

* Designed for daily execution to enable time-series analysis

---

## 5. Ingestion Process

The ingestion process is implemented in:

```
src/ingestion/fetch_jobs.py
```

### Workflow:

For each job query and each page:

1. Send a request to the Adzuna API
2. Retrieve job listings
3. Store the raw response as a JSON file

This ensures that data collection is systematic, repeatable, and scalable.

---

## 6. Raw Data Design

Raw data is stored **without any modification** to preserve the original source of truth.

### File structure:

```
data/raw/adzuna/YYYY-MM-DD/
```

### File naming convention:

```
{query}_page_{page}_{timestamp}.json
```

### Each file contains:

* `query`: search keyword used
* `page`: page number
* `ingestion_timestamp`: time of data collection
* `data`: full API response

### Example:

```json
{
  "query": "data analyst",
  "page": 1,
  "ingestion_timestamp": "2026-03-28T15:08:49",
  "data": { ... }
}
```

---

## 7. Design Decisions

### Raw data is immutable

Raw data is never modified to ensure:

* reproducibility
* traceability
* debugging capability

### Timestamped storage

Each dataset is associated with a timestamp to:

* enable time-based analysis
* prevent overwriting
* track data evolution

### Query-based filtering

Using specific job roles allows:

* controlled dataset scope
* relevant analysis
* reduced noise

### Pagination

Pagination ensures:

* complete data retrieval
* manageable API requests
* scalable ingestion

---

## 8. Limitations

* Salary information is often missing or inconsistent
* Location granularity varies across listings
* Duplicate job postings may exist
* Results depend on keyword matching (not perfect classification)

---

## 9. Current Status

At the end of this phase, the system includes:

* A clearly defined problem and analytical objectives
* A validated external data source
* A working ingestion script
* A structured raw data storage system

This provides a solid foundation for the next phase: **data processing and modeling**.

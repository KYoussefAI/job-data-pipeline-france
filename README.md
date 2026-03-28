# 📊 Job Data Pipeline – France

## 1. Overview

This project builds an end-to-end data pipeline to analyze the evolution of data-related job demand in France over time.

The system is designed to collect, store, process, and analyze job market data in a structured and scalable way.

---

## 2. Current Status

* Phase 1: Problem Definition & Data Source Design → Completed
* Next Phase: Data Processing & Modeling

---

## 3. Pipeline Architecture (Current)

```
        +-------------+
        |  Adzuna API |
        +-------------+
               ↓
        +----------------------+
        | Ingestion Script     |
        | fetch_jobs.py        |
        +----------------------+
               ↓
        +----------------------+
        | Raw Data Storage     |
        | data/raw/adzuna/     |
        +----------------------+
```

---

## 4. Project Structure

```
job-data-pipeline-france/
│
├── data/                          # Raw data (ignored in Git)
│   └── raw/
│       └── adzuna/
│           └── YYYY-MM-DD/
│               └── *.json
│
├── docs/                          # Project documentation
│   └── problem_and_data_design.md
│
├── src/                           # Source code
│   └── ingestion/
│       └── fetch_jobs.py
│
├── .gitignore
├── README.md
├── .env                           # API keys (not committed)
```

---

## 5. Data Source

The project uses the Adzuna Job Search API, which provides access to job listings across France.

Key features:

* Structured job data
* Keyword-based filtering
* Pagination support

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

  * Designed for daily execution

---

## 7. Raw Data Design

Raw data is stored in JSON format and is never modified.

Each file contains:

* query
* page
* ingestion timestamp
* full API response

Storage format:

```
data/raw/adzuna/YYYY-MM-DD/
```

---

## 8. Design Principles

* Raw data is immutable (reproducibility, traceability)
* Timestamped storage (time-based analysis)
* Controlled data collection (query filtering)
* Scalable ingestion (pagination)

---

## 9. How to Run

1. Create a `.env` file:

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_api_key
```

2. Install dependencies:

```
pip install requests python-dotenv
```

3. Run the ingestion script:

```
python src/ingestion/fetch_jobs.py
```

---

## 10. Next Steps

* Data cleaning and transformation
* Structured schema design
* Database integration (PostgreSQL)
* Analytics and dashboard
* Pipeline automation

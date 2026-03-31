# Data Processing & Transformation

## 1. Overview

This phase focuses on transforming raw job data into a clean, structured format suitable for storage and analysis.

The goal is to build a reliable data processing pipeline that standardizes raw JSON data while preserving its integrity.

---

## 2. Objective

The objective of this phase is to convert raw, nested API responses into a structured dataset that can support analytical queries and database storage.

This includes:

* Extracting relevant fields from raw data
* Handling missing and inconsistent values
* Converting data into appropriate types
* Creating additional features for analysis

---

## 3. Input Data

The processing pipeline operates on raw data generated during the ingestion phase.

### Input structure:

```
data/raw/adzuna/YYYY-MM-DD/
```

Each file contains:

* query
* page
* ingestion_timestamp
* full API response

---

## 4. Processing Pipeline

The processing logic is implemented in:

```
src/processing/
```

### Components:

* `reader.py` → loads raw JSON files
* `extractor.py` → extracts and flattens relevant fields
* `transformer.py` → applies transformations and type conversions
* `writer.py` → saves processed data
* `process_jobs.py` → orchestrates the pipeline

### Workflow:

1. Read raw JSON files
2. Extract relevant job fields
3. Transform data into structured format
4. Save processed dataset

---

## 5. Data Transformation

### Field Extraction

Nested structures are flattened into a consistent schema.

Key extracted fields include:

* job_id
* title
* company
* location
* country
* salary_min
* salary_max
* contract_type
* category
* description
* created_at
* ingestion_timestamp

---

### Data Cleaning

The pipeline ensures safe handling of inconsistent data:

* Missing fields are handled using safe access (`.get()`)
* No imputation is applied at this stage
* Missing values are preserved as `None` or `NaN`

---

### Type Conversion

Data is converted into appropriate types:

* Timestamps → datetime
* Salary fields → numeric

This ensures compatibility with downstream processing and storage systems.

---

### Feature Engineering

Additional fields are created:

* ingestion_date → extracted from ingestion timestamp
* salary_avg → computed as the average of salary_min and salary_max

---

## 6. Output Data

Processed data is stored in Parquet format.

### Output structure:

```
data/processed/adzuna/YYYY-MM-DD/jobs.parquet
```

This structure mirrors the raw data layout and supports incremental data processing.

---

## 7. Design Decisions

### Separation of Concerns

The processing pipeline is modular:

* Each component has a single responsibility
* Improves readability and maintainability
* Allows independent testing of each step

---

### Preservation of Data Integrity

No transformations alter the original meaning of the data:

* Missing values are not artificially filled
* Raw data remains the source of truth

---

### Use of Parquet Format

Parquet is used for processed data because:

* efficient storage
* faster read performance
* schema preservation
* scalability for large datasets

---

## 8. Limitations

* Salary information is often missing
* Duplicate records may still exist across pages
* Some categorical fields (e.g. category) may lack consistency

---

## 9. Current Status

At the end of this phase, the system includes:

* A complete data processing pipeline
* Structured and clean datasets
* Data ready for database integration

This provides the foundation for the next phase: **data storage and modeling**.

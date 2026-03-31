import pandas as pd


EXPECTED_COLUMNS = [
    "job_id",
    "title",
    "company",
    "location",
    "country",
    "salary_min",
    "salary_max",
    "contract_type",
    "category",
    "description",
    "created_at",
    "ingestion_timestamp"
]


def transform_jobs(jobs):

    df = pd.DataFrame(jobs)

    # This forces them to be in the right order and drops any unexpected cols
    df = df[EXPECTED_COLUMNS]

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["ingestion_timestamp"] = pd.to_datetime(
        df["ingestion_timestamp"], errors="coerce"
    )

    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")

    df["ingestion_date"] = pd.to_datetime(df["ingestion_timestamp"].dt.date)

    df["salary_avg"] = df[["salary_min", "salary_max"]].mean(axis=1)

    df = df.drop_duplicates(subset=["job_id"])

    return df

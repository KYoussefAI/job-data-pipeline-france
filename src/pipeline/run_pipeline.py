from src.ingestion.fetch_jobs import run_ingestion
from src.processing.process_jobs import process_jobs
from src.storage.load_jobs import run as load_jobs
from datetime import datetime
import os


def is_processed(date):
    path = f"data/processed/adzuna/{date}/jobs.parquet"
    return os.path.exists(path)


def raw_data_exists(date):
    path = f"data/raw/adzuna/{date}"
    return os.path.exists(path) and len(os.listdir(path)) > 0


def run_pipeline(date):

    if is_processed(date):
        print(f"{date} already processed. Skipping.")
        return

    print(f"[{datetime.now()}] Pipeline started")

    if not raw_data_exists(date):
        run_ingestion(date)
        print("→ Ingestion done")
    else:
        print("→ Raw data already exists. Skipping ingestion")

    process_jobs(date)
    print("→ Processing done")

    load_jobs(date)
    print("→ Loading done")

    print(f"Pipeline completed for {date}")


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    run_pipeline(today)

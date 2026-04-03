from src.processing.reader import load_raw_jobs
from src.processing.extractor import extract_job
from src.processing.transformer import transform_jobs
from src.processing.writer import save_to_parquet


def process_jobs(date):
    RAW_PATH = f"data/raw/adzuna/{date}"
    PROCESSED_PATH = "data/processed/adzuna"

    jobs = load_raw_jobs(RAW_PATH)

    extracted_jobs = [extract_job(job) for job in jobs]

    df = transform_jobs(extracted_jobs)

    save_to_parquet(df, PROCESSED_PATH)

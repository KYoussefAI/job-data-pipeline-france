from reader import load_raw_jobs
from extractor import extract_job
from transformer import transform_jobs
from writer import save_to_parquet

RAW_PATH = "data/raw/adzuna/2026-03-28"
PROCESSED_PATH = "data/processed/adzuna"

jobs = load_raw_jobs(RAW_PATH)
extracted_jobs = [extract_job(job) for job in jobs]
df = transform_jobs(extracted_jobs)
save_to_parquet(df, PROCESSED_PATH)

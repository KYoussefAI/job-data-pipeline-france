import json
from glob import glob


def load_raw_jobs(folder_path):
    files = glob(f"{folder_path}/*.json")

    all_jobs = []

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        ingestion_ts = content.get("ingestion_timestamp")
        job_role = content.get("query")
        results = content.get("data", {}).get("results", [])

        for job in results:
            job["ingestion_timestamp"] = ingestion_ts
            job["job_role"] = job_role
            all_jobs.append(job)

    return all_jobs

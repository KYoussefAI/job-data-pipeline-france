import json
from glob import glob


def load_raw_jobs(folder_path):
    files = glob(f"{folder_path}/*.json")

    all_jobs = []

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        ingestion_ts = content.get("ingestion_timestamp")
        results = content.get("data", {}).get("results", [])

        for job in results:
            job["ingestion_timestamp"] = ingestion_ts
            all_jobs.append(job)

    return all_jobs

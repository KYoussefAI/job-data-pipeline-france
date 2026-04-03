import os
import requests
import json
from datetime import datetime, timezone
from dotenv import load_dotenv


def run_ingestion(date):

    load_dotenv()

    APP_ID = os.getenv("ADZUNA_APP_ID")
    APP_KEY = os.getenv("ADZUNA_APP_KEY")

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/fr/search/{}"

    queries = [
        "data engineer",
        "data analyst",
        "data scientist"
    ]
    MAX_PAGES = 2

    for query in queries:
        print(f"\n--- Fetching jobs for: {query} ---")

        for page in range(1, MAX_PAGES + 1):

            url = BASE_URL.format(page)

            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "what": query,
                "where": "france",
                "results_per_page": 5
            }

            response = requests.get(url, params=params)

            if response.status_code != 200:
                print(f"Error on page {page}: {response.status_code}")
                continue

            data = response.json()
            results = data.get("results", [])

            print(f"Query: {query} | Page: {page} | \
                  Jobs fetched: {len(results)}")

            # -------------

            now = datetime.now(timezone.utc)
            date_str = date
            time_str = now.strftime("%H-%M-%S")

            folder_path = f"data/raw/adzuna/{date_str}"
            os.makedirs(folder_path, exist_ok=True)

            safe_query = query.replace(" ", "_")

            file_name = f"{safe_query}_page_{page}_{time_str}.json"
            file_path = os.path.join(folder_path, file_name)

            output_data = {
                "query": safe_query,
                "page": page,
                "ingestion_timestamp": now.isoformat(),
                "data": data
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f"Saved: {file_path}")

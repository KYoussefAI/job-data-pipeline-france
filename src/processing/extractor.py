def extract_job(job):
    return {
        "job_id": job.get("id"),
        "title": job.get("title"),
        "job_role": job.get("job_role"),

        "company": job.get("company", {}).get("display_name"),

        "location": job.get("location", {}).get("display_name"),

        "country": job.get("location", {}).get("area", [None])[0],

        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),

        "contract_type": job.get("contract_type"),

        "category": job.get("category", {}).get("label"),

        "description": job.get("description"),

        "created_at": job.get("created"),

        "ingestion_timestamp": job.get("ingestion_timestamp")
    }

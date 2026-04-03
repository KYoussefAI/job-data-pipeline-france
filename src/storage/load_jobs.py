import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv


def load_parquet(date):
    path = f"data/processed/adzuna/{date}/jobs.parquet"
    return pd.read_parquet(path)


def get_connection():
    load_dotenv()
    return psycopg2.connect(
        dbname="France_job_pipeline",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )


def insert_companies(cur, df):
    companies = df["company"].dropna().unique()

    for company in companies:
        cur.execute("""
            INSERT INTO companies (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (company,))


def insert_locations(cur, df):
    locations = df[["location", "country"]].dropna().drop_duplicates()

    for _, row in locations.iterrows():
        cur.execute("""
            INSERT INTO locations(name, country)
            VALUES(%s, %s)
            ON CONFLICT (name, country) DO NOTHING
            """, (row["location"], row["country"]))


def build_mappings(cur):
    cur.execute("SELECT company_id, name FROM companies")
    company_rows = cur.fetchall()

    company_map = {name: cid for cid, name in company_rows}

    cur.execute("SELECT location_id, name, country FROM locations")
    location_rows = cur.fetchall()

    location_map = {
        (name, country): lid
        for lid, name, country in location_rows
    }

    return company_map, location_map


def enrich_dataframe(df, company_map, location_map):
    df["company_id"] = df["company"].map(company_map)

    df["location_id"] = df.apply(
        lambda x: location_map.get((x["location"], x["country"])),
        axis=1
    )

    df = df.dropna(subset=["company_id", "location_id"])
    df["company_id"] = df["company_id"].astype(int)
    df["location_id"] = df["location_id"].astype(int)

    return df


def insert_jobs(cur, df):
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO jobs (
                job_id, title, job_role, description,
                company_id, location_id,
                contract_type, category,
                salary_min, salary_max, salary_avg,
                created_at, ingestion_timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) DO NOTHING
        """, (
            row["job_id"],
            row["title"],
            row['job_role'],
            row["description"],
            row["company_id"],
            row["location_id"],
            row["contract_type"],
            row["category"],
            row["salary_min"],
            row["salary_max"],
            row["salary_avg"],
            row["created_at"],
            row["ingestion_timestamp"]
        ))


def run(date):
    df = load_parquet(date)
    print(f"Loaded {len(df)} rows from parquet")

    conn = get_connection()
    cur = conn.cursor()

    insert_companies(cur, df)
    insert_locations(cur, df)

    company_map, location_map = build_mappings(cur)

    df = enrich_dataframe(df, company_map, location_map)
    print(f"{len(df)} rows after enrichment")

    insert_jobs(cur, df)

    conn.commit()
    cur.close()
    conn.close()

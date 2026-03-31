import os


def save_to_parquet(df, base_path):

    ingestion_date_str = df["ingestion_timestamp"].iloc[0].strftime("%Y-%m-%d")

    output_path = os.path.join(base_path, ingestion_date_str)

    os.makedirs(output_path, exist_ok=True)

    file_path = os.path.join(output_path, "jobs.parquet")

    df.to_parquet(file_path, index=False)

    print(f"Saved processed data to: {file_path}")

# tasks/ingestion.py
# create .env file (example available in the repo root folder)
# pip install python-dotenv

from prefect import task
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

@task
def ingest_csv_to_mysql(file_path: str, table: str):
    """
    Ingests a CSV into a MySQL table, validates schema, logs row counts, 
    and handles missing/extra columns gracefully.
    """
    # Load CSV
    df = pd.read_csv(file_path)
    row_count = len(df)
    print(f"Loaded {row_count} rows from {file_path}")

    # Connect to MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Get DB columns
    cursor.execute(f"DESCRIBE {table}")
    db_columns = [row[0] for row in cursor.fetchall()]

    # Check for missing and extra columns
    missing_cols = set(db_columns) - set(df.columns)
    extra_cols = set(df.columns) - set(db_columns)

    if missing_cols:
        raise ValueError(f"Missing required columns for table '{table}': {missing_cols}")
    
    if extra_cols:
        print(f"Warning: Extra columns in CSV ignored: {extra_cols}")
        # Keep only columns that exist in DB
        df = df[[col for col in df.columns if col in db_columns]]

    # Prepare insert statement
    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

    # Insert rows
    for _, row in df.iterrows():
        cursor.execute(sql, tuple(row))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Inserted {row_count} rows into {table}")
    return row_count

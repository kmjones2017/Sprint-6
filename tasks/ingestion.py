import mysql.connector
import pandas as pd
from typing import Dict
from config import db_config

# --- Utility functions ---

def get_table_columns(cursor, table_name: str) -> set:
    cursor.execute(f"DESCRIBE {table_name}")
    return {row[0] for row in cursor.fetchall()}


def validate_schema(df: pd.DataFrame, table_name: str, cursor) -> None:
    """
    Validates that the DataFrame columns match the target MySQL table schema.
    Raises ValueError if there is a mismatch.
    """
    table_columns = get_table_columns(cursor, table_name)
    df_columns = set(df.columns)

    missing = table_columns - df_columns
    extra = df_columns - table_columns

    if missing:
        raise ValueError(f"Missing columns for table '{table_name}': {missing}")
    if extra:
        raise ValueError(f"Unexpected columns for table '{table_name}': {extra}")


# --- Core ingestion task ---

def ingest_csv_to_mysql(csv_path: str, table_name: str) -> int:
    """
    Reads a CSV file, validates schema, inserts data into MySQL.
    Returns number of rows inserted.
    """
    df = pd.read_csv(csv_path)

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Schema validation
    validate_schema(df, table_name, cursor)

    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

    cursor.executemany(sql, data)
    connection.commit()

    row_count = cursor.rowcount

    cursor.close()
    connection.close()

    print(f"Inserted {row_count} rows into {table_name}")
    return row_count


# --- Example execution order (FK-safe) ---
if __name__ == "__main__":
    # replace the first parameter's file path in each of the following lines with the local file path of each CSV on your computer
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\customers.csv", "customers")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\suppliers.csv", "suppliers")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\raw_materials.csv", "raw_materials")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\drugs.csv", "drugs")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\drug_formulations.csv", "drug_formulations")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\drug_batches.csv", "drug_batches")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\orders.csv", "orders")
    ingest_csv_to_mysql(r"C:\Users\kmjon\Documents\ITExpertSystem\Internship\Sprint_6\order_items.csv", "order_items")

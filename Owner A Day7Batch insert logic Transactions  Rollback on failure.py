from prefect import task, get_run_logger
import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import db_config

@task(name="Batch Insert to MySQL (Owner A)", retries=0)
def batch_insert_mysql(df: pd.DataFrame, table: str, batch_size: int = 1000) -> int:
    """
    Owner A deliverable:
    - Batch insert using executemany
    - Explicit transaction handling
    - Rollback on failure
    Returns inserted rows count
    """
    logger = get_run_logger()

    conn = None
    cursor = None
    inserted = 0

    try:
        conn = mysql.connector.connect(**db_config)
        conn.autocommit = False  # ✅ transaction mode
        cursor = conn.cursor()

        cols = list(df.columns)
        placeholders = ", ".join(["%s"] * len(cols))
        col_list = ", ".join(cols)
        sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

        data = [tuple(row) for row in df.itertuples(index=False, name=None)]

        # ✅ Batch insert
        for i in range(0, len(data), batch_size):
            chunk = data[i:i + batch_size]
            cursor.executemany(sql, chunk)
            inserted += cursor.rowcount

        conn.commit()  # ✅ commit if all good
        logger.info(f"✅ Inserted {inserted} rows into {table} in batches of {batch_size}")
        return inserted

    except Error as e:
        # ✅ rollback on failure
        if conn is not None:
            conn.rollback()
        logger.error(f"❌ Batch insert FAILED for table={table}. Rolled back. Error: {e}")
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

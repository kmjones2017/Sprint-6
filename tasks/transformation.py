import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def load_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def validate_columns(df, required_cols, table_name):
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"{table_name} missing columns: {missing}")

def save_merged_report(df, path="C:/Users/kmjon/Documents/ITExpertSystem/Internship/Sprint_6/merged_orders_report.csv"):
    df.to_csv(path, index=False)
    print(f"Saved merged report to {path}")

# ---- Load tables ----
customers = load_table("customers")
orders = load_table("orders")
order_items = load_table("order_items")
drug_batches = load_table("drug_batches")
drugs = load_table("drugs")

# ---- Validate minimal schema ----
validate_columns(customers, ["customer_id"], "customers")
validate_columns(orders, ["order_id", "customer_id"], "orders")
validate_columns(order_items, ["order_id", "batch_id", "quantity"], "order_items")
validate_columns(drug_batches, ["batch_id", "drug_id"], "drug_batches")
validate_columns(drugs, ["drug_id"], "drugs")

# ---- Merge lineage ----
orders_enriched = orders.merge(customers, on="customer_id", how="left")

orders_items = orders_enriched.merge(
    order_items,
    on="order_id",
    how="left"
)

orders_batches = orders_items.merge(
    drug_batches,
    on="batch_id",
    how="left"
)

final_df = orders_batches.merge(
    drugs,
    on="drug_id",
    how="left"
)

if __name__ == "__main__":
    print(f"Final row count: {len(final_df)}")
    save_merged_report(final_df)

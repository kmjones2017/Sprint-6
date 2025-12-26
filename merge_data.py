from prefect import task
import pandas as pd

@task(name="Merge Customers Orders Items Batches Drugs")
def merge_data(customers: pd.DataFrame,
               orders: pd.DataFrame,
               order_items: pd.DataFrame,
               drug_batches: pd.DataFrame,
               drugs: pd.DataFrame) -> pd.DataFrame:

    print(f"customers rows: {len(customers)}")
    print(f"orders rows: {len(orders)}")
    print(f"order_items rows: {len(order_items)}")
    print(f"drug_batches rows: {len(drug_batches)}")
    print(f"drugs rows: {len(drugs)}")

    merged = orders.merge(customers, on="customer_id", how="left")
    merged = merged.merge(order_items, on="order_id", how="left")
    merged = merged.merge(drug_batches, on="batch_id", how="left")
    merged = merged.merge(drugs, on="drug_id", how="left")

    print(f"✅ merged rows: {len(merged)}")
    return merged

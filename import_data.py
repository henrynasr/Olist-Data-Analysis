from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:0000@localhost:5432/olit")

# Test it
with engine.connect() as conn:
    print("Connection successful")

import pandas as pd

# (filename, table_name) in load order
files = [
    ("olist_customers_dataset.csv", "customers"),
    ("olist_sellers_dataset.csv", "sellers"),
    ("olist_products_dataset.csv", "products"),
    ("product_category_name_translation.csv", "product_category_translation"),
    ("olist_orders_dataset.csv", "orders"),
    ("olist_order_items_dataset.csv", "order_items"),
    ("olist_order_payments_dataset.csv", "order_payments"),
    ("olist_order_reviews_dataset.csv", "order_reviews"),
    ("olist_geolocation_dataset.csv", "geolocation"),
    ("olist_marketing_qualified_leads_dataset.csv", "marketing_qualified_leads"),
    ("olist_closed_deals_dataset.csv", "closed_deals"),
]

for filename, table in files:
    df = pd.read_csv(f"data/{filename}")
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"Loaded {table}: {len(df)} rows")
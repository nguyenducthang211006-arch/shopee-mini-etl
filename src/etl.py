import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, NVARCHAR
from urllib.parse import quote_plus
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
print("SERVER:", os.getenv("DB_SERVER"))
print("DATABASE:", os.getenv("DB_NAME"))
print("USER:", os.getenv("DB_USER"))
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "TrustServerCertificate=yes;"
)

params = quote_plus(connection_string)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)

products = pd.read_sql(
    "Select * from productt",
    engine
)
orders = pd.read_sql(
    "Select * from orderr",
    engine
)
order_items = pd.read_sql(
    "select * from order_item",
    engine
)
shop = pd.read_sql(
    "select * from shop",
    engine
)
categories = pd.read_sql(
    "SELECT * FROM catgory",
    engine
)
df = order_items.merge(
    orders,
    on="order_id",
    how="inner"
)
df = df.merge(
    products,
    on="product_id",
    how="inner"
)
df = df.merge(
    shop[["shop_id","shop_name"]],
    on="shop_id",
    how="left"
)
df = df.merge(
    categories[["category_id","category_name"]],
    on="category_id",
    how="left"
)
df["sales_amount"] = df["quantity"] * df["unit_price"]
df[
    [
        "order_id",
        "order_date",
        "userr_id",
        "product_id",
        "product_name",
        "shop_id",
        "shop_name",
        "category_id",
        "category_name",
        "quantity",
        "unit_price",
        "sales_amount"
    ]
].to_sql(
    "fact_sales",
    engine,
    if_exists="append",
    index=False,
    dtype={
        "product_name": NVARCHAR(50),
        "shop_name": NVARCHAR(50),
        "category_name": NVARCHAR(50)
    }
)


#IMPORT
import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, NVARCHAR,text,bindparam
from urllib.parse import quote_plus
from pathlib import Path

#CONNECTION
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
#OLTP
connection_string_oltp = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "TrustServerCertificate=yes;"
)

params_oltp = quote_plus(connection_string_oltp)

engine_oltp = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params_oltp}"
)
#DWH
connection_string_dwh = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={os.getenv('DB_SERVER')};"
    "DATABASE=shopeemini_dwh;"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "TrustServerCertificate=yes;"
)

params_dwh = quote_plus(connection_string_dwh)

engine_dwh = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params_dwh}"
)
#DIM_USER
def load_dim_user():
    print("Loading dim_user...")
    users = pd.read_sql(
    "select * from [User]",
    engine_oltp
)
    users = users[
    [
        "userr_id",
        "userr_name",
        "email",
        "phone"
    ]
]
    users.to_sql(
    "dim_user",
    engine_dwh,
    if_exists="append",
    index=False,
     dtype={
        "userr_name": NVARCHAR(50)
    }
)
    print("dim_user loaded")
#DIM_PRODUCT
def load_dim_product():
    print("Loading dim_product...")

    products = pd.read_sql(
        "SELECT * FROM productt",
        engine_oltp
    )

    products = products[
        [
            "product_id",
            "product_name",
            "shop_id",
            "category_id",
            "price",
            "stock",
            "descriptions"
        ]
    ]

    products.to_sql(
        "dim_product",
        engine_dwh,
        if_exists="append",
        index=False,
        dtype={
            "product_name": NVARCHAR(50),
            "descriptions": NVARCHAR(200)
        }
    )

    print("dim_product loaded")
#DIM_SHOP
def load_dim_shop():
    print("Loading dim_shop...")

    shops = pd.read_sql(
        "SELECT * FROM shop",
        engine_oltp
    )

    shops = shops[
        [
            "shop_id",
            "shop_name",
            "userr_id"
        ]
    ]

    shops.to_sql(
        "dim_shop",
        engine_dwh,
        if_exists="append",
        index=False,
        dtype={
            "shop_name": NVARCHAR(50)
        }
    )

    print("dim_shop loaded")

#DIM_CATEGORY

def load_dim_category():

    print("Loading dim_category...")

    categories = pd.read_sql(
        "SELECT * FROM catgory",
        engine_oltp
    )

    categories = categories[
        [
            "category_id",
            "category_name"
        ]
    ]

    categories.to_sql(
        "dim_category",
        engine_dwh,
        if_exists="append",
        index=False,
        dtype={
            "category_name": NVARCHAR(50)
        }
    )

    print("dim_category loaded")

#DIM_DATE
def load_dim_date():

    print("Loading dim_date...")

    dates = pd.date_range(
        start="2026-01-01",
        end="2026-12-31",
        freq="D"
    )

    dim_date = pd.DataFrame({
        "full_date": dates
    })

    dim_date["date_key"] = (
        dim_date["full_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["year"] = dim_date["full_date"].dt.year

    dim_date = dim_date[
        [
            "date_key",
            "full_date",
            "day",
            "month",
            "quarter",
            "year"
        ]
    ]

    dim_date.to_sql(
        "dim_date",
        engine_dwh,
        if_exists="append",
        index=False
    )

    print("dim_date loaded")

#FACT_SALES
def load_fact_sales():
     print("Loading fact_sales...")
     # Extract từ OLTP
     orders = pd.read_sql(
        "SELECT * FROM orderr",
        engine_oltp
    )

     order_items = pd.read_sql(
        "SELECT * FROM order_item",
        engine_oltp
    )
     products = pd.read_sql(
        """
        SELECT
            product_id,
            shop_id,
            category_id
        FROM productt
        """,
        engine_oltp
    )
     # Merge source data
     sales = order_items.merge(
        products,
        on="product_id",
        how="left"
    )
     sales = sales.merge(
        orders[
            [
                "order_id",
                "userr_id",
                "order_date"
            ]
        ],
        on="order_id",
        how="left"
    )
      # Lookup DIM USER

     dim_user_lookup = pd.read_sql(
        """
        SELECT user_key, userr_id
        FROM dim_user
        """,
        engine_dwh
    )
     sales = sales.merge(
        dim_user_lookup,
        on="userr_id",
        how="left"
    )
     #Lookup DIM PRODUCT
     dim_product_lookup = pd.read_sql(
        """
        SELECT product_key, product_id
        FROM dim_product
        """,
        engine_dwh
    )

     sales = sales.merge(
        dim_product_lookup,
        on="product_id",
        how="left"
    )
     # Lookup DIM SHOP
     dim_shop_lookup = pd.read_sql(
        """
        SELECT shop_key, shop_id
        FROM dim_shop
        """,
        engine_dwh
    )

     sales = sales.merge(
        dim_shop_lookup,
        on="shop_id",
        how="left"
    )
     # Lookup DIM CATEGORY
     dim_category_lookup = pd.read_sql(
        """
        SELECT category_key, category_id
        FROM dim_category
        """,
        engine_dwh
    )

     sales = sales.merge(
        dim_category_lookup,
        on="category_id",
        how="left"
    )
     # Lookup DIM DATE
     dim_date_lookup = pd.read_sql(
        """
        SELECT date_key, full_date
        FROM dim_date
        """,
        engine_dwh
    )

     sales["order_date"] = pd.to_datetime(
        sales["order_date"]
    ).dt.date

     dim_date_lookup["full_date"] = pd.to_datetime(
        dim_date_lookup["full_date"]
    ).dt.date

     sales = sales.merge(
        dim_date_lookup,
        left_on="order_date",
        right_on="full_date",
        how="left"
    )
     # Transform
     sales["sales_amount"] = (
        sales["quantity"]
        * sales["unit_price"]
    )

     fact_sales = sales[
        [
            "order_id",
            "user_key",
            "product_key",
            "shop_key",
            "category_key",
            "date_key",
            "quantity",
            "unit_price",
            "sales_amount"
        ]
    ]
     # Load DWH
     fact_sales.to_sql(
        "fact_sales",
        engine_dwh,
        if_exists="append",
        index=False
    )

     print("fact_sales loaded")

#FULL_LOAD
def run_full_load():

    
    print("START FULL LOAD")
    

    load_dim_user()
    load_dim_shop()
    load_dim_category()
    load_dim_product()
    load_dim_date()

    load_fact_sales()

  
    print("FULL LOAD COMPLETED")
   

#WATERMARK-INCREMENTAL
def get_watermark(engine_dwh):
    query = text("""
    SELECT last_watermark
    FROM etl_watermark
    WHERE pipeline_name = 'order_pipeline'
"""
    )
    with engine_dwh.connect() as conn:
        df = pd.read_sql(query,conn)

        return df.iloc[0]["last_watermark"]

    last_watermark = get_watermark(engine_dwh)

    print(last_watermark)

def extract_orders_incremental(
    engine_oltp,
    last_watermark
):

    query = text("""
        SELECT *
        FROM orderr
        WHERE updated_at > :last_watermark
    """)

    with engine_oltp.connect() as conn:

        df = pd.read_sql(
            query,
            conn,
            params={
                "last_watermark": last_watermark
            }
        )

    return df

def run_incremental_order():


    print("START INCREMENTAL LOAD")
    

    # 1. Lấy watermark cũ
    last_watermark = get_watermark(
        engine_dwh
    )

    print(
        "Last watermark:",
        last_watermark
    )

    # 2. Extract order mới/thay đổi
    orders = extract_orders_incremental(
        engine_oltp,
        last_watermark
    )

    print(
        "Number of changed orders:",
        len(orders)
    )

    # Không có dữ liệu mới
    if orders.empty:
        print("No changed orders.")
        return

    # 3. Xác định watermark mới
    new_watermark = orders[
        "updated_at"
    ].max()

    print(
        "New watermark:",
        new_watermark
    )

    # 4. Transform + lookup DIM
    fact_sales = build_incremental_fact_sales(
        orders
    )

    print(
        "Number of fact rows:",
        len(fact_sales)
    )

    # 5. Các order cần refresh trong fact
    changed_order_ids = (
        orders["order_id"]
        .drop_duplicates()
        .tolist()
    )

    # 6. Load + update watermark
    load_incremental_fact_sales(
        fact_sales,
        changed_order_ids,
        new_watermark
    )

    print("==============================")
    print("INCREMENTAL LOAD COMPLETED")
    print("==============================")
################################################
def build_incremental_fact_sales(changed_orders):

    # Lấy danh sách order_id vừa thay đổi
    order_ids = changed_orders["order_id"].tolist()

    # Lấy order_item chỉ thuộc những order vừa thay đổi
    query = text("""
        SELECT *
        FROM order_item
        WHERE order_id IN :order_ids
    """).bindparams(
        bindparam("order_ids", expanding=True)
    )

    with engine_oltp.connect() as conn:
        order_items = pd.read_sql(
            query,
            conn,
            params={
                "order_ids": order_ids
            }
        )

    # Ghép order_item với thông tin order
    sales = order_items.merge(
        changed_orders[
            [
                "order_id",
                "userr_id",
                "order_date"
            ]
        ],
        on="order_id",
        how="inner"
    )

   
    # LOOKUP DIM PRODUCT
   

    dim_product_lookup = pd.read_sql(
        """
        SELECT
            product_key,
            product_id,
            shop_id,
            category_id
        FROM dim_product
        """,
        engine_dwh
    )

    sales = sales.merge(
        dim_product_lookup,
        on="product_id",
        how="left"
    )

    
    # LOOKUP DIM USER
   

    dim_user_lookup = pd.read_sql(
        """
        SELECT user_key, userr_id
        FROM dim_user
        """,
        engine_dwh
    )

    sales = sales.merge(
        dim_user_lookup,
        on="userr_id",
        how="left"
    )


    # LOOKUP DIM SHOP
   

    dim_shop_lookup = pd.read_sql(
        """
        SELECT shop_key, shop_id
        FROM dim_shop
        """,
        engine_dwh
    )

    sales = sales.merge(
        dim_shop_lookup,
        on="shop_id",
        how="left"
    )


    # LOOKUP DIM CATEGORY
  

    dim_category_lookup = pd.read_sql(
        """
        SELECT category_key, category_id
        FROM dim_category
        """,
        engine_dwh
    )

    sales = sales.merge(
        dim_category_lookup,
        on="category_id",
        how="left"
    )

    
    # LOOKUP DIM DATE
    

    dim_date_lookup = pd.read_sql(
        """
        SELECT date_key, full_date
        FROM dim_date
        """,
        engine_dwh
    )

    sales["order_date"] = pd.to_datetime(
        sales["order_date"]
    ).dt.date

    dim_date_lookup["full_date"] = pd.to_datetime(
        dim_date_lookup["full_date"]
    ).dt.date

    sales = sales.merge(
        dim_date_lookup,
        left_on="order_date",
        right_on="full_date",
        how="left"
    )

  
    # TRANSFORM
 

    sales["sales_amount"] = (
        sales["quantity"]
        * sales["unit_price"]
    )

    fact_sales = sales[
        [
            "order_id",
            "user_key",
            "product_key",
            "shop_key",
            "category_key",
            "date_key",
            "quantity",
            "unit_price",
            "sales_amount"
        ]
    ]

    return fact_sales
#########################################
def update_watermark(conn, new_watermark):

    query = text("""
        UPDATE etl_watermark
        SET last_watermark = :new_watermark
        WHERE pipeline_name = 'order_pipeline'
    """)

    conn.execute(
        query,
        {
            "new_watermark": new_watermark
        }
    )
########################################
def load_incremental_fact_sales(
    fact_sales,
    changed_order_ids,
    new_watermark
):

    with engine_dwh.begin() as conn:

        # Xóa dữ liệu cũ của các order vừa thay đổi
        for order_id in changed_order_ids:

            conn.execute(
                text("""
                    DELETE FROM fact_sales
                    WHERE order_id = :order_id
                """),
                {
                    "order_id": order_id
                }
            )

        # Insert phiên bản mới
        if not fact_sales.empty:

            fact_sales.to_sql(
                "fact_sales",
                conn,
                if_exists="append",
                index=False
            )

        # Chỉ update watermark sau khi load thành công
        update_watermark(
            conn,
            new_watermark
        )
if __name__ == "__main__":
    run_incremental_order()
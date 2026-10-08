# ShopeeMini ETL Pipeline & Data Warehouse

A personal Data Engineering project that simulates a small e-commerce system and implements an ETL pipeline from an OLTP database to a Data Warehouse using Python, Pandas, SQL Server, SQLAlchemy, and PyODBC.

The project also supports **watermark-based incremental loading** to process only newly created or modified orders instead of reloading the entire dataset.

---

## Project Overview

The project consists of two main databases:

- `shopeemini`: OLTP database containing transactional e-commerce data.
- `shopeemini_dwh`: Data Warehouse used for analytical workloads.

The ETL pipeline extracts data from the OLTP database, transforms and enriches it using Pandas, performs surrogate key lookups, and loads the processed data into a Star Schema Data Warehouse.

---

## Architecture

```text
                SQL Server OLTP
                  shopeemini
                       |
                       |
                 Extract Data
                       |
                       v
              Python / Pandas ETL
                       |
              -------------------
              |                 |
          Transform         DIM Lookup
              |                 |
              -------------------
                       |
                       v
              SQL Server DWH
               shopeemini_dwh
                       |
          -------------------------
          |                       |
      Dimensions              fact_sales
          |
          v
   Incremental Watermark
```

For incremental loading:

```text
UPDATE orderr
      |
      v
SQL Server Trigger
      |
      v
updated_at changes
      |
      v
Python reads watermark
      |
      v
SELECT rows where
updated_at > last_watermark
      |
      v
Transform + DIM Lookup
      |
      v
Refresh affected fact_sales rows
      |
      v
Update watermark
```

---

## Technologies

- Python
- Pandas
- SQL Server
- SQLAlchemy
- PyODBC
- ODBC Driver 18 for SQL Server
- Git / GitHub
- Python dotenv

---

## OLTP Database

Database:

```text
shopeemini
```

Main tables include:

- `User`
- `shop`
- `catgory`
- `productt`
- `cart`
- `cart_item`
- `orderr`
- `order_item`
- `review`

The `orderr` table includes an additional column:

```sql
updated_at DATETIME2(0)
```

This column is used to track the latest modification time of each order for incremental processing.

A SQL Server trigger automatically updates `updated_at` whenever an order is modified.

---

## Data Warehouse

Database:

```text
shopeemini_dwh
```

The Data Warehouse follows a Star Schema design.

### Dimension Tables

- `dim_user`
- `dim_product`
- `dim_shop`
- `dim_category`
- `dim_date`

The dimension tables use surrogate keys such as:

```text
user_key
product_key
shop_key
category_key
date_key
```

These keys are looked up during the ETL process before loading data into the fact table.

### Fact Table

`fact_sales` stores sales transaction data such as:

```text
order_id
user_key
product_key
shop_key
category_key
date_key
quantity
unit_price
sales_amount
```

Sales amount is calculated as:

```text
sales_amount = quantity × unit_price
```

---

## ETL Process

### 1. Extract

Data is extracted from the SQL Server OLTP database using Pandas and SQLAlchemy.

Example sources:

```text
orderr
order_item
productt
User
shop
catgory
```

### 2. Transform

The pipeline performs transformations including:

- Selecting required columns
- Merging order and order item data
- Calculating sales amount
- Converting date formats
- Performing Dimension lookups
- Mapping OLTP business keys to Data Warehouse surrogate keys

Example:

```text
userr_id
    ↓
dim_user lookup
    ↓
user_key
```

Similarly:

```text
product_id  → product_key
shop_id     → shop_key
category_id → category_key
order_date  → date_key
```

### 3. Load

Processed data is loaded into:

```text
dim_user
dim_product
dim_shop
dim_category
dim_date
fact_sales
```

The project separates the initial Full Load from subsequent Incremental Loads.

---

## Incremental Loading

The project implements **timestamp-based watermark incremental loading**.

Instead of extracting the entire `orderr` table every time, the ETL pipeline only selects records where:

```sql
updated_at > last_watermark
```

The last successfully processed timestamp is stored in:

```text
etl_watermark
```

Example structure:

```text
pipeline_name      last_watermark
order_pipeline     2026-10-07 14:30:00
```

### Incremental Flow

```text
1. Read last watermark from DWH
2. Extract changed orders from OLTP
3. Retrieve related order_item records
4. Transform the changed data
5. Perform Dimension surrogate key lookups
6. Refresh affected fact_sales records
7. Update watermark after a successful load
```

For affected orders, the pipeline removes the previous fact rows and inserts the latest version.

This prevents duplicate records when the ETL pipeline is executed multiple times.

---

## Transaction Handling

Incremental loading is executed using a database transaction.

The load follows this logic:

```text
DELETE affected fact rows
        ↓
INSERT updated fact rows
        ↓
UPDATE watermark
        ↓
COMMIT
```

If an error occurs during the load:

```text
ROLLBACK
```

This prevents the watermark from advancing when the data has not been successfully loaded.

---

## Project Structure

```text
shopee-mini-etl/
│
├── src/
│   └── etl.py
│
├── sql/
│   ├── create_tables.sql
│   ├── insert_data.sql
│   ├── create_dwh_tables.sql
│   └── incremental_setup.sql
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### SQL Files

`create_tables.sql`

Creates the ShopeeMini OLTP database and transactional tables.

`insert_data.sql`

Inserts sample e-commerce data into the OLTP database.

`create_dwh_tables.sql`

Creates Dimension and Fact tables for the Data Warehouse.

`incremental_setup.sql`

Contains SQL objects required for incremental loading, including:

- `etl_watermark`
- `orderr.updated_at`
- SQL Server trigger for tracking order updates

---

## Environment Configuration

Database credentials are stored using environment variables.

Example `.env.example`:

```env
DB_SERVER=your_server
DB_USER=your_username
DB_PASSWORD=your_password
```

The real `.env` file is excluded from Git using `.gitignore`.

---

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Example required packages:

```text
pandas
sqlalchemy
pyodbc
python-dotenv
```

---

## Running the ETL Pipeline

Run:

```bash
python3 src/etl.py
```

The current execution mode runs the incremental order pipeline.

The process reads the previous watermark and extracts only orders that have changed since the last successful ETL run.

Example output:

```text
START INCREMENTAL LOAD

Last watermark: 2026-10-07 14:30:00

Number of changed orders: 1

New watermark: 2026-10-08 09:20:15

INCREMENTAL LOAD COMPLETED
```

Running the pipeline again without changing any orders should return:

```text
Number of changed orders: 0
No changed orders.
```

---

## Key Concepts Practiced

This project was built to practice Data Engineering concepts including:

- OLTP database design
- ETL pipeline development
- Data transformation with Pandas
- Data Warehouse design
- Star Schema
- Dimension and Fact tables
- Surrogate keys
- Dimension key lookup
- Full Load
- Incremental Load
- Timestamp Watermark
- SQL Server Triggers
- Transaction handling
- Idempotent ETL processing
- Environment variable management
- Git / GitHub version control

---

## Current Limitation

The current incremental pipeline detects changes based on:

```text
orderr.updated_at
```

Therefore, changes made directly to `order_item` are not yet independently tracked unless the corresponding order is marked as updated.

A future improvement is to extend change tracking to `order_item` and Dimension tables.

---

## Future Improvements

- Add change tracking for `order_item`
- Implement incremental loading for Dimension tables
- Implement Slowly Changing Dimensions (SCD)
- Add logging and error handling
- Add ETL job scheduling
- Add data quality validation
- Containerize the pipeline with Docker

---

## Author

Data Engineering personal project developed for learning and practicing ETL, SQL Server, Data Warehouse, and incremental data processing.
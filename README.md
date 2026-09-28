# Shopee Mini - ETL Data Pipeline

A mini e-commerce data engineering project built with SQL Server,
Python and Pandas.

The project simulates a simplified e-commerce system and implements
an ETL pipeline to transform transactional data into an analytical
fact table.

## Project Overview

This project simulates a simplified e-commerce platform similar to Shopee.

The transactional database contains:

- Users
- Shops
- Categories
- Products
- Carts
- Orders
- Payments
- Reviews

The ETL pipeline extracts transactional data from SQL Server,
transforms it using Pandas, and loads the processed data into
a `fact_sales` table.

## Architecture

```text
SQL Server OLTP
       |
       | Extract
       v
     Pandas
       |
       | Transform
       | - Merge orders
       | - Merge order items
       | - Merge products
       | - Merge shops
       | - Merge categories
       | - Calculate sales_amount
       v
   fact_sales
       |
       | Load
       v
   SQL Server
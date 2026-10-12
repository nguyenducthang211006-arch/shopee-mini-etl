CREATE DATABASE shopeemini_dwh;
GO

USE shopeemini_dwh;
GO
CREATE TABLE fact_sales (
    sales_key INT IDENTITY(1,1) PRIMARY KEY,
    order_id VARCHAR(50),
    user_key INT,
    product_key INT,
    shop_key INT,
    category_key INT,
    date_key INT,
    quantity INT,
    unit_price DECIMAL(18,2),
    sales_amount DECIMAL(18,2)
);
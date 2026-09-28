USE shopeemini;
GO

CREATE TABLE fact_sales (
    order_id VARCHAR(50),
    order_date DATE,
    userr_id INT,
    product_id VARCHAR(50),
    product_name NVARCHAR(50),
    shop_id INT,
    shop_name NVARCHAR(50),
    category_id VARCHAR(50),
    category_name NVARCHAR(50),
    quantity INT,
    unit_price DECIMAL(18,2),
    sales_amount DECIMAL(18,2)
);
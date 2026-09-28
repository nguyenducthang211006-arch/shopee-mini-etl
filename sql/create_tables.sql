CREATE DATABASE shopeemini;
GO

USE shopeemini;
GO

CREATE TABLE [User](
    userr_id INT PRIMARY KEY,
    userr_name NVARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(50),
    passwordd VARCHAR(50)
);

CREATE TABLE shop(
    shop_id INT PRIMARY KEY,
    userr_id INT NOT NULL,
    shop_name NVARCHAR(50),
    FOREIGN KEY (userr_id) REFERENCES [User](userr_id)
);

CREATE TABLE catgory(
    category_id VARCHAR(50) PRIMARY KEY,
    category_name NVARCHAR(50)
);

CREATE TABLE productt(
    product_id VARCHAR(50) PRIMARY KEY,
    product_name NVARCHAR(50),
    shop_id INT NOT NULL,
    category_id VARCHAR(50) NOT NULL,
    price DECIMAL(18,2),
    stock INT,
    descriptions NVARCHAR(200),
    FOREIGN KEY (shop_id) REFERENCES shop(shop_id),
    FOREIGN KEY (category_id) REFERENCES catgory(category_id)
);

CREATE TABLE cart(
    cart_id VARCHAR(50) PRIMARY KEY,
    userr_id INT NOT NULL,
    FOREIGN KEY (userr_id) REFERENCES [User](userr_id)
);

CREATE TABLE cart_item(
    cart_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (cart_id, product_id),
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
    FOREIGN KEY (product_id) REFERENCES productt(product_id)
);

CREATE TABLE orderr(
    order_id VARCHAR(50) PRIMARY KEY,
    userr_id INT NOT NULL,
    order_date DATE,
    status VARCHAR(50),
    total_amont INT,
    shipping_address NVARCHAR(50),
    FOREIGN KEY (userr_id) REFERENCES [User](userr_id)
);

CREATE TABLE order_item(
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INT,
    unit_price DECIMAL(18,2),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orderr(order_id),
    FOREIGN KEY (product_id) REFERENCES productt(product_id)
);

CREATE TABLE payment(
    payment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    paid_at DATE,
    FOREIGN KEY (order_id) REFERENCES orderr(order_id)
);

CREATE TABLE review(
    review_id VARCHAR(50) PRIMARY KEY,
    userr_id INT NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment NVARCHAR(100),
    FOREIGN KEY (userr_id) REFERENCES [User](userr_id),
    FOREIGN KEY (product_id) REFERENCES productt(product_id)
);
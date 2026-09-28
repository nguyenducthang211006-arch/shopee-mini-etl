INSERT INTO [User] (userr_id, userr_name, email, phone, passwordd)
VALUES
(1, N'Nguyễn Văn An', 'an@gmail.com', '0901000001', '123456'),
(2, N'Trần Văn Bình', 'binh@gmail.com', '0901000002', '123456'),
(3, N'Lê Minh Cường', 'cuong@gmail.com', '0901000003', '123456'),
(4, N'Phạm Hoàng Dũng', 'dung@gmail.com', '0901000004', '123456'),
(5, N'Đỗ Thị Hà', 'ha@gmail.com', '0901000005', '123456'),
(6, N'Vũ Thị Lan', 'lan@gmail.com', '0901000006', '123456'),
(7, N'Hoàng Đức Nam', 'nam@gmail.com', '0901000007', '123456'),
(8, N'Nguyễn Thị Mai', 'mai@gmail.com', '0901000008', '123456'),
(9, N'Phan Quốc Việt', 'viet@gmail.com', '0901000009', '123456'),
(10, N'Bùi Thanh Tùng', 'tung@gmail.com', '0901000010', '123456');

INSERT INTO shop (shop_id, userr_id, shop_name)
VALUES
(101, 1, N'Shop Công Nghệ An'),
(102, 2, N'Bình Mobile'),
(103, 3, N'Cường Gia Dụng'),
(104, 4, N'Dũng Store'),
(105, 5, N'Hà Fashion');

INSERT INTO catgory (category_id, category_name)
VALUES
('C01', N'Điện thoại'),
('C02', N'Laptop'),
('C03', N'Phụ kiện'),
('C04', N'Gia dụng'),
('C05', N'Thời trang'),
('C06', N'Đồ điện tử');

INSERT INTO productt
(product_id, product_name, shop_id, category_id, price, stock, descriptions)
VALUES
('P001', N'iPhone 15', 101, 'C01', 20000000, 10, N'Điện thoại Apple iPhone 15'),
('P002', N'iPhone 15 Pro', 101, 'C01', 25000000, 8, N'Điện thoại Apple iPhone 15 Pro'),
('P003', N'Samsung Galaxy S24', 102, 'C01', 18000000, 15, N'Điện thoại Samsung Galaxy S24'),
('P004', N'Xiaomi Redmi Note 13', 102, 'C01', 6000000, 20, N'Điện thoại Xiaomi'),
('P005', N'MacBook Air M2', 101, 'C02', 24000000, 7, N'Laptop Apple MacBook Air M2'),
('P006', N'Dell Inspiron 15', 104, 'C02', 16000000, 12, N'Laptop Dell Inspiron'),
('P007', N'Lenovo IdeaPad 5', 104, 'C02', 15000000, 9, N'Laptop Lenovo'),
('P008', N'Chuột Logitech G102', 101, 'C03', 500000, 30, N'Chuột gaming Logitech'),
('P009', N'Bàn phím cơ AKKO', 101, 'C03', 1500000, 18, N'Bàn phím cơ AKKO'),
('P010', N'Tai nghe Bluetooth', 102, 'C03', 800000, 25, N'Tai nghe Bluetooth không dây'),
('P011', N'Nồi cơm điện Sharp', 103, 'C04', 1200000, 20, N'Nồi cơm điện gia đình'),
('P012', N'Máy xay sinh tố', 103, 'C04', 900000, 14, N'Máy xay sinh tố'),
('P013', N'Áo Hoodie', 105, 'C05', 450000, 40, N'Áo Hoodie thời trang'),
('P014', N'Quần Jeans', 105, 'C05', 600000, 35, N'Quần Jeans nam nữ'),
('P015', N'Đồng hồ thông minh', 104, 'C06', 2500000, 11, N'Đồng hồ thông minh'),
('P016', N'Loa Bluetooth JBL', 104, 'C06', 3000000, 13, N'Loa Bluetooth JBL'),
('P017', N'Sạc nhanh 65W', 101, 'C03', 700000, 22, N'Củ sạc nhanh 65W'),
('P018', N'USB 64GB', 102, 'C03', 250000, 50, N'USB dung lượng 64GB'),
('P019', N'Màn hình 24 inch', 104, 'C06', 4000000, 6, N'Màn hình máy tính 24 inch'),
('P020', N'Balo Laptop', 105, 'C05', 800000, 17, N'Balo đựng laptop');

INSERT INTO cart (cart_id, userr_id)
VALUES
('CART01', 1),
('CART02', 2),
('CART03', 3),
('CART04', 4),
('CART05', 5),
('CART06', 6),
('CART07', 7),
('CART08', 8);

INSERT INTO cart_item (cart_id, product_id, quantity)
VALUES
('CART01', 'P001', 1),
('CART01', 'P008', 2),
('CART02', 'P003', 1),
('CART02', 'P010', 1),
('CART03', 'P005', 1),
('CART03', 'P009', 2),
('CART04', 'P011', 1),
('CART04', 'P012', 1),
('CART05', 'P013', 2),
('CART05', 'P014', 1),
('CART06', 'P006', 1),
('CART06', 'P017', 2),
('CART07', 'P015', 1),
('CART08', 'P019', 1);

INSERT INTO orderr
(order_id, userr_id, order_date, status, total_amont, shipping_address)
VALUES
('O001', 1, '2026-09-20', 'Completed', 21000000, N'Hà Nội'),
('O002', 2, '2026-09-20', 'Completed', 18800000, N'Hải Phòng'),
('O003', 3, '2026-09-21', 'Completed', 27000000, N'Hà Nội'),
('O004', 4, '2026-09-21', 'Pending', 16000000, N'Đà Nẵng'),
('O005', 5, '2026-09-22', 'Completed', 1500000, N'Hà Nội'),
('O006', 6, '2026-09-22', 'Shipping', 2900000, N'Hồ Chí Minh'),
('O007', 7, '2026-09-23', 'Completed', 2500000, N'Hà Nội'),
('O008', 8, '2026-09-23', 'Cancelled', 4000000, N'Bắc Ninh'),
('O009', 1, '2026-09-24', 'Completed', 3000000, N'Hà Nội'),
('O010', 3, '2026-09-24', 'Pending', 6500000, N'Hải Dương');

INSERT INTO order_item
(order_id, product_id, quantity, unit_price)
VALUES
('O001', 'P001', 1, 20000000),
('O001', 'P008', 2, 500000),
('O002', 'P003', 1, 18000000),
('O002', 'P010', 1, 800000),
('O003', 'P005', 1, 24000000),
('O003', 'P009', 2, 1500000),
('O004', 'P006', 1, 16000000),
('O005', 'P013', 2, 450000),
('O005', 'P014', 1, 600000),
('O006', 'P006', 1, 16000000),
('O006', 'P017', 2, 700000),
('O007', 'P015', 1, 2500000),
('O008', 'P019', 1, 4000000),
('O009', 'P016', 1, 3000000),
('O010', 'P004', 1, 6000000),
('O010', 'P018', 2, 250000);

INSERT INTO payment
(payment_id, order_id, payment_method, payment_status, paid_at)
VALUES
('PAY001', 'O001', 'Banking', 'Paid', '2026-09-20'),
('PAY002', 'O002', 'COD', 'Paid', '2026-09-20'),
('PAY003', 'O003', 'Banking', 'Paid', '2026-09-21'),
('PAY004', 'O004', 'COD', 'Pending', NULL),
('PAY005', 'O005', 'Banking', 'Paid', '2026-09-22'),
('PAY006', 'O006', 'COD', 'Paid', '2026-09-22'),
('PAY007', 'O007', 'Banking', 'Paid', '2026-09-23'),
('PAY008', 'O008', 'Banking', 'Refunded', NULL),
('PAY009', 'O009', 'COD', 'Paid', '2026-09-24'),
('PAY010', 'O010', 'Banking', 'Pending', NULL);

INSERT INTO review
(review_id, userr_id, product_id, rating, comment)
VALUES
('R001', 1, 'P001', 5, N'Sản phẩm rất tốt'),
('R002', 2, 'P003', 4, N'Điện thoại dùng ổn'),
('R003', 3, 'P005', 5, N'Laptop rất tốt'),
('R004', 4, 'P006', 4, N'Đóng gói cẩn thận'),
('R005', 5, 'P013', 5, N'Áo đẹp'),
('R006', 6, 'P017', 4, N'Sạc nhanh tốt'),
('R007', 7, 'P015', 5, N'Đồng hồ đẹp'),
('R008', 8, 'P019', 4, N'Màn hình khá tốt'),
('R009', 1, 'P008', 5, N'Chuột dùng tốt'),
('R010', 3, 'P009', 4, N'Bàn phím đẹp');

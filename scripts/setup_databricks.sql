-- RetailOps 360 | Databricks SQL / Unity Catalog
-- Change catalog if you selected a different name.
CREATE CATALOG IF NOT EXISTS retailops360;
CREATE SCHEMA IF NOT EXISTS retailops360.source;
USE CATALOG retailops360;
USE SCHEMA source;

CREATE TABLE IF NOT EXISTS customers (customer_id BIGINT, customer_name STRING, city STRING, province STRING, signup_date DATE, acquisition_channel STRING) USING DELTA;
CREATE TABLE IF NOT EXISTS products (product_id BIGINT, product_name STRING, category STRING, list_price DECIMAL(12,2), product_status STRING) USING DELTA;
CREATE TABLE IF NOT EXISTS customer_addresses (address_id BIGINT, customer_id BIGINT, address_type STRING, city STRING, province STRING) USING DELTA;
CREATE TABLE IF NOT EXISTS orders (order_id BIGINT, customer_id BIGINT, order_date DATE, expected_delivery_date DATE, order_status STRING, order_amount DECIMAL(12,2), sales_channel STRING) USING DELTA;
CREATE TABLE IF NOT EXISTS order_items (order_item_id BIGINT, order_id BIGINT, product_id BIGINT, quantity INT, unit_price DECIMAL(12,2)) USING DELTA;
CREATE TABLE IF NOT EXISTS payments (payment_id BIGINT, order_id BIGINT, payment_amount DECIMAL(12,2), payment_method STRING, payment_date DATE, payment_status STRING) USING DELTA;
CREATE TABLE IF NOT EXISTS shipments (shipment_id BIGINT, order_id BIGINT, delivered_date DATE, shipment_status STRING, shipping_method STRING) USING DELTA;
CREATE TABLE IF NOT EXISTS returns (return_id BIGINT, order_id BIGINT, product_id BIGINT, return_date DATE, return_reason STRING, return_status STRING) USING DELTA;

-- Create a volume first and upload CSVs into it. Replace the path if needed.
CREATE VOLUME IF NOT EXISTS source_files;

COPY INTO customers FROM '/Volumes/retailops360/source/source_files/customers.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO products FROM '/Volumes/retailops360/source/source_files/products.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO customer_addresses FROM '/Volumes/retailops360/source/source_files/customer_addresses.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO orders FROM '/Volumes/retailops360/source/source_files/orders.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO order_items FROM '/Volumes/retailops360/source/source_files/order_items.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO payments FROM '/Volumes/retailops360/source/source_files/payments.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO shipments FROM '/Volumes/retailops360/source/source_files/shipments.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');
COPY INTO returns FROM '/Volumes/retailops360/source/source_files/returns.csv' FILEFORMAT = CSV FORMAT_OPTIONS ('header'='true');

-- Expected counts, in order: 15000, 2500, 30000, 55000, 105571, 55685, 43854, 3415
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'customer_addresses', COUNT(*) FROM customer_addresses
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'shipments', COUNT(*) FROM shipments
UNION ALL SELECT 'returns', COUNT(*) FROM returns;

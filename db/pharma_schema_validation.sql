USE pharma_db;

-- Check that the tables are present in the db
SHOW TABLES;

-- Check that all of the rows in each table have been imported
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM suppliers;
SELECT COUNT(*) FROM raw_materials;
SELECT COUNT(*) FROM drugs;
SELECT COUNT(*) FROM drug_formulations;
SELECT COUNT(*) FROM drug_batches;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_items;

-- Confirm the structure of each table, PKs and FKs
SHOW CREATE TABLE customers;
SHOW CREATE TABLE suppliers;
SHOW CREATE TABLE raw_materials;
SHOW CREATE TABLE drugs;
SHOW CREATE TABLE drug_formulations;
SHOW CREATE TABLE drug_batches;
SHOW CREATE TABLE orders;
SHOW CREATE TABLE order_items;
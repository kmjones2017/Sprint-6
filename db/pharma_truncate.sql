USE pharma_db;

-- Temporarily disable FK checks so TRUNCATE works cleanly
SET FOREIGN_KEY_CHECKS = 0;

-- Child tables first
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;

TRUNCATE TABLE drug_batches;
TRUNCATE TABLE drug_formulations;

TRUNCATE TABLE raw_materials;

-- Parent tables
TRUNCATE TABLE drugs;
TRUNCATE TABLE customers;
TRUNCATE TABLE suppliers;

-- Re-enable FK checks
SET FOREIGN_KEY_CHECKS = 1;
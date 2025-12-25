/*
Join validation
If any of the following queries returns any rows, it's a foreign key violation
*/

-- if necessary, make sure to connect to the correct database
USE pharma_db;

-- Orders with missing customers 
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Order items without orders
SELECT oi.order_item_id, oi.order_id
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

-- Order items that don't belong to any drug batches
SELECT oi.order_item_id, oi.batch_id
FROM order_items oi
LEFT JOIN drug_batches db ON oi.batch_id = db.batch_id
WHERE db.batch_id IS NULL;

-- Drug batches that don't have drug IDs
SELECT db.batch_id, db.drug_id
FROM drug_batches db
LEFT JOIN drugs d ON db.drug_id = d.drug_id
WHERE d.drug_id IS NULL;

-- Drug formulations without a drug ID
SELECT df.formulation_id, df.drug_id
FROM drug_formulations df
LEFT JOIN drugs d ON df.drug_id = d.drug_id
WHERE d.drug_id IS NULL;

-- Drug formulations with raw mats that don't exist in the database
SELECT df.formulation_id, df.material_id
FROM drug_formulations df
LEFT JOIN raw_materials rm ON df.material_id = rm.material_id
WHERE rm.material_id IS NULL;

-- Raw mats that don't have a supplier
SELECT rm.material_id, rm.supplier_id
FROM raw_materials rm
LEFT JOIN suppliers s ON rm.supplier_id = s.supplier_id
WHERE s.supplier_id IS NULL;

/*
Aggregation Checks
For general knowledge about the data and explaining any oddities in the join validation query results
(Specifically, expected missing joins)
*/

-- Orders per customer
SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Orders per drug batch
SELECT db.batch_id, db.batch_number, COUNT(oi.order_item_id) AS total_items
FROM drug_batches db
LEFT JOIN order_items oi ON db.batch_id = oi.batch_id
GROUP BY db.batch_id, db.batch_number;

-- Batches per drug
SELECT d.drug_id, d.drug_name, COUNT(db.batch_id) AS batch_count
FROM drugs d
LEFT JOIN drug_batches db ON d.drug_id = db.drug_id
GROUP BY d.drug_id, d.drug_name;


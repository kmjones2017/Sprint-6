-- Show all customers
SELECT * FROM customers;

-- Find all orders placed by City General Hospital
SELECT o.order_id, o.order_date, oi.quantity, d.drug_name
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN drug_batches db ON oi.batch_id = db.batch_id
JOIN drugs d ON db.drug_id = d.drug_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.name = 'City General Hospital';

-- Trace an order back to its raw materials and suppliers
SELECT o.order_id, d.drug_name, rm.material_name, s.supplier_name, s.country
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN drug_batches db ON oi.batch_id = db.batch_id
JOIN drugs d ON db.drug_id = d.drug_id
JOIN drug_formulations df ON d.drug_id = df.drug_id
JOIN raw_materials rm ON df.material_id = rm.material_id
JOIN suppliers s ON rm.supplier_id = s.supplier_id
WHERE o.order_id = 1;

-- Count how many orders each customer has placed
SELECT c.name AS customer_name, COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- List drugs and the number of batches produced
SELECT d.drug_name, COUNT(db.batch_id) AS batch_count
FROM drugs d
LEFT JOIN drug_batches db ON d.drug_id = db.drug_id
GROUP BY d.drug_id, d.drug_name;

-- Find suppliers providing Magnesium Stearate
SELECT s.supplier_name, s.country
FROM raw_materials rm
JOIN suppliers s ON rm.supplier_id = s.supplier_id
WHERE rm.material_name = 'Magnesium Stearate';


-- Pharmaceutical Manufacturing Schema
CREATE DATABASE IF NOT EXISTS pharma_db;

USE pharma_db;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    customer_type ENUM('Hospital', 'Pharmacy', 'Clinic') NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(20),
    address VARCHAR(255)
);

CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(150) NOT NULL,
    material_type VARCHAR(100),
    contact_email VARCHAR(150),
    country VARCHAR(100)
);

CREATE TABLE raw_materials (
    material_id INT PRIMARY KEY,
    material_name VARCHAR(150) NOT NULL,
    unit_of_measure VARCHAR(50),
    supplier_id INT NOT NULL,
    cost_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE drugs (
    drug_id INT PRIMARY KEY,
    drug_name VARCHAR(150) NOT NULL,
    dosage_form VARCHAR(50),
    strength_mg INT,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE drug_formulations (
    formulation_id INT PRIMARY KEY,
    drug_id INT NOT NULL,
    material_id INT NOT NULL,
    quantity_required DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id),
    FOREIGN KEY (material_id) REFERENCES raw_materials(material_id)
);

CREATE TABLE drug_batches (
    batch_id INT PRIMARY KEY,
    drug_id INT NOT NULL,
    batch_number VARCHAR(100) UNIQUE NOT NULL,
    manufacture_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    quantity_produced INT NOT NULL,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    batch_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (batch_id) REFERENCES drug_batches(batch_id)
);

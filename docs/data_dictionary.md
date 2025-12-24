# Pharmaceutical Manufacturing Data Dictionary

This data dictionary documents the **locked pharmaceutical manufacturing schema** exactly as defined in `pharma_schema.sql`. It describes each table, its columns, keys, and relationships, and includes brief ER-style summaries.

---

## 1. customers

**Description:** Stores information about organizations that purchase manufactured drugs.

| Column        | Type                                 | Description                                           |
| ------------- | ------------------------------------ | ----------------------------------------------------- |
| customer_id   | INT                                  | **Primary Key.** Unique identifier for each customer. |
| name          | VARCHAR(150)                         | Customer name.                                        |
| customer_type | ENUM('Hospital','Pharmacy','Clinic') | Classification of customer.                           |
| email         | VARCHAR(150)                         | Contact email address.                                |
| phone         | VARCHAR(20)                          | Contact phone number.                                 |
| address       | VARCHAR(255)                         | Physical address.                                     |

**Keys & Relationships:**

* PK: `customer_id`
* Referenced by: `orders.customer_id`

**ER Summary:** One customer can place many orders.

---

## 2. suppliers

**Description:** Stores suppliers that provide raw materials.

| Column        | Type         | Description                                  |
| ------------- | ------------ | -------------------------------------------- |
| supplier_id   | INT          | **Primary Key.** Unique supplier identifier. |
| supplier_name | VARCHAR(150) | Supplier name.                               |
| material_type | VARCHAR(100) | General category of materials supplied.      |
| contact_email | VARCHAR(150) | Supplier contact email.                      |
| country       | VARCHAR(100) | Country of operation.                        |

**Keys & Relationships:**

* PK: `supplier_id`
* Referenced by: `raw_materials.supplier_id`

**ER Summary:** One supplier can supply many raw materials.

---

## 3. raw_materials

**Description:** Defines raw materials used in drug manufacturing.

| Column          | Type          | Description                                       |
| --------------- | ------------- | ------------------------------------------------- |
| material_id     | INT           | **Primary Key.** Unique raw material identifier.  |
| material_name   | VARCHAR(150)  | Name of the raw material.                         |
| unit_of_measure | VARCHAR(50)   | Measurement unit (e.g., kg).                      |
| supplier_id     | INT           | **Foreign Key.** Supplier providing the material. |
| cost_per_unit   | DECIMAL(10,2) | Cost per unit of material.                        |

**Keys & Relationships:**

* PK: `material_id`
* FK: `supplier_id` → `suppliers.supplier_id`
* Referenced by: `drug_formulations.material_id`

**ER Summary:** Raw materials belong to one supplier and can be used in many formulations.

---

## 4. drugs

**Description:** Master list of manufactured drugs.

| Column      | Type          | Description                                     |
| ----------- | ------------- | ----------------------------------------------- |
| drug_id     | INT           | **Primary Key.** Unique drug identifier.        |
| drug_name   | VARCHAR(150)  | Commercial drug name.                           |
| dosage_form | VARCHAR(50)   | Form of administration (tablet, capsule, etc.). |
| strength_mg | INT           | Dosage strength in milligrams.                  |
| price       | DECIMAL(10,2) | Standard list price (non-transactional).        |

**Keys & Relationships:**

* PK: `drug_id`
* Referenced by: `drug_formulations.drug_id`, `drug_batches.drug_id`

**ER Summary:** A drug can have multiple formulations and many production batches.

---

## 5. drug_formulations

**Description:** Junction table defining which raw materials are required for each drug.

| Column            | Type          | Description                                 |
| ----------------- | ------------- | ------------------------------------------- |
| formulation_id    | INT           | **Primary Key.** Unique formulation record. |
| drug_id           | INT           | **Foreign Key.** Drug being formulated.     |
| material_id       | INT           | **Foreign Key.** Raw material used.         |
| quantity_required | DECIMAL(10,2) | Amount of material needed per batch.        |

**Keys & Relationships:**

* PK: `formulation_id`
* FK: `drug_id` → `drugs.drug_id`
* FK: `material_id` → `raw_materials.material_id`

**ER Summary:** Resolves the many-to-many relationship between drugs and raw materials.

---

## 6. drug_batches

**Description:** Tracks manufacturing batches for each drug.

| Column            | Type         | Description                                   |
| ----------------- | ------------ | --------------------------------------------- |
| batch_id          | INT          | **Primary Key.** Internal batch identifier.   |
| drug_id           | INT          | **Foreign Key.** Drug produced in this batch. |
| batch_number      | VARCHAR(100) | External/manufacturing batch identifier.      |
| manufacture_date  | DATE         | Date of manufacture.                          |
| expiration_date   | DATE         | Expiration date.                              |
| quantity_produced | INT          | Units produced in the batch.                  |

**Keys & Relationships:**

* PK: `batch_id`
* FK: `drug_id` → `drugs.drug_id`
* Referenced by: `order_items.batch_id`

**ER Summary:** A drug can have many batches; each batch belongs to one drug.

---

## 7. orders

**Description:** Represents customer purchase orders.

| Column      | Type | Description                                  |
| ----------- | ---- | -------------------------------------------- |
| order_id    | INT  | **Primary Key.** Unique order identifier.    |
| customer_id | INT  | **Foreign Key.** Customer placing the order. |
| order_date  | DATE | Date the order was placed.                   |

**Keys & Relationships:**

* PK: `order_id`
* FK: `customer_id` → `customers.customer_id`
* Referenced by: `order_items.order_id`

**ER Summary:** A customer can place many orders; each order belongs to one customer.

---

## 8. order_items

**Description:** Line items for each order, tied to specific drug batches.

| Column        | Type          | Description                                    |
| ------------- | ------------- | ---------------------------------------------- |
| order_item_id | INT           | **Primary Key.** Unique order line identifier. |
| order_id      | INT           | **Foreign Key.** Parent order.                 |
| batch_id      | INT           | **Foreign Key.** Batch sold.                   |
| quantity      | INT           | Units sold.                                    |
| unit_price    | DECIMAL(10,2) | Price per unit at time of sale.                |

**Keys & Relationships:**

* PK: `order_item_id`
* FK: `order_id` → `orders.order_id`
* FK: `batch_id` → `drug_batches.batch_id`

**ER Summary:** Orders contain many order items; each item references a specific batch.

---

## High-Level ER Overview

* Customers → Orders → Order Items → Drug Batches → Drugs
* Drugs ↔ Raw Materials via Drug Formulations
* Suppliers → Raw Materials
* Business identifiers (e.g., batch_number) support traceability and reporting.
* Transactional prices are stored in order_items to preserve historical accuracy.

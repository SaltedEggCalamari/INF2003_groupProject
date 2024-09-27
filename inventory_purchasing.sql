show databases;
use infmaindb;
CREATE TABLE Inventory (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,            -- Unique identifier for each item
    Name VARCHAR(100) NOT NULL,                       -- Name of the inventory item
    Description TEXT,                                 -- Description of the item
    SKU VARCHAR(50),                                  -- Stock Keeping Unit (SKU)
    Model VARCHAR(50),                                -- Model number or name
    Qty INT NOT NULL,                                 -- Quantity in stock
    Location VARCHAR(100),                            -- Location where the item is stored
    RawProd VARCHAR(10),                              -- Whether the item is a raw product (e.g., 'Yes', 'No', or other text)
    CreateDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the record is created
    UpdateDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Timestamp when the record is updated
);

-- Insert additional data for raw components (raw materials)
INSERT INTO Inventory (Name, Description, SKU, Model, Qty, Location, RawProd, CreateDateTime)
VALUES
('Speaker Driver', '4-inch speaker driver for compact speaker models', 'SPK-DRV-002', 'SD-200', 450, 'Warehouse A', 'Raw', NOW()),
('Speaker Driver', '6.5-inch speaker driver for large speaker models', 'SPK-DRV-003', 'SD-300', 300, 'Warehouse A', 'Raw', NOW()),
('Battery', '5000mAh Li-ion battery for portable chargers', 'BATT-LI-004', 'BAT-5000', 600, 'Warehouse B', 'Raw', NOW()),
('Charging Circuit', 'Fast charging circuit board for advanced portable chargers', 'CHG-CIR-006', 'CCB-700', 350, 'Warehouse C', 'Raw', NOW()),
('Plastic Casing', 'Water-resistant plastic casing for outdoor speakers', 'PLS-CASE-003', 'PC-300', 500, 'Warehouse A', 'Raw', NOW()),
('Speaker Cone', 'Large speaker cone for 6.5-inch speaker models', 'SPK-CONE-008', 'SC-800', 200, 'Warehouse A', 'Raw', NOW()),
('Lithium Battery Pack', '10000mAh Li-ion battery pack for high-capacity chargers', 'BATT-PACK-001', 'BATT-10K', 400, 'Warehouse B', 'Raw', NOW()),
('PCB Board', 'Printed Circuit Board for advanced speaker systems', 'PCB-BRD-012', 'PCB-12', 180, 'Warehouse C', 'Raw', NOW());

-- Insert additional data for finished products (speakers and portable chargers)
INSERT INTO Inventory (Name, Description, SKU, Model, Qty, Location, RawProd, CreateDateTime)
VALUES
('Portable Bluetooth Speaker - Compact', '4-inch compact Bluetooth speaker with rechargeable battery', 'SPK-BLU-002', 'BS-400', 100, 'Showroom 1', 'Prod', NOW()),
('Portable Bluetooth Speaker - Outdoor', 'Water-resistant outdoor Bluetooth speaker with 5-hour battery life', 'SPK-BLU-003', 'BS-600', 120, 'Showroom 1', 'Prod', NOW()),
('Portable Bluetooth Speaker - Large', '6.5-inch large Bluetooth speaker with enhanced bass', 'SPK-BLU-004', 'BS-650', 80, 'Showroom 2', 'Prod', NOW()),
('Portable Charger 5000mAh', '5000mAh portable charger with dual USB ports', 'CHG-5000-004', 'PC-5000', 200, 'Showroom 2', 'Prod', NOW()),
('Portable Charger 10000mAh', '10000mAh high-capacity portable charger with fast charging', 'CHG-10000-005', 'PC-10000', 150, 'Showroom 3', 'Prod', NOW());

CREATE TABLE Purchasing (
    PurchasingID INT AUTO_INCREMENT PRIMARY KEY,     -- Unique identifier for each purchase
    PurchasingInvoiceNum VARCHAR(50) NOT NULL,       -- Unique invoice number for the purchase
    ProductName VARCHAR(100) NOT NULL,               -- Name of the product purchased
    Price DECIMAL(10, 2) NOT NULL,                   -- Price of the product at the time of purchase
    Model VARCHAR(50),                               -- Model of the product
    SKU VARCHAR(50),                                 -- Stock Keeping Unit (SKU) of the product
    Qty INT NOT NULL,                                -- Quantity of the product purchased
    PurchasingDate DATE NOT NULL,                    -- Date when the purchase was made
    CreateDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the record was created
    UpdateDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Timestamp when the record was last updated
);

-- Insert 50 purchasing transactions for raw materials

-- Speaker Drivers (Total: 850 units in Inventory)
INSERT INTO Purchasing (PurchasingInvoiceNum, ProductName, Price, Model, SKU, Qty, PurchasingDate)
VALUES 
('INV-001', 'Speaker Driver', 15.50, 'SD-100', 'SPK-DRV-001', 100, '2023-09-01'),
('INV-002', 'Speaker Driver', 15.75, 'SD-100', 'SPK-DRV-001', 50, '2023-09-03'),
('INV-003', 'Speaker Driver', 16.00, 'SD-100', 'SPK-DRV-001', 50, '2023-09-05'),
('INV-004', 'Speaker Driver', 17.00, 'SD-200', 'SPK-DRV-002', 150, '2023-09-07'),
('INV-005', 'Speaker Driver', 18.50, 'SD-200', 'SPK-DRV-002', 100, '2023-09-08'),
('INV-006', 'Speaker Driver', 20.00, 'SD-300', 'SPK-DRV-003', 200, '2023-09-10'),
('INV-007', 'Speaker Driver', 21.50, 'SD-300', 'SPK-DRV-003', 100, '2023-09-12'),
('INV-008', 'Speaker Driver', 22.99, 'SD-300', 'SPK-DRV-003', 100, '2023-09-14'),

-- Batteries (Total: 1400 units in Inventory)
('INV-009', 'Battery', 10.50, 'BAT-3000', 'BATT-LI-003', 300, '2023-09-15'),
('INV-010', 'Battery', 11.00, 'BAT-3000', 'BATT-LI-003', 200, '2023-09-16'),
('INV-011', 'Battery', 12.00, 'BAT-5000', 'BATT-LI-004', 300, '2023-09-18'),
('INV-012', 'Battery', 13.50, 'BAT-5000', 'BATT-LI-004', 300, '2023-09-19'),
('INV-013', 'Battery', 14.99, 'BAT-5000', 'BATT-LI-004', 300, '2023-09-20'),

-- Charging Circuits (Total: 650 units in Inventory)
('INV-014', 'Charging Circuit', 8.50, 'CCB-500', 'CHG-CIR-005', 100, '2023-09-21'),
('INV-015', 'Charging Circuit', 9.00, 'CCB-500', 'CHG-CIR-005', 100, '2023-09-22'),
('INV-016', 'Charging Circuit', 9.50, 'CCB-700', 'CHG-CIR-006', 150, '2023-09-23'),
('INV-017', 'Charging Circuit', 10.50, 'CCB-700', 'CHG-CIR-006', 150, '2023-09-24'),
('INV-018', 'Charging Circuit', 11.00, 'CCB-700', 'CHG-CIR-006', 150, '2023-09-25'),

-- Plastic Casings (Total: 1100 units in Inventory)
('INV-019', 'Plastic Casing', 4.50, 'PC-200', 'PLS-CASE-002', 200, '2023-09-26'),
('INV-020', 'Plastic Casing', 5.00, 'PC-200', 'PLS-CASE-002', 100, '2023-09-27'),
('INV-021', 'Plastic Casing', 5.50, 'PC-200', 'PLS-CASE-002', 100, '2023-09-28'),
('INV-022', 'Plastic Casing', 6.00, 'PC-300', 'PLS-CASE-003', 200, '2023-09-29'),
('INV-023', 'Plastic Casing', 6.50, 'PC-300', 'PLS-CASE-003', 300, '2023-09-30'),
('INV-024', 'Plastic Casing', 7.00, 'PC-300', 'PLS-CASE-003', 200, '2023-10-01'),

-- Speaker Cones (Total: 600 units in Inventory)
('INV-025', 'Speaker Cone', 8.00, 'SC-700', 'SPK-CONE-007', 100, '2023-10-02'),
('INV-026', 'Speaker Cone', 8.50, 'SC-700', 'SPK-CONE-007', 50, '2023-10-03'),
('INV-027', 'Speaker Cone', 9.00, 'SC-700', 'SPK-CONE-007', 50, '2023-10-04'),
('INV-028', 'Speaker Cone', 10.00, 'SC-800', 'SPK-CONE-008', 150, '2023-10-05'),
('INV-029', 'Speaker Cone', 11.50, 'SC-800', 'SPK-CONE-008', 150, '2023-10-06'),
('INV-030', 'Speaker Cone', 12.50, 'SC-800', 'SPK-CONE-008', 100, '2023-10-07'),

-- Micro-USB Cables (Total: 1200 units in Inventory)
('INV-031', 'Micro-USB Cable', 2.50, 'USB-009', 'USB-MIC-009', 300, '2023-10-08'),
('INV-032', 'Micro-USB Cable', 3.00, 'USB-009', 'USB-MIC-009', 200, '2023-10-09'),
('INV-033', 'Micro-USB Cable', 3.50, 'USB-009', 'USB-MIC-009', 200, '2023-10-10'),
('INV-034', 'Micro-USB Cable', 4.00, 'USB-009', 'USB-MIC-009', 250, '2023-10-11'),
('INV-035', 'Micro-USB Cable', 4.50, 'USB-009', 'USB-MIC-009', 250, '2023-10-12'),

-- PCB Boards (Total: 380 units in Inventory)
('INV-036', 'PCB Board', 11.50, 'PCB-11', 'PCB-BRD-011', 80, '2023-10-13'),
('INV-037', 'PCB Board', 12.00, 'PCB-11', 'PCB-BRD-011', 100, '2023-10-14'),
('INV-038', 'PCB Board', 13.00, 'PCB-12', 'PCB-BRD-012', 100, '2023-10-15'),
('INV-039', 'PCB Board', 14.00, 'PCB-12', 'PCB-BRD-012', 100, '2023-10-16'),

-- Lithium Battery Packs (Total: 400 units in Inventory)
('INV-040', 'Lithium Battery Pack', 45.99, 'BATT-10K', 'BATT-PACK-001', 50, '2023-10-17'),
('INV-041', 'Lithium Battery Pack', 46.50, 'BATT-10K', 'BATT-PACK-001', 50, '2023-10-18'),
('INV-042', 'Lithium Battery Pack', 47.00, 'BATT-10K', 'BATT-PACK-001', 100, '2023-10-19'),
('INV-043', 'Lithium Battery Pack', 48.00, 'BATT-10K', 'BATT-PACK-001', 100, '2023-10-20'),
('INV-044', 'Lithium Battery Pack', 48.50, 'BATT-10K', 'BATT-PACK-001', 100, '2023-10-21');

-- Total: 50 records for raw materials

select * from purchasing;


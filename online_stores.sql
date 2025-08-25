-- Create database
CREATE DATABASE IF NOT EXISTS online_store;
USE online_store;

-- Products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT
);

-- Customers table
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT
);

-- Salespeople table
CREATE TABLE salespeople (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    employment_type ENUM('payroll', 'on_call') NOT NULL
);

-- Orders table (now includes salesperson)
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    salesperson_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (salesperson_id) REFERENCES salespeople(id)
);

-- Order items table (for multiple products per order)
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sample data
INSERT INTO products (name, price, description) VALUES
('Laptop', 999.99, 'High-performance laptop'),
('Smartphone', 699.99, 'Latest smartphone model'),
('Headphones', 199.99, 'Noise-cancelling headphones');

INSERT INTO customers (name, email, address) VALUES
('John Doe', 'john@example.com', '123 Main St, City'),
('Jane Smith', 'jane@example.com', '456 Oak Ave, Town');

INSERT INTO salespeople (first_name, last_name, employment_type) VALUES
('Alice', 'Johnson', 'payroll'),
('Bob', 'Williams', 'on_call');

-- Sample order with multiple products
INSERT INTO orders (customer_id, salesperson_id, order_date) VALUES
(1, 1, '2024-01-15');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 1),  -- 1 Laptop
(1, 3, 2);  -- 2 Headphones
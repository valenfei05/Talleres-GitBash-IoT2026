CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

INSERT INTO products (name, price) VALUES 
('Laptop', 3500000),
('Mouse', 150000),
('Teclado', 250000),
('Monitor', 1200000),
('Audífonos', 300000);
CREATE SCHEMA oltp;

CREATE TABLE oltp.customers (
    customer_id SERIAL PRIMARY KEY,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP
);

CREATE TABLE oltp.products (
    product_id SERIAL PRIMARY KEY,
    product_type TEXT,
    name TEXT,
    price NUMERIC
);

CREATE TABLE oltp.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES oltp.customers(customer_id),
    order_date TIMESTAMP
);

CREATE TABLE oltp.order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES oltp.orders(order_id),
    product_id INT REFERENCES oltp.products(product_id),
    quantity INT
);
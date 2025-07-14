CREATE TYPE customer_status AS ENUM ('ACTIVE', 'INACTIVE', 'PENDING', 'SUSPENDED');

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    status customer_status NOT NULL DEFAULT 'ACTIVE'
);

CREATE INDEX idx_customers_country ON customers(country);
CREATE INDEX idx_customers_status ON customers(status);

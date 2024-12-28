CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    gender VARCHAR(15) NOT NULL,
    dob DATE NOT NULL,
    current_address VARCHAR(255) NOT NULL,
    current_city VARCHAR(50) NOT NULL,
    current_state VARCHAR(50) NOT NULL,
    current_pincode VARCHAR(6) NOT NULL,
    is_permanent_same_as_current BOOLEAN DEFAULT FALSE,
    permanent_address VARCHAR(255) NOT NULL,
    permanent_city VARCHAR(50) NOT NULL,
    permanent_state VARCHAR(50) NOT NULL,
    permanent_pincode VARCHAR(6) NOT NULL,
    password VARCHAR(255) NOT NULL,
    primary_account_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(id) NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    balance NUMERIC(15, 2) DEFAULT 0.0,
    currency VARCHAR(3) DEFAULT 'INR',
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(id) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    document_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

ALTER TABLE customers ADD CONSTRAINT fk_primary_account FOREIGN KEY (primary_account_id) REFERENCES accounts(id);


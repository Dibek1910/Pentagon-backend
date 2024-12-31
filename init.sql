-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id BIGINT PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    middle_name VARCHAR,
    last_name VARCHAR NOT NULL,
    phone_number VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    gender VARCHAR NOT NULL,
    dob DATE NOT NULL,
    current_address VARCHAR NOT NULL,
    current_city VARCHAR NOT NULL,
    current_state VARCHAR NOT NULL,
    current_pincode VARCHAR NOT NULL,
    is_permanent_same_as_current BOOLEAN DEFAULT FALSE,
    permanent_address VARCHAR NOT NULL,
    permanent_city VARCHAR NOT NULL,
    permanent_state VARCHAR NOT NULL,
    permanent_pincode VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    primary_account_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    account_type VARCHAR NOT NULL,
    balance FLOAT DEFAULT 0.0,
    currency VARCHAR DEFAULT 'INR',
    status VARCHAR DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Add foreign key constraint for primary_account_id in customers table
ALTER TABLE customers
ADD CONSTRAINT fk_primary_account
FOREIGN KEY (primary_account_id) REFERENCES accounts(id);

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    document_type VARCHAR NOT NULL,
    document_path VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

ALTER TABLE accounts ALTER COLUMN id SET DEFAULT nextval('accounts_id_seq');


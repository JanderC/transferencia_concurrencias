DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(id),
    recipient_id INT REFERENCES accounts(id),
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO accounts (name, balance) VALUES 
    ('Cuenta Principal', 10000.00),
    ('Cuenta Ahorros', 5000.00),
    ('Cuenta Inversiones', 15000.00);

INSERT INTO transactions (account_id, recipient_id, amount, transaction_type) VALUES
    (1, 2, 500.00, 'transfer'),
    (2, 1, 200.00, 'transfer'),
    (3, NULL, 1000.00, 'withdrawal');
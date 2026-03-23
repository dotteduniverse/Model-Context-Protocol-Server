import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            tenant_id TEXT NOT NULL REFERENCES tenants(id),
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            tenant_id TEXT NOT NULL REFERENCES tenants(id),
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            customer_name TEXT,
            total DECIMAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tenant_id TEXT,
            endpoint TEXT,
            user_id TEXT
        )
    """)

    # Enable RLS on tenant‑specific tables
    cur.execute("ALTER TABLE customers ENABLE ROW LEVEL SECURITY")
    cur.execute("ALTER TABLE orders ENABLE ROW LEVEL SECURITY")

    # Create policies
    cur.execute("""
        DROP POLICY IF EXISTS customer_tenant_policy ON customers;
        CREATE POLICY customer_tenant_policy ON customers
            USING (tenant_id = current_setting('app.current_tenant', true)::TEXT);
    """)
    cur.execute("""
        DROP POLICY IF EXISTS order_tenant_policy ON orders;
        CREATE POLICY order_tenant_policy ON orders
            USING (tenant_id = current_setting('app.current_tenant', true)::TEXT);
    """)

    # Insert sample tenants
    cur.execute("INSERT INTO tenants (id, name) VALUES ('tenant_a', 'Tenant A') ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO tenants (id, name) VALUES ('tenant_b', 'Tenant B') ON CONFLICT DO NOTHING")

    # Insert sample customers and orders for tenant_a
    cur.execute("""
        INSERT INTO customers (tenant_id, name, email) VALUES
        ('tenant_a', 'Alice', 'alice@example.com'),
        ('tenant_a', 'Bob', 'bob@example.com')
        ON CONFLICT DO NOTHING
    """)
    cur.execute("""
        INSERT INTO orders (tenant_id, customer_id, customer_name, total) VALUES
        ('tenant_a', (SELECT id FROM customers WHERE tenant_id='tenant_a' AND name='Alice'), 'Alice', 1200.0),
        ('tenant_a', (SELECT id FROM customers WHERE tenant_id='tenant_a' AND name='Bob'), 'Bob', 850.0)
        ON CONFLICT DO NOTHING
    """)

    # Sample for tenant_b
    cur.execute("""
        INSERT INTO customers (tenant_id, name, email) VALUES
        ('tenant_b', 'Charlie', 'charlie@example.com'),
        ('tenant_b', 'Diana', 'diana@example.com')
        ON CONFLICT DO NOTHING
    """)
    cur.execute("""
        INSERT INTO orders (tenant_id, customer_id, customer_name, total) VALUES
        ('tenant_b', (SELECT id FROM customers WHERE tenant_id='tenant_b' AND name='Charlie'), 'Charlie', 2300.0),
        ('tenant_b', (SELECT id FROM customers WHERE tenant_id='tenant_b' AND name='Diana'), 'Diana', 1750.0)
        ON CONFLICT DO NOTHING
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
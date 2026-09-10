import sqlite3
from pathlib import Path

database = Path(
    r"D:\CODE_WORD\Py_Data_Visualization\data\raw\sqlite\ecommerce.sqlite"
)

with sqlite3.connect(database) as connection:
    # --- orders ---
    connection.execute("""
        CREATE TABLE orders_fixed (
            order_id TEXT,
            customer_id TEXT,
            ordered_at TEXT,
            order_status TEXT,
            currency TEXT,
            subtotal REAL,
            tax_amount REAL,
            shipping_amount REAL,
            order_total REAL
        )
    """)
    connection.execute("""
        INSERT INTO orders_fixed
        SELECT field1, field2, field3, field4, field5, field6, field7, field8, field9
        FROM orders
        WHERE field1 != 'order_id'
    """)
    connection.execute("DROP TABLE orders")
    connection.execute("ALTER TABLE orders_fixed RENAME TO orders")

    # --- payments ---
    connection.execute("""
        CREATE TABLE payments_fixed (
            payment_id TEXT,
            order_id TEXT,
            paid_at TEXT,
            payment_method TEXT,
            payment_status TEXT,
            amount REAL
        )
    """)
    connection.execute("""
        INSERT INTO payments_fixed
        SELECT field1, field2, field3, field4, field5, field6
        FROM payments
        WHERE field1 != 'payment_id'
    """)
    connection.execute("DROP TABLE payments")
    connection.execute("ALTER TABLE payments_fixed RENAME TO payments")

    # --- refunds ---
    connection.execute("""
        CREATE TABLE refunds_fixed (
            refund_id TEXT,
            payment_id TEXT,
            order_id TEXT,
            refunded_at TEXT,
            refund_reason TEXT,
            amount REAL
        )
    """)
    connection.execute("""
        INSERT INTO refunds_fixed
        SELECT field1, field2, field3, field4, field5, field6
        FROM refunds
        WHERE field1 != 'refund_id'
    """)
    connection.execute("DROP TABLE refunds")
    connection.execute("ALTER TABLE refunds_fixed RENAME TO refunds")

    connection.commit()

print("Done fixing orders, payments, refunds")
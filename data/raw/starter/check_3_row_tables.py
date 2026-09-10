import sqlite3
from pathlib import Path

database = Path(
    r"D:\CODE_WORD\Py_Data_Visualization\data\raw\sqlite\ecommerce.sqlite"
)

with sqlite3.connect(database) as connection:
    for table in ["orders", "payments", "refunds"]:
        print(f"\n--- {table} ---")
        rows = connection.execute(f"SELECT * FROM {table} LIMIT 3").fetchall()
        for row in rows:
            print(row)
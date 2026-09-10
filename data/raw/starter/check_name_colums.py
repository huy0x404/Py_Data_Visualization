import sqlite3
from pathlib import Path

database = Path(
    r"D:\CODE_WORD\Py_Data_Visualization\data\raw\sqlite\ecommerce.sqlite"
)

with sqlite3.connect(database) as connection:
    for table in ["orders", "payments", "refunds"]:
        cols = connection.execute(f"PRAGMA table_info({table})").fetchall()
        print(f"\n--- {table} ---")
        for c in cols:
            print(c[1])  # tên cột
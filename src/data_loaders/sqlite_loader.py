"""
SQLite implementation of BaseDataLoader.
Demonstrates context management, database queries, and exception handling (Chapters 2 & 3).
"""

from pathlib import Path
from typing import Dict
import sqlite3
import pandas as pd
import logging

from .base_loader import BaseDataLoader
from ..core.exceptions import DatabaseConnectionError

logger = logging.getLogger("SQLiteDataLoader")


class SQLiteDataLoader(BaseDataLoader):
    """Loads relational tables directly from a SQLite database file."""

    def __init__(self, db_path: Path):
        super().__init__(db_path)
        if not self._source_path.exists():
            raise DatabaseConnectionError(str(self._source_path), "Database file does not exist.")

    def load(self) -> Dict[str, pd.DataFrame]:
        """
        Connects to SQLite database using context management,
        reads each table using pandas.read_sql_query, and parses dates.
        """
        logger.info(f"Connecting to SQLite database: {self._source_path}")
        loaded: Dict[str, pd.DataFrame] = {}

        date_cols_map = {
            "customers": ["created_at"],
            "orders": ["ordered_at"],
            "payments": ["paid_at"],
            "refunds": ["refunded_at"],
        }

        try:
            with sqlite3.connect(self._source_path) as conn:
                # Query table names in SQLite master catalog
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                existing_tables = {row[0] for row in cursor.fetchall()}

                for table in self.EXPECTED_TABLES:
                    if table not in existing_tables:
                        logger.warning(f"Table '{table}' does not exist in SQLite database.")
                        continue

                    parse_dates = date_cols_map.get(table, None)
                    query = f"SELECT * FROM {table}"
                    df = pd.read_sql_query(query, conn, parse_dates=parse_dates)
                    loaded[table] = df
                    logger.info(f"Loaded '{table}' from SQLite: {len(df):,} rows.")

        except sqlite3.Error as e:
            raise DatabaseConnectionError(str(self._source_path), str(e)) from e

        self._data = loaded
        self._is_loaded = True
        self.validate()
        return self._data

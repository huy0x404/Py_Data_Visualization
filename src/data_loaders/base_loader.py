"""
Abstract Base Class for Data Loaders.
Demonstrates Abstraction (ABC), Polymorphism, and Contract-based design (Chapter 3).
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
import logging

from ..core.exceptions import DataValidationError, DataLoadError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("BaseDataLoader")


class BaseDataLoader(ABC):
    """
    Abstract interface for all data loading strategies (CSV, SQLite, API, Parquet).
    Defines the contract and common validation routines across subclasses.
    """

    EXPECTED_TABLES: List[str] = [
        "customers",
        "orders",
        "order_items",
        "products",
        "payments",
        "refunds",
    ]

    REQUIRED_COLUMNS: Dict[str, List[str]] = {
        "customers": ["customer_id", "created_at", "country_code", "acquisition_channel", "customer_segment"],
        "orders": ["order_id", "customer_id", "ordered_at", "order_status", "subtotal", "order_total"],
        "order_items": ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "line_total"],
        "products": ["product_id", "sku", "product_name", "category", "unit_cost", "list_price"],
        "payments": ["payment_id", "order_id", "paid_at", "payment_method", "payment_status", "amount"],
        "refunds": ["refund_id", "payment_id", "order_id", "refunded_at", "refund_reason", "amount"],
    }

    def __init__(self, source_path: Path):
        self._source_path = Path(source_path)
        self._data: Dict[str, pd.DataFrame] = {}
        self._is_loaded: bool = False

    @property
    def source_path(self) -> Path:
        """Encapsulated getter for the source path."""
        return self._source_path

    @property
    def is_loaded(self) -> bool:
        """Check whether data has been successfully ingested."""
        return self._is_loaded

    @abstractmethod
    def load(self) -> Dict[str, pd.DataFrame]:
        """
        Abstract method to load raw data into a dictionary of DataFrames.
        Subclasses MUST implement this method.
        """
        pass

    def validate(self) -> bool:
        """
        Validates loaded DataFrames against expected tables and critical schema columns.
        Raises DataValidationError if critical schema requirements are not met.
        """
        if not self._data:
            raise DataLoadError(str(self._source_path), "No tables found in data container.")

        for table, required_cols in self.REQUIRED_COLUMNS.items():
            if table not in self._data:
                logger.warning(f"Optional or missing table: {table}")
                continue
            df = self._data[table]
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                raise DataValidationError(table, missing)

        logger.info("Data validation succeeded for all loaded tables.")
        return True

    def get_table(self, table_name: str) -> pd.DataFrame:
        """Safe getter for individual tables."""
        if not self._is_loaded:
            self.load()
        if table_name not in self._data:
            raise KeyError(f"Table '{table_name}' is not loaded. Available: {list(self._data.keys())}")
        return self._data[table_name]

    def summary(self) -> Dict[str, Dict[str, int]]:
        """Returns row and column counts for each loaded table."""
        if not self._is_loaded:
            self.load()
        return {
            table: {"rows": len(df), "columns": len(df.columns)}
            for table, df in self._data.items()
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(source='{self._source_path}', loaded={self._is_loaded})>"

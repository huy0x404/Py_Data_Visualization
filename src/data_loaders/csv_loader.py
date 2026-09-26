"""
CSV implementation of BaseDataLoader.
Loads tables from normalized CSV files located in a target directory.
"""

from pathlib import Path
from typing import Dict, Optional
import pandas as pd
import logging

from .base_loader import BaseDataLoader
from ..core.exceptions import DataLoadError

logger = logging.getLogger("CSVDataLoader")


class CSVDataLoader(BaseDataLoader):
    """Loads relational ecommerce tables from a folder containing CSV files."""

    def __init__(self, csv_dir: Path):
        super().__init__(csv_dir)
        if not self._source_path.exists() or not self._source_path.is_dir():
            raise DataLoadError(str(self._source_path), "Directory does not exist or is not a directory.")

    def load(self) -> Dict[str, pd.DataFrame]:
        """
        Loads CSV files corresponding to the expected ecommerce tables.
        Applies robust type inference and parses standard date columns.
        """
        logger.info(f"Loading CSV tables from: {self._source_path}")
        loaded: Dict[str, pd.DataFrame] = {}

        date_cols_map = {
            "customers": ["created_at"],
            "orders": ["ordered_at"],
            "payments": ["paid_at"],
            "refunds": ["refunded_at"],
        }

        for table in self.EXPECTED_TABLES:
            file_path = self._source_path / f"{table}.csv"
            if not file_path.exists():
                logger.warning(f"File {file_path.name} not found in {self._source_path}.")
                continue

            try:
                parse_dates = date_cols_map.get(table, None)
                df = pd.read_csv(file_path, parse_dates=parse_dates)
                loaded[table] = df
                logger.info(f"Loaded '{table}': {len(df):,} rows, {len(df.columns)} columns.")
            except Exception as e:
                raise DataLoadError(str(file_path), str(e)) from e

        self._data = loaded
        self._is_loaded = True
        self.validate()
        return self._data

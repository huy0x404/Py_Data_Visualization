"""
Data Cleaner module.
Demonstrates:
- Handling missing data (dropna, fillna, isna) (Chapter 6.5)
- Data type conversion and date parsing
- String manipulation and sanitization (Chapter 6.5)
- Defensive programming with custom exceptions
"""

from typing import Dict
import pandas as pd
import numpy as np
import logging

from ..core.exceptions import ProcessingError

logger = logging.getLogger("DataCleaner")


class DataCleaner:
    """Cleans and standardizes raw relational ecommerce dataframes."""

    def __init__(self, raw_tables: Dict[str, pd.DataFrame]):
        self._raw = raw_tables
        self._cleaned: Dict[str, pd.DataFrame] = {}

    def clean_all(self) -> Dict[str, pd.DataFrame]:
        """Runs cleaning pipeline on all registered tables."""
        logger.info("Initiating full dataset cleaning...")
        try:
            self._cleaned["customers"] = self.clean_customers(self._raw["customers"])
            self._cleaned["products"] = self.clean_products(self._raw["products"])
            self._cleaned["orders"] = self.clean_orders(self._raw["orders"])
            self._cleaned["order_items"] = self.clean_order_items(self._raw["order_items"])
            self._cleaned["payments"] = self.clean_payments(self._raw["payments"])
            self._cleaned["refunds"] = self.clean_refunds(self._raw["refunds"])
            logger.info("All tables successfully cleaned and standardized.")
            return self._cleaned
        except Exception as e:
            raise ProcessingError(step="clean_all", reason=str(e)) from e

    def clean_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans customers dataframe."""
        df = df.copy()
        df["customer_id"] = df["customer_id"].astype(str).str.strip()
        df["country_code"] = df["country_code"].astype(str).str.strip().str.upper()
        df["acquisition_channel"] = df["acquisition_channel"].astype(str).str.strip().str.lower()
        df["customer_segment"] = df["customer_segment"].astype(str).str.strip().str.lower()
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df.dropna(subset=["customer_id", "created_at"], inplace=True)
        return df

    def clean_products(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans products dataframe."""
        df = df.copy()
        df["product_id"] = df["product_id"].astype(str).str.strip()
        df["sku"] = df["sku"].astype(str).str.strip()
        df["product_name"] = df["product_name"].astype(str).str.strip()
        df["category"] = df["category"].astype(str).str.strip()
        df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0.0)
        df["list_price"] = pd.to_numeric(df["list_price"], errors="coerce").fillna(0.0)
        df["profit_margin"] = df["list_price"] - df["unit_cost"]
        df["markup_pct"] = np.where(df["unit_cost"] > 0, (df["profit_margin"] / df["unit_cost"]) * 100, 0.0)
        return df

    def clean_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans orders dataframe."""
        df = df.copy()
        df["order_id"] = df["order_id"].astype(str).str.strip()
        df["customer_id"] = df["customer_id"].astype(str).str.strip()
        df["ordered_at"] = pd.to_datetime(df["ordered_at"], errors="coerce")
        df["order_status"] = df["order_status"].astype(str).str.strip().str.lower()
        df["currency"] = df["currency"].astype(str).str.strip().str.upper()

        numeric_cols = ["subtotal", "tax_amount", "shipping_amount", "order_total"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        df.dropna(subset=["order_id", "customer_id", "ordered_at"], inplace=True)
        return df

    def clean_order_items(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans order_items dataframe."""
        df = df.copy()
        df["order_item_id"] = df["order_item_id"].astype(str).str.strip()
        df["order_id"] = df["order_id"].astype(str).str.strip()
        df["product_id"] = df["product_id"].astype(str).str.strip()
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0)
        df["discount_amount"] = pd.to_numeric(df["discount_amount"], errors="coerce").fillna(0.0)
        df["line_total"] = pd.to_numeric(df["line_total"], errors="coerce").fillna(0.0)
        return df

    def clean_payments(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans payments dataframe."""
        df = df.copy()
        df["payment_id"] = df["payment_id"].astype(str).str.strip()
        df["order_id"] = df["order_id"].astype(str).str.strip()
        df["paid_at"] = pd.to_datetime(df["paid_at"], errors="coerce")
        df["payment_method"] = df["payment_method"].astype(str).str.strip().str.lower()
        df["payment_status"] = df["payment_status"].astype(str).str.strip().str.lower()
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        return df

    def clean_refunds(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans refunds dataframe."""
        df = df.copy()
        df["refund_id"] = df["refund_id"].astype(str).str.strip()
        df["payment_id"] = df["payment_id"].astype(str).str.strip()
        df["order_id"] = df["order_id"].astype(str).str.strip()
        df["refunded_at"] = pd.to_datetime(df["refunded_at"], errors="coerce")
        df["refund_reason"] = df["refund_reason"].astype(str).str.strip().str.lower()
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        return df

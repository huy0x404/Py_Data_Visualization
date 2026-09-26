"""
Data Merger module.
Demonstrates relational joins, denormalization, grouping and aggregations with Pandas (Chapter 6).
"""

from typing import Dict
import pandas as pd
import numpy as np
import logging

from ..core.exceptions import ProcessingError

logger = logging.getLogger("DataMerger")


class DataMerger:
    """Nối ghép và tổng hợp các bảng quan hệ ecommerce."""

    def __init__(self, cleaned_tables: Dict[str, pd.DataFrame]):
        self._tables = cleaned_tables

    def build_master_orders(self) -> pd.DataFrame:
        """
        Xây dựng bảng master_orders:
        Kết hợp: orders + customers + payments_aggregated + refunds_aggregated.
        Tính toán: paid_amount, refunded_amount, net_sales, year, month, quarter, day_of_week.
        """
        logger.info("Building denormalized master_orders DataFrame...")
        try:
            orders = self._tables["orders"].copy()
            customers = self._tables["customers"].copy()
            payments = self._tables["payments"].copy()
            refunds = self._tables["refunds"].copy()

            # 1. Tổng hợp payments thành công theo từng đơn hàng
            succeeded_payments = payments[payments["payment_status"] == "succeeded"]
            paid_summary = (
                succeeded_payments.groupby("order_id")
                .agg(
                    paid_amount=("amount", "sum"),
                    payment_count=("payment_id", "count"),
                    primary_payment_method=("payment_method", lambda x: x.iloc[0] if len(x) > 0 else "unknown"),
                    last_paid_at=("paid_at", "max"),
                )
                .reset_index()
            )

            # 2. Tổng hợp refunds theo từng đơn hàng
            refund_summary = (
                refunds.groupby("order_id")
                .agg(
                    refunded_amount=("amount", "sum"),
                    refund_count=("refund_id", "count"),
                    primary_refund_reason=("refund_reason", lambda x: x.iloc[0] if len(x) > 0 else "none"),
                    last_refunded_at=("refunded_at", "max"),
                )
                .reset_index()
            )

            # 3. Merge orders với customers (Many-to-one)
            master = orders.merge(
                customers,
                on="customer_id",
                how="left",
                suffixes=("", "_customer"),
            )

            # 4. Merge với payment summary và refund summary (Left joins)
            master = master.merge(paid_summary, on="order_id", how="left")
            master = master.merge(refund_summary, on="order_id", how="left")

            # 5. Điền giá trị missing hợp lý
            master["paid_amount"] = master["paid_amount"].fillna(0.0)
            master["payment_count"] = master["payment_count"].fillna(0).astype(int)
            master["primary_payment_method"] = master["primary_payment_method"].fillna("unpaid")

            master["refunded_amount"] = master["refunded_amount"].fillna(0.0)
            master["refund_count"] = master["refund_count"].fillna(0).astype(int)
            master["primary_refund_reason"] = master["primary_refund_reason"].fillna("none")

            # 6. Tính toán Net Sales
            # Net Sales = tiền thực trả thành công trừ đi tiền đã hoàn
            master["net_sales"] = (master["paid_amount"] - master["refunded_amount"]).round(2)
            master["is_refunded"] = master["refunded_amount"] > 0

            # 7. Trích xuất đặc trưng chuỗi thời gian (Pandas datetime features)
            dt_series = master["ordered_at"].dt.tz_localize(None) if master["ordered_at"].dt.tz is not None else master["ordered_at"]
            master["order_year"] = master["ordered_at"].dt.year
            master["order_month"] = dt_series.dt.to_period("M").astype(str)
            master["order_quarter"] = dt_series.dt.to_period("Q").astype(str)
            master["order_day_name"] = master["ordered_at"].dt.day_name()
            master["order_hour"] = master["ordered_at"].dt.hour

            logger.info(f"master_orders built: {len(master):,} rows, {len(master.columns)} columns.")
            return master

        except Exception as e:
            raise ProcessingError(step="build_master_orders", reason=str(e)) from e

    def build_master_order_items(self, master_orders: pd.DataFrame) -> pd.DataFrame:
        """
        Xây dựng bảng master_order_items:
        Kết hợp: order_items + products + master_orders (lấy customer_id, ordered_at, category, profit).
        """
        logger.info("Building denormalized master_order_items DataFrame...")
        try:
            items = self._tables["order_items"].copy()
            products = self._tables["products"].copy()

            # Merge items with products
            items_merged = items.merge(products, on="product_id", how="left")

            # Calculate cost and profit per line
            items_merged["total_cost"] = (items_merged["quantity"] * items_merged["unit_cost"]).round(2)
            items_merged["line_profit"] = (items_merged["line_total"] - items_merged["total_cost"]).round(2)
            items_merged["line_margin_pct"] = np.where(
                items_merged["line_total"] > 0,
                (items_merged["line_profit"] / items_merged["line_total"]) * 100.0,
                0.0,
            ).round(2)

            # Merge context columns from master_orders
            orders_subset = master_orders[
                [
                    "order_id",
                    "customer_id",
                    "ordered_at",
                    "order_status",
                    "customer_segment",
                    "country_code",
                    "acquisition_channel",
                    "order_month",
                    "order_year",
                ]
            ]
            full_items = items_merged.merge(orders_subset, on="order_id", how="left")

            logger.info(f"master_order_items built: {len(full_items):,} rows, {len(full_items.columns)} columns.")
            return full_items

        except Exception as e:
            raise ProcessingError(step="build_master_order_items", reason=str(e)) from e

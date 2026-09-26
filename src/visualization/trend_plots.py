"""
Trend & Time-Series Visualizer module.
Covers:
- Đồ thị đường (Line plot) (Chapter 7.3)
- Đồ thị đa đường (Multi-line plot) (Chapter 7.3)
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from .base_visualizer import BaseVisualizer

logger = logging.getLogger("TrendVisualizer")


class TrendVisualizer(BaseVisualizer):
    """Trực quan hóa xu hướng tài chính và tăng trưởng theo thời gian."""

    def plot_financial_performance_trends(
        self,
        monthly_df: pd.DataFrame,
        filename: str = "01_financial_performance_trends.png",
    ) -> Path:
        """
        Đồ thị đa đường (Multi-line plot) thể hiện:
        Gross Sales, Net Sales, Refunds và đường trung bình động 3 tháng (3-Month Rolling Average).
        """
        fig, ax = self.create_figure(figsize=(14, 7))

        x_vals = monthly_df["order_month"].astype(str)

        # Đường Doanh thu gộp (Gross Sales)
        ax.plot(
            x_vals,
            monthly_df["gross_sales"],
            label="Gross Sales ($)",
            color="#2b5c8f",
            linewidth=2.2,
            marker="o",
            markersize=5,
        )

        # Đường Doanh thu thuần (Net Sales)
        ax.plot(
            x_vals,
            monthly_df["net_sales"],
            label="Net Sales ($)",
            color="#2ca02c",
            linewidth=2.5,
            marker="s",
            markersize=5,
        )

        # Đường Hoàn tiền (Refunds)
        ax.plot(
            x_vals,
            monthly_df["refund_amount"],
            label="Refunds ($)",
            color="#d62728",
            linewidth=1.8,
            linestyle="--",
            marker="^",
            markersize=4,
        )

        # Đường Rolling Average 3 tháng
        ax.plot(
            x_vals,
            monthly_df["net_sales_roll3"],
            label="Net Sales (3-M Moving Avg)",
            color="#ff7f0e",
            linewidth=2.0,
            linestyle=":",
        )

        ax.set_title("Ecommerce Monthly Revenue Trends (2023 - 2025)", fontweight="bold", pad=15)
        ax.set_xlabel("Order Month", fontweight="bold", labelpad=10)
        ax.set_ylabel("Revenue in USD ($)", fontweight="bold", labelpad=10)
        self.format_currency_axis(ax, "y")

        # Xoay nhãn tháng để dễ đọc
        ax.tick_params(axis="x", rotation=45)
        ax.legend(frameon=True, facecolor="white", framealpha=0.9, loc="upper left")
        ax.grid(True, linestyle="--", alpha=0.6)

        return self.save_figure(fig, filename)

    def plot_segment_growth_multiline(
        self,
        master_orders: pd.DataFrame,
        filename: str = "02_segment_revenue_growth_multiline.png",
    ) -> Path:
        """
        Đồ thị đa đường (Multi-line plot) so sánh xu hướng doanh thu hàng tháng giữa các phân khúc:
        Consumer, Small Business, Enterprise.
        """
        fig, ax = self.create_figure(figsize=(14, 7))

        # Gom nhóm doanh thu theo Tháng và Phân khúc
        segment_monthly = (
            master_orders.groupby(["order_month", "customer_segment"])["net_sales"]
            .sum()
            .reset_index()
        )

        # Sử dụng Seaborn lineplot
        palette = {"consumer": "#1f77b4", "small_business": "#ff7f0e", "enterprise": "#2ca02c"}
        sns.lineplot(
            data=segment_monthly,
            x="order_month",
            y="net_sales",
            hue="customer_segment",
            palette=palette,
            marker="o",
            linewidth=2.5,
            ax=ax,
        )

        ax.set_title("Monthly Net Sales Trajectory by Customer Segment", fontweight="bold", pad=15)
        ax.set_xlabel("Order Month", fontweight="bold", labelpad=10)
        ax.set_ylabel("Net Sales in USD ($)", fontweight="bold", labelpad=10)
        self.format_currency_axis(ax, "y")
        ax.tick_params(axis="x", rotation=45)

        # Định dạng legend đẹp mắt
        ax.legend(
            title="Customer Segment",
            title_fontsize=11,
            frameon=True,
            facecolor="white",
            framealpha=0.9,
            labels=["Consumer", "Small Business", "Enterprise"],
        )
        ax.grid(True, linestyle="--", alpha=0.6)

        return self.save_figure(fig, filename)

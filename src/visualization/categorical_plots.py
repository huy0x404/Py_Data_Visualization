"""
Categorical & Composition Visualizer module.
Covers:
- Biểu đồ tròn & Donut (Pie chart / Donut chart) (Chapter 7.3)
- Biểu đồ cột / thanh (Bar chart) (Chapter 7.3)
- Catplot (Chapter 7.4)
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from .base_visualizer import BaseVisualizer

logger = logging.getLogger("CategoricalVisualizer")


class CategoricalVisualizer(BaseVisualizer):
    """Trực quan hóa cơ cấu tỉ trọng và so sánh danh mục sản phẩm / khách hàng."""

    def plot_acquisition_channel_donut(
        self,
        customers_df: pd.DataFrame,
        filename: str = "06_acquisition_channel_donut.png",
    ) -> Path:
        """
        Biểu đồ Donut (Donut / Pie Chart) thể hiện thị phần của các kênh tiếp cận khách hàng.
        (Chapter 7.3 Biểu đồ tròn)
        """
        fig, ax = self.create_figure(figsize=(9, 9))

        channel_counts = customers_df["acquisition_channel"].value_counts()
        colors = ["#2b5c8f", "#4682b4", "#5dade2", "#85c1e9", "#aed6f1"][: len(channel_counts)]

        wedges, texts, autotexts = ax.pie(
            channel_counts,
            labels=channel_counts.index.str.replace("_", " ").str.title(),
            autopct="%1.1f%%",
            startangle=140,
            pctdistance=0.78,
            colors=colors,
            wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        )

        plt.setp(autotexts, size=11, weight="bold", color="white")
        plt.setp(texts, size=11)

        # Thêm vòng tròn giữa tạo hiệu ứng Donut Chart
        centre_circle = plt.Circle((0, 0), 0.55, fc="white")
        ax.add_artist(centre_circle)

        # Chèn tổng số khách hàng ở giữa tâm
        total_customers = len(customers_df)
        ax.text(
            0,
            0,
            f"Total\n{total_customers:,}\nUsers",
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
            color="#2c3e50",
        )

        ax.set_title("Customer Acquisition Channel Share", fontweight="bold", pad=20)
        return self.save_figure(fig, filename)

    def plot_top_products_bar(
        self,
        master_items: pd.DataFrame,
        top_n: int = 10,
        filename: str = "07_top_products_revenue_bar.png",
    ) -> Path:
        """
        Biểu đồ thanh ngang (Horizontal Bar Chart) xếp hạng Top 10 sản phẩm bán chạy nhất theo doanh thu và lợi nhuận.
        (Chapter 7.3 Biểu đồ thanh)
        """
        fig, ax = self.create_figure(figsize=(13, 8))

        top_products = (
            master_items.groupby("product_name")
            .agg(
                total_revenue=("line_total", "sum"),
                total_profit=("line_profit", "sum"),
                total_units=("quantity", "sum"),
            )
            .sort_values("total_revenue", ascending=False)
            .head(top_n)
            .reset_index()
        )

        # Vẽ thanh doanh thu
        bars = ax.barh(
            top_products["product_name"],
            top_products["total_revenue"],
            color="#3498db",
            edgecolor="#2980b9",
            height=0.6,
        )

        ax.invert_yaxis()  # Sản phẩm cao nhất ở trên cùng
        ax.set_title(f"Top {top_n} Best-Selling Products by Revenue & Profit", fontweight="bold", pad=15)
        ax.set_xlabel("Gross Revenue in USD ($)", fontweight="bold", labelpad=10)
        self.format_currency_axis(ax, "x")

        # Thêm nhãn giá trị doanh thu và lợi nhuận trên mỗi thanh
        for bar, profit in zip(bars, top_products["total_profit"]):
            width = bar.get_width()
            ax.text(
                width + (top_products["total_revenue"].max() * 0.01),
                bar.get_y() + bar.get_height() / 2,
                f"${width:,.0f} (Profit: ${profit:,.0f})",
                va="center",
                ha="left",
                fontsize=9.5,
                color="#2c3e50",
                fontweight="bold",
            )

        ax.set_xlim(0, top_products["total_revenue"].max() * 1.25)
        ax.grid(True, axis="x", linestyle="--", alpha=0.6)

        return self.save_figure(fig, filename)

    def plot_customer_segment_catplot(
        self,
        master_orders: pd.DataFrame,
        filename: str = "08_customer_segment_catplot.png",
    ) -> Path:
        """
        Seaborn Catplot thể hiện mức chi tiêu trung bình (Mean Order Total)
        theo Customer Segment và Payment Method. (Chapter 7.4 Catplot)
        """
        valid_orders = master_orders[master_orders["primary_payment_method"].isin(["card", "paypal", "bank_transfer"])]

        g = sns.catplot(
            data=valid_orders,
            x="customer_segment",
            y="order_total",
            hue="primary_payment_method",
            kind="bar",
            height=6,
            aspect=1.8,
            palette="Blues",
            edgecolor="gray",
            legend=True,
        )

        g.figure.subplots_adjust(top=0.88)
        g.figure.suptitle("Average Order Value by Customer Segment & Payment Method", fontweight="bold")
        g.set_axis_labels("Customer Segment", "Average Order Value ($)", fontweight="bold")
        self.format_currency_axis(g.ax, "y")

        return self.save_figure(g.figure, filename)

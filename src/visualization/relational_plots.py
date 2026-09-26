"""
Relational & Complex Multivariate Visualizer module.
Covers:
- Đồ thị phân tán (Scatter plot) (Chapter 7.3)
- FacetGrid (Chapter 7.4)
- Pairplot (Chapter 7.4)
- Heatmap tương quan và Cohort Retention (Chapter 6 & 7)
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from .base_visualizer import BaseVisualizer

logger = logging.getLogger("RelationalVisualizer")


class RelationalVisualizer(BaseVisualizer):
    """Trực quan hóa tương quan đa biến, phân nhóm ma trận và lưới FacetGrid."""

    def plot_cost_vs_price_scatter(
        self,
        products_df: pd.DataFrame,
        filename: str = "09_product_cost_vs_price_scatter.png",
    ) -> Path:
        """
        Đồ thị phân tán (Scatter plot) giữa Unit Cost vs List Price cho 1,200 sản phẩm,
        phân nhóm theo Category, kích thước điểm theo Profit Margin.
        (Chapter 7.3 Đồ thị phân tán)
        """
        fig, ax = self.create_figure(figsize=(13, 8))

        sns.scatterplot(
            data=products_df,
            x="unit_cost",
            y="list_price",
            hue="category",
            size="profit_margin",
            sizes=(30, 200),
            alpha=0.75,
            palette="tab10",
            ax=ax,
        )

        # Vẽ đường hòa vốn 1:1 (List Price = Unit Cost)
        max_limit = max(products_df["unit_cost"].max(), products_df["list_price"].max()) * 1.05
        ax.plot([0, max_limit], [0, max_limit], color="gray", linestyle="--", linewidth=1.5, label="Cost Line (1:1)")

        ax.set_title("Product Pricing Strategy: Unit Cost vs. List Price", fontweight="bold", pad=15)
        ax.set_xlabel("Unit Cost in USD ($)", fontweight="bold", labelpad=10)
        ax.set_ylabel("List Price in USD ($)", fontweight="bold", labelpad=10)
        self.format_currency_axis(ax, "x")
        self.format_currency_axis(ax, "y")

        ax.legend(
            bbox_to_anchor=(1.02, 1),
            loc="upper left",
            borderaxespad=0,
            frameon=True,
            facecolor="white",
        )
        ax.grid(True, linestyle="--", alpha=0.5)

        return self.save_figure(fig, filename)

    def plot_rfm_pairplot(
        self,
        rfm_df: pd.DataFrame,
        sample_size: int = 1200,
        filename: str = "10_rfm_multivariate_pairplot.png",
    ) -> Path:
        """
        Seaborn Pairplot phân tích ma trận tương quan đa chiều giữa Recency, Frequency, Monetary
        được tô màu theo phân khúc RFM Segment. (Chapter 7.4 Pairplot)
        """
        sample_rfm = rfm_df.sample(n=min(len(rfm_df), sample_size), random_state=42)
        target_cols = ["recency", "frequency", "monetary", "rfm_segment"]
        plot_data = sample_rfm[target_cols].copy()

        # Log transform monetary for better visual scaling
        plot_data["monetary"] = np.log10(np.clip(plot_data["monetary"], a_min=1.0, a_max=None))
        plot_data.rename(columns={"monetary": "log10_monetary"}, inplace=True)

        g = sns.pairplot(
            plot_data,
            hue="rfm_segment",
            palette="Set2",
            corner=True,
            diag_kind="kde",
            plot_kws={"alpha": 0.6, "s": 35},
        )
        g.figure.subplots_adjust(top=0.93)
        g.figure.suptitle("Multivariate Pairplot of RFM Metrics Across Customer Segments", fontweight="bold")

        return self.save_figure(g.figure, filename)

    def plot_facetgrid_category_segments(
        self,
        master_items: pd.DataFrame,
        sample_size: int = 15000,
        filename: str = "11_facetgrid_category_segments.png",
    ) -> Path:
        """
        Seaborn FacetGrid phân tích phân bố line_total của các ngành hàng chia theo Customer Segment.
        (Chapter 7.4 FacetGrid)
        """
        sample_items = master_items.sample(n=min(len(master_items), sample_size), random_state=42)
        p98 = sample_items["line_total"].quantile(0.98)
        subset = sample_items[sample_items["line_total"] <= p98]

        g = sns.FacetGrid(
            subset,
            col="customer_segment",
            hue="customer_segment",
            palette="muted",
            height=5,
            aspect=1.2,
            sharey=False,
        )
        g.map_dataframe(sns.histplot, x="line_total", kde=True, bins=30)
        g.set_axis_labels("Line Item Total ($)", "Frequency Count")
        g.set_titles(col_template="Segment: {col_name}", size=12, weight="bold")
        g.figure.subplots_adjust(top=0.82)
        g.figure.suptitle("FacetGrid: Line Item Sales Distribution by Customer Segment", fontweight="bold")

        return self.save_figure(g.figure, filename)

    def plot_cohort_retention_heatmap(
        self,
        retention_matrix: pd.DataFrame,
        filename: str = "12_cohort_retention_heatmap.png",
    ) -> Path:
        """
        Seaborn Heatmap trực quan hóa tỷ lệ giữ chân khách hàng (Cohort Retention Rate %)
        theo thời gian.
        """
        fig, ax = self.create_figure(figsize=(16, 10))

        # Hiển thị tối đa 15 cohort đầu tiên và 12 tháng retention để đồ thị sắc nét
        display_data = retention_matrix.iloc[:18, :13]

        sns.heatmap(
            display_data,
            annot=True,
            fmt=".1f",
            cmap="YlGnBu",
            vmin=0,
            vmax=30,  # chuẩn hóa dải màu để làm nổi bật tỷ lệ tái mua
            cbar_kws={"label": "Retention Rate (%)"},
            linewidths=0.5,
            linecolor="white",
            ax=ax,
        )

        ax.set_title("Customer Monthly Cohort Retention Heatmap (%)", fontweight="bold", pad=15)
        ax.set_xlabel("Cohort Period (Months Since First Purchase)", fontweight="bold", labelpad=10)
        ax.set_ylabel("Cohort Acquisition Month", fontweight="bold", labelpad=10)

        return self.save_figure(fig, filename)

    def plot_financial_correlation_heatmap(
        self,
        orders_df: pd.DataFrame,
        filename: str = "13_financial_correlation_heatmap.png",
    ) -> Path:
        """
        Seaborn Heatmap thể hiện ma trận tương quan tài chính giữa các chỉ số đơn hàng:
        subtotal, tax_amount, shipping_amount, order_total, paid_amount, refunded_amount, net_sales.
        """
        numeric_cols = [
            "subtotal",
            "tax_amount",
            "shipping_amount",
            "order_total",
            "paid_amount",
            "refunded_amount",
            "net_sales",
        ]
        corr_matrix = orders_df[numeric_cols].corr()

        fig, ax = self.create_figure(figsize=(10, 8))

        # Tạo mask cho nửa trên tam giác để biểu đồ gọn gàng
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        sns.heatmap(
            corr_matrix,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap="vlag",
            center=0,
            square=True,
            linewidths=0.8,
            cbar_kws={"shrink": 0.8, "label": "Pearson Correlation"},
            ax=ax,
        )

        ax.set_title("Correlation Heatmap of Ecommerce Financial Metrics", fontweight="bold", pad=15)
        return self.save_figure(fig, filename)

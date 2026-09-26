"""
Distribution & Spread Visualizer module.
Covers:
- Đồ thị hộp (Box plot) (Chapter 7.3)
- Biểu đồ Violin (Violin plot)
- Swarm plot / Strip plot (Chapter 7.4)
- Histogram & KDE distribution (Chapter 7.3)
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from .base_visualizer import BaseVisualizer

logger = logging.getLogger("DistributionVisualizer")


class DistributionVisualizer(BaseVisualizer):
    """Trực quan hóa sự phân bố và phân tán của dữ liệu tài chính."""

    def plot_order_total_distribution(
        self,
        orders_df: pd.DataFrame,
        filename: str = "03_order_total_distribution_hist_box.png",
    ) -> Path:
        """
        Biểu đồ kết hợp: Boxplot ở trên và Histogram + KDE ở dưới để phân tích phân phối order_total.
        """
        # Giới hạn phân vị 99% để biểu đồ không bị kéo dài bởi ngoại lai cực trị
        p99 = orders_df["order_total"].quantile(0.99)
        filtered_orders = orders_df[orders_df["order_total"] <= p99]

        fig, (ax_box, ax_hist) = plt.subplots(
            nrows=2,
            ncols=1,
            figsize=(13, 8),
            sharex=True,
            gridspec_kw={"height_ratios": [0.25, 0.75]},
        )

        # 1. Boxplot (trên)
        sns.boxplot(
            data=filtered_orders,
            x="order_total",
            color="#5dade2",
            ax=ax_box,
            fliersize=3,
        )
        ax_box.set(xlabel="")
        ax_box.set_title("Distribution & Outliers of Order Values (99th Percentile)", fontweight="bold", pad=12)

        # 2. Histogram + KDE (dưới)
        sns.histplot(
            data=filtered_orders,
            x="order_total",
            kde=True,
            color="#2874a6",
            bins=50,
            ax=ax_hist,
            stat="density",
        )
        mean_val = filtered_orders["order_total"].mean()
        median_val = filtered_orders["order_total"].median()

        ax_hist.axvline(mean_val, color="red", linestyle="--", linewidth=1.8, label=f"Mean: ${mean_val:,.1f}")
        ax_hist.axvline(median_val, color="green", linestyle="-", linewidth=1.8, label=f"Median: ${median_val:,.1f}")

        ax_hist.set_xlabel("Order Total in USD ($)", fontweight="bold", labelpad=10)
        ax_hist.set_ylabel("Probability Density", fontweight="bold", labelpad=10)
        self.format_currency_axis(ax_hist, "x")
        ax_hist.legend(frameon=True, facecolor="white", framealpha=0.9)

        return self.save_figure(fig, filename)

    def plot_payment_methods_box_violin(
        self,
        orders_df: pd.DataFrame,
        filename: str = "04_payment_methods_box_violin.png",
    ) -> Path:
        """
        So sánh phân phối giá trị đơn hàng giữa các phương thức thanh toán
        (card, paypal, bank_transfer) thông qua Box plot và Violin plot.
        """
        valid_orders = orders_df[orders_df["primary_payment_method"].isin(["card", "paypal", "bank_transfer"])]
        p98 = valid_orders["order_total"].quantile(0.98)
        subset = valid_orders[valid_orders["order_total"] <= p98]

        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

        # 1. Box plot
        sns.boxplot(
            data=subset,
            x="primary_payment_method",
            y="order_total",
            hue="primary_payment_method",
            legend=False,
            palette="Blues",
            ax=ax1,
        )
        ax1.set_title("Order Value Spread by Payment Method (Boxplot)", fontweight="bold")
        ax1.set_xlabel("Payment Method", fontweight="bold")
        ax1.set_ylabel("Order Total in USD ($)", fontweight="bold")
        self.format_currency_axis(ax1, "y")

        # 2. Violin plot
        sns.violinplot(
            data=subset,
            x="primary_payment_method",
            y="order_total",
            hue="primary_payment_method",
            legend=False,
            palette="PuBuGn",
            ax=ax2,
            inner="quartile",
        )
        ax2.set_title("Kernel Density Shape by Payment Method (Violin Plot)", fontweight="bold")
        ax2.set_xlabel("Payment Method", fontweight="bold")
        ax2.set_ylabel("")
        self.format_currency_axis(ax2, "y")

        return self.save_figure(fig, filename)

    def plot_refund_reason_swarm(
        self,
        refunds_df: pd.DataFrame,
        sample_size: int = 1500,
        filename: str = "05_refund_reasons_swarm_plot.png",
    ) -> Path:
        """
        Đồ thị Swarm plot / Strip plot thể hiện phân bổ các khoản hoàn tiền theo lý do hoàn trả (refund_reason).
        (Chapter 7.4 Swarm plot)
        """
        fig, ax = self.create_figure(figsize=(13, 7))

        # Lấy mẫu ngẫu nhiên có kiểm soát nếu dữ liệu quá lớn để vẽ swarm plot không bị tràn điểm
        sample_df = refunds_df.sample(n=min(len(refunds_df), sample_size), random_state=42)

        sns.stripplot(
            data=sample_df,
            x="refund_reason",
            y="amount",
            hue="refund_reason",
            legend=False,
            jitter=0.25,
            alpha=0.6,
            palette="Set2",
            size=6,
            ax=ax,
        )

        # Vẽ điểm trung bình (pointplot) đè lên
        sns.pointplot(
            data=sample_df,
            x="refund_reason",
            y="amount",
            color="black",
            errorbar=None,
            markers="D",
            linestyles="",
            ax=ax,
        )

        ax.set_title("Refund Amounts Distribution Across Reasons (Strip/Swarm with Mean Points)", fontweight="bold", pad=15)
        ax.set_xlabel("Refund Reason", fontweight="bold", labelpad=10)
        ax.set_ylabel("Refund Amount ($)", fontweight="bold", labelpad=10)
        self.format_currency_axis(ax, "y")
        ax.tick_params(axis="x", rotation=15)

        return self.save_figure(fig, filename)

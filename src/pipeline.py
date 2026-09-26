"""
End-to-End Analytics & Visualization Pipeline.
Orchestrates loading, cleaning, merging, feature engineering, processed data export,
and automated figure generation across all visualization modules.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import logging
import time

from .core.config import settings
from .core.exceptions import EcommerceAnalyticsError
from .data_loaders.base_loader import BaseDataLoader
from .data_loaders.csv_loader import CSVDataLoader
from .data_loaders.sqlite_loader import SQLiteDataLoader
from .processing.cleaner import DataCleaner
from .processing.merger import DataMerger
from .processing.feature_engineering import FeatureEngineer
from .visualization.trend_plots import TrendVisualizer
from .visualization.distribution_plots import DistributionVisualizer
from .visualization.categorical_plots import CategoricalVisualizer
from .visualization.relational_plots import RelationalVisualizer

logger = logging.getLogger("EcommercePipeline")


class EcommercePipeline:
    """Điều phối toàn bộ quy trình phân tích và trực quan hoá dữ liệu thương mại điện tử."""

    def __init__(self, source_type: str = "csv", source_path: Optional[Path] = None):
        self.source_type = source_type.lower()
        if self.source_type == "csv":
            self.source_path = Path(source_path or settings.RAW_DATA_DIR)
            self.loader: BaseDataLoader = CSVDataLoader(self.source_path)
        elif self.source_type == "sqlite":
            self.source_path = Path(source_path or settings.SQLITE_DB_PATH)
            self.loader = SQLiteDataLoader(self.source_path)
        else:
            raise ValueError(f"Unsupported source type '{source_type}'. Choose 'csv' or 'sqlite'.")

        self.trend_viz = TrendVisualizer()
        self.dist_viz = DistributionVisualizer()
        self.cat_viz = CategoricalVisualizer()
        self.rel_viz = RelationalVisualizer()

        # Data placeholders
        self.raw_data: Dict[str, pd.DataFrame] = {}
        self.cleaned_data: Dict[str, pd.DataFrame] = {}
        self.master_orders: Optional[pd.DataFrame] = None
        self.master_items: Optional[pd.DataFrame] = None
        self.rfm_df: Optional[pd.DataFrame] = None
        self.monthly_df: Optional[pd.DataFrame] = None
        self.retention_matrix: Optional[pd.DataFrame] = None
        self.generated_figures: list = []

    def run_all(self, export_plots: bool = True, save_processed: bool = True) -> Dict[str, Any]:
        """
        Thực thi toàn bộ pipeline từ đầu đến cuối:
        1. Load -> 2. Clean -> 3. Merge -> 4. Feature Engineer -> 5. Save Data -> 6. Visualizations
        """
        start_time = time.time()
        logger.info(f"=== Starting Ecommerce Analytics Pipeline [Source: {self.source_type.upper()}] ===")

        # Bước 1: Nạp dữ liệu
        logger.info("Step 1/6: Loading raw relational tables...")
        self.raw_data = self.loader.load()

        # Bước 2: Làm sạch dữ liệu
        logger.info("Step 2/6: Cleaning and standardizing tables...")
        cleaner = DataCleaner(self.raw_data)
        self.cleaned_data = cleaner.clean_all()

        # Bước 3: Nối ghép tạo Master DataFrames
        logger.info("Step 3/6: Joining tables and calculating net revenue...")
        merger = DataMerger(self.cleaned_data)
        self.master_orders = merger.build_master_orders()
        self.master_items = merger.build_master_order_items(self.master_orders)

        # Bước 4: Tạo lập đặc trưng nâng cao (NumPy & Pandas)
        logger.info("Step 4/6: Computing RFM, Cohort and Time-series metrics...")
        engineer = FeatureEngineer(self.master_orders, self.master_items)
        self.rfm_df = engineer.compute_rfm_metrics_numpy()
        self.monthly_df = engineer.compute_monthly_time_series()
        _, self.retention_matrix = engineer.compute_cohort_retention_matrix()

        # Bước 5: Lưu trữ dữ liệu đã xử lý vào data/processed/
        if save_processed:
            logger.info("Step 5/6: Exporting processed datasets to data/processed/...")
            self._save_processed_data()

        # Bước 6: Trực quan hóa dữ liệu và xuất đồ thị
        if export_plots:
            logger.info("Step 6/6: Rendering and exporting high-resolution visualization figures...")
            self._generate_all_visualizations()

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"=== Pipeline completed successfully in {elapsed}s ===")

        return self.get_summary_statistics()

    def _save_processed_data(self) -> None:
        """Lưu các bảng phân tích đã xử lý sang định dạng CSV trong data/processed/."""
        target_dir = settings.PROCESSED_DATA_DIR
        target_dir.mkdir(parents=True, exist_ok=True)

        if self.master_orders is not None:
            self.master_orders.to_csv(target_dir / "clean_master_orders.csv", index=False)
        if self.rfm_df is not None:
            self.rfm_df.to_csv(target_dir / "customer_rfm_metrics.csv", index=False)
        if self.monthly_df is not None:
            self.monthly_df.to_csv(target_dir / "monthly_financial_trends.csv", index=False)
        if self.retention_matrix is not None:
            self.retention_matrix.to_csv(target_dir / "cohort_retention_matrix.csv")

        logger.info(f"All processed data exported to: {target_dir}")

    def _generate_all_visualizations(self) -> None:
        """Sinh và xuất toàn bộ 13 đồ thị chuẩn theo chương 7 của học phần."""
        self.generated_figures.clear()

        # 1 & 2: Trend plots (Line & Multi-line)
        f1 = self.trend_viz.plot_financial_performance_trends(self.monthly_df)
        f2 = self.trend_viz.plot_segment_growth_multiline(self.master_orders)
        self.generated_figures.extend([f1, f2])

        # 3, 4 & 5: Distribution plots (Hist, Box, Violin, Swarm)
        f3 = self.dist_viz.plot_order_total_distribution(self.master_orders)
        f4 = self.dist_viz.plot_payment_methods_box_violin(self.master_orders)
        f5 = self.dist_viz.plot_refund_reason_swarm(self.cleaned_data["refunds"])
        self.generated_figures.extend([f3, f4, f5])

        # 6, 7 & 8: Categorical plots (Donut, Bar, Catplot)
        f6 = self.cat_viz.plot_acquisition_channel_donut(self.cleaned_data["customers"])
        f7 = self.cat_viz.plot_top_products_bar(self.master_items)
        f8 = self.cat_viz.plot_customer_segment_catplot(self.master_orders)
        self.generated_figures.extend([f6, f7, f8])

        # 9, 10, 11, 12 & 13: Relational plots (Scatter, Pairplot, FacetGrid, Heatmaps)
        f9 = self.rel_viz.plot_cost_vs_price_scatter(self.cleaned_data["products"])
        f10 = self.rel_viz.plot_rfm_pairplot(self.rfm_df)
        f11 = self.rel_viz.plot_facetgrid_category_segments(self.master_items)
        f12 = self.rel_viz.plot_cohort_retention_heatmap(self.retention_matrix)
        f13 = self.rel_viz.plot_financial_correlation_heatmap(self.master_orders)
        self.generated_figures.extend([f9, f10, f11, f12, f13])

        logger.info(f"Rendered {len(self.generated_figures)} high-res figures to {settings.FIGURES_DIR}")

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Tổng hợp các chỉ số KPI doanh nghiệp chính."""
        if self.master_orders is None:
            return {}

        total_orders = len(self.master_orders)
        total_customers = self.master_orders["customer_id"].nunique()
        gross_sales = float(self.master_orders["subtotal"].sum())
        total_paid = float(self.master_orders["paid_amount"].sum())
        total_refunded = float(self.master_orders["refunded_amount"].sum())
        net_sales = float(self.master_orders["net_sales"].sum())
        refund_rate = (total_refunded / total_paid * 100) if total_paid > 0 else 0.0
        avg_order_value = net_sales / total_orders if total_orders > 0 else 0.0

        top_segment = self.master_orders["customer_segment"].value_counts().index[0]
        top_channel = self.master_orders["acquisition_channel"].value_counts().index[0]

        return {
            "total_orders": total_orders,
            "total_customers": total_customers,
            "gross_sales": round(gross_sales, 2),
            "total_paid": round(total_paid, 2),
            "total_refunded": round(total_refunded, 2),
            "net_sales": round(net_sales, 2),
            "refund_rate_pct": round(refund_rate, 2),
            "avg_order_value": round(avg_order_value, 2),
            "top_segment": top_segment,
            "top_channel": top_channel,
            "figures_count": len(self.generated_figures),
        }

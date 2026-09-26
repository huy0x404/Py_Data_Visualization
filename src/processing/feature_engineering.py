"""
Feature Engineering module.
Integrates:
- Advanced NumPy array operations, broadcasting, statistics, and linear algebra (Chapter 5)
- Pandas advanced aggregations, pivot tables, and Cohort Analysis (Chapter 6)
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
import logging

from ..core.exceptions import ProcessingError

logger = logging.getLogger("FeatureEngineer")


class FeatureEngineer:
    """Tạo lập các tập đặc trưng nâng cao sử dụng NumPy và Pandas."""

    def __init__(self, master_orders: pd.DataFrame, master_items: pd.DataFrame):
        self.orders = master_orders
        self.items = master_items

    # =========================================================================
    # 1. NUMPY-DRIVEN COMPUTATIONS (Chương 5: Mảng, Thống kê, Đại số tuyến tính)
    # =========================================================================

    def compute_rfm_metrics_numpy(self, reference_date: pd.Timestamp = None) -> pd.DataFrame:
        """
        Tính toán chỉ số RFM (Recency, Frequency, Monetary) kết hợp vector hóa NumPy:
        - Recency: Số ngày từ đơn hàng cuối đến ngày mốc (reference_date)
        - Frequency: Tổng số đơn hàng đã đặt
        - Monetary: Tổng Net Sales của khách hàng
        - Chuẩn hóa Z-Score và tính khoảng cách Euclid (Euclidean Distance) bằng NumPy.
        """
        logger.info("Computing Customer RFM metrics using NumPy vectorized operations...")
        try:
            if reference_date is None:
                reference_date = self.orders["ordered_at"].max() + pd.Timedelta(days=1)

            # Tổng hợp cơ bản qua Pandas
            rfm = (
                self.orders.groupby("customer_id")
                .agg(
                    last_order_date=("ordered_at", "max"),
                    frequency=("order_id", "nunique"),
                    monetary=("net_sales", "sum"),
                    first_order_date=("ordered_at", "min"),
                    customer_segment=("customer_segment", "first"),
                    country_code=("country_code", "first"),
                )
                .reset_index()
            )

            # Tính Recency (ngày)
            rfm["recency"] = (reference_date - rfm["last_order_date"]).dt.days

            # --- SỬ DỤNG NUMPY MẢNG ĐA CHIỀU & PHÉP TOÁN VECTOR HÓA ---
            # Chuyển đổi sang mảng 2D NumPy (N x 3)
            recency_vals = rfm["recency"].to_numpy(dtype=np.float64)
            frequency_vals = rfm["frequency"].to_numpy(dtype=np.float64)
            # Thay thế monetary âm hoặc bằng 0 bằng epsilon nhỏ để log-transform
            monetary_vals = np.clip(rfm["monetary"].to_numpy(dtype=np.float64), a_min=0.01, a_max=None)

            # Log transformation để giảm độ lệch (skewness)
            log_r = np.log1p(recency_vals)
            log_f = np.log1p(frequency_vals)
            log_m = np.log1p(monetary_vals)

            # Ma trận đặc trưng đã biến đổi (N x 3)
            X = np.column_stack((log_r, log_f, log_m))

            # Tính Mean và Std bằng hàm thống kê NumPy (Chapter 5.5)
            means = np.mean(X, axis=0)
            stds = np.std(X, axis=0)
            # Tránh chia cho 0
            stds = np.where(stds == 0, 1.0, stds)

            # Chuẩn hóa Z-Score theo phương pháp Broadcasting của NumPy
            # X_scaled = (X - Mean) / Std
            X_scaled = (X - means) / stds

            rfm["r_scaled"] = X_scaled[:, 0]
            rfm["f_scaled"] = X_scaled[:, 1]
            rfm["m_scaled"] = X_scaled[:, 2]

            # Vector đại diện khách hàng lý tưởng (Recency thấp -> âm, Freq cao, Monetary cao)
            ideal_centroid = np.array([np.min(X_scaled[:, 0]), np.max(X_scaled[:, 1]), np.max(X_scaled[:, 2])])

            # Tính ma trận khoảng cách Euclid (Euclidean distance) tới điểm lý tưởng bằng NumPy Linear Algebra
            # norm(X_scaled - ideal_centroid, axis=1) (Chapter 5.6)
            diff = X_scaled - ideal_centroid
            distances = np.linalg.norm(diff, axis=1)
            rfm["distance_to_vip"] = distances.round(4)

            # Phân loại khách hàng theo Quantiles
            rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
            rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
            rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
            rfm["rfm_combined"] = (
                rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)
            )

            # Gán nhãn phân khúc (Customer Segment label)
            def segment_label(row):
                score = row["r_score"] + row["f_score"] + row["m_score"]
                if score >= 10:
                    return "Champions"
                elif score >= 8:
                    return "Loyal Customers"
                elif score >= 6:
                    return "Potential Loyalists"
                elif score >= 4:
                    return "At Risk"
                else:
                    return "Hibernating"

            rfm["rfm_segment"] = rfm.apply(segment_label, axis=1)

            logger.info(f"RFM metrics computed: {len(rfm):,} customers segmented.")
            return rfm

        except Exception as e:
            raise ProcessingError(step="compute_rfm_metrics_numpy", reason=str(e)) from e

    def compute_correlation_matrix_numpy(self, df: pd.DataFrame, numeric_cols: list) -> Tuple[np.ndarray, list]:
        """
        Tính toán ma trận tương quan trực tiếp bằng np.corrcoef (Chapter 5.5, 5.6).
        """
        data_matrix = df[numeric_cols].to_numpy(dtype=np.float64)
        # corrcoef nhận ma trận trong đó mỗi hàng là một biến (rowvar=False để mỗi cột là một biến)
        corr_matrix = np.corrcoef(data_matrix, rowvar=False)
        return corr_matrix, numeric_cols

    # =========================================================================
    # 2. PANDAS-DRIVEN AGGREGATIONS & TIME SERIES (Chương 6)
    # =========================================================================

    def compute_monthly_time_series(self) -> pd.DataFrame:
        """
        Tính toán các chỉ số kinh doanh theo chuỗi thời gian hàng tháng:
        - Tổng doanh thu gộp (Gross Subtotal)
        - Tổng hoàn tiền (Refund Amount)
        - Doanh thu thuần (Net Sales)
        - Tỷ lệ hoàn tiền (Refund Rate %)
        - Giá trị trung bình đơn hàng (AOV)
        - Trung bình động 3 tháng (3-Month Rolling Average)
        """
        logger.info("Computing monthly financial time series...")
        try:
            monthly = (
                self.orders.groupby("order_month")
                .agg(
                    total_orders=("order_id", "count"),
                    active_customers=("customer_id", "nunique"),
                    gross_sales=("subtotal", "sum"),
                    paid_amount=("paid_amount", "sum"),
                    refund_amount=("refunded_amount", "sum"),
                    net_sales=("net_sales", "sum"),
                )
                .reset_index()
            )

            # Sắp xếp theo chuỗi thời gian
            monthly["period_dt"] = pd.to_datetime(monthly["order_month"])
            monthly = monthly.sort_values("period_dt").reset_index(drop=True)

            # Các chỉ số tài chính tính toán thêm
            monthly["refund_rate_pct"] = np.where(
                monthly["paid_amount"] > 0,
                (monthly["refund_amount"] / monthly["paid_amount"]) * 100.0,
                0.0,
            ).round(2)

            monthly["aov"] = (monthly["net_sales"] / monthly["total_orders"]).round(2)

            # Rolling moving average (Trung bình động 3 tháng với Pandas rolling)
            monthly["net_sales_roll3"] = monthly["net_sales"].rolling(window=3, min_periods=1).mean().round(2)

            return monthly

        except Exception as e:
            raise ProcessingError(step="compute_monthly_time_series", reason=str(e)) from e

    def compute_cohort_retention_matrix(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Phân tích Cohort Retention hàng tháng:
        - Xác định Cohort Month (tháng mua đầu tiên của mỗi khách hàng)
        - Tính Cohort Index (khoảng cách tháng so với lần mua đầu)
        - Tạo Pivot Table số lượng khách hàng quay lại và tỷ lệ giữ chân (Retention Rate %)
        """
        logger.info("Computing monthly cohort retention matrix...")
        try:
            df = self.orders[["customer_id", "ordered_at"]].copy()
            dt_clean = df["ordered_at"].dt.tz_localize(None) if df["ordered_at"].dt.tz is not None else df["ordered_at"]

            # 1. Tháng phát sinh đơn hàng
            df["order_month"] = dt_clean.dt.to_period("M")

            # 2. Tháng mua hàng đầu tiên của mỗi khách (Cohort Month)
            df["cohort_month"] = df.groupby("customer_id")["order_month"].transform("min")

            # 3. Tính chỉ số tháng (Cohort Index: 0, 1, 2, ...)
            cohort_year = df["cohort_month"].dt.year
            cohort_m = df["cohort_month"].dt.month
            order_year = df["order_month"].dt.year
            order_m = df["order_month"].dt.month

            years_diff = order_year - cohort_year
            months_diff = order_m - cohort_m
            df["cohort_index"] = years_diff * 12 + months_diff

            # 4. Gom nhóm tính số khách hàng duy nhất hoạt động
            cohort_group = (
                df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
            )

            # 5. Pivot Table
            cohort_counts = cohort_group.pivot(index="cohort_month", columns="cohort_index", values="customer_id")

            # 6. Tính tỷ lệ Retention %
            cohort_size = cohort_counts.iloc[:, 0]
            retention_matrix = cohort_counts.divide(cohort_size, axis=0) * 100.0

            # Định dạng index thành chuỗi YYYY-MM
            cohort_counts.index = cohort_counts.index.astype(str)
            retention_matrix.index = retention_matrix.index.astype(str)

            logger.info("Cohort Retention Matrix computed successfully.")
            return cohort_counts, retention_matrix

        except Exception as e:
            raise ProcessingError(step="compute_cohort_retention_matrix", reason=str(e)) from e

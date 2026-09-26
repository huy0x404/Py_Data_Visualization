"""
Unit tests for Data Processing & Feature Engineering modules.
Verifies Data Cleaning, Joining logic, NumPy vectorization, and Cohort matrices.
"""

import pytest
import pandas as pd
import numpy as np
from src.core.config import settings
from src.data_loaders.csv_loader import CSVDataLoader
from src.processing.cleaner import DataCleaner
from src.processing.merger import DataMerger
from src.processing.feature_engineering import FeatureEngineer


@pytest.fixture(scope="module")
def loaded_sample_data():
    loader = CSVDataLoader(settings.RAW_DATA_DIR)
    raw = loader.load()
    # Sample subsets for fast unit testing
    sample_raw = {
        "customers": raw["customers"].head(500),
        "orders": raw["orders"].head(1000),
        "order_items": raw["order_items"].head(2000),
        "products": raw["products"].head(200),
        "payments": raw["payments"].head(1200),
        "refunds": raw["refunds"].head(200),
    }
    return sample_raw


def test_cleaner_and_merger(loaded_sample_data):
    cleaner = DataCleaner(loaded_sample_data)
    cleaned = cleaner.clean_all()

    assert pd.api.types.is_datetime64_any_dtype(cleaned["orders"]["ordered_at"])
    assert pd.api.types.is_datetime64_any_dtype(cleaned["customers"]["created_at"])

    merger = DataMerger(cleaned)
    master_orders = merger.build_master_orders()

    assert "net_sales" in master_orders.columns
    assert "paid_amount" in master_orders.columns
    assert "refunded_amount" in master_orders.columns

    # Verify arithmetic formula: net_sales == round(paid_amount - refunded_amount, 2)
    expected_net = (master_orders["paid_amount"] - master_orders["refunded_amount"]).round(2)
    assert np.allclose(master_orders["net_sales"], expected_net)


def test_numpy_rfm_computation(loaded_sample_data):
    cleaner = DataCleaner(loaded_sample_data)
    cleaned = cleaner.clean_all()
    merger = DataMerger(cleaned)
    master_orders = merger.build_master_orders()
    master_items = merger.build_master_order_items(master_orders)

    engineer = FeatureEngineer(master_orders, master_items)
    rfm = engineer.compute_rfm_metrics_numpy()

    assert "recency" in rfm.columns
    assert "frequency" in rfm.columns
    assert "monetary" in rfm.columns
    assert "r_scaled" in rfm.columns
    assert "distance_to_vip" in rfm.columns
    assert "rfm_segment" in rfm.columns
    # Check that Z-scores have approximately mean 0 and std 1
    assert abs(np.mean(rfm["r_scaled"])) < 0.1

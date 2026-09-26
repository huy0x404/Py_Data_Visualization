"""
Unit tests for Data Loaders (CSVDataLoader, SQLiteDataLoader, Models).
Verifies OOP Abstraction, Polymorphism, and Exception handling.
"""

import pytest
from pathlib import Path
from src.core.config import settings
from src.core.exceptions import DataLoadError, DatabaseConnectionError
from src.data_loaders.csv_loader import CSVDataLoader
from src.data_loaders.sqlite_loader import SQLiteDataLoader
from src.data_loaders.models import Customer, Product, Order


def test_customer_model_validation():
    # Valid customer
    cust = Customer(
        customer_id="cust_001",
        country_code="US",
        acquisition_channel="organic_search",
        customer_segment="consumer",
    )
    assert cust.id == "cust_001"
    assert cust.customer_segment == "consumer"
    assert not cust.is_enterprise()

    # Invalid customer segment raises ValueError (Encapsulation test)
    with pytest.raises(ValueError):
        Customer(
            customer_id="cust_002",
            country_code="US",
            acquisition_channel="direct",
            customer_segment="invalid_segment",
        )


def test_product_model_margin():
    prod = Product(
        product_id="prod_01",
        sku="SKU-100",
        product_name="Wireless Mouse",
        category="Electronics",
        unit_cost=20.0,
        list_price=50.0,
    )
    assert prod.profit_margin == 30.0
    assert prod.markup_percentage == 150.0


def test_order_model_total():
    order = Order(
        order_id="ord_01",
        customer_id="cust_001",
        ordered_at=None,
        order_status="completed",
        subtotal=100.0,
        tax_amount=8.5,
        shipping_amount=5.0,
    )
    assert order.total_calculated == 113.5


def test_csv_data_loader():
    loader = CSVDataLoader(settings.RAW_DATA_DIR)
    data = loader.load()
    assert loader.is_loaded
    assert "orders" in data
    assert "customers" in data
    assert len(data["customers"]) > 0


def test_csv_loader_invalid_path():
    with pytest.raises(DataLoadError):
        loader = CSVDataLoader(Path("invalid/non_existent_folder"))


def test_sqlite_data_loader():
    loader = SQLiteDataLoader(settings.SQLITE_DB_PATH)
    data = loader.load()
    assert loader.is_loaded
    assert "orders" in data
    assert len(data["orders"]) > 0

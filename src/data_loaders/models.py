"""
OOP Domain Models representing core entities in the Ecommerce business.
Demonstrates:
- Class & Object creation (3.1)
- Methods (Instance, Class, Dunder methods __repr__, __eq__) (3.2)
- Encapsulation & Properties with validation (3.6)
- Inheritance (3.3)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


class Entity:
    """Base class providing common string representation and identity check."""
    def __init__(self, entity_id: str):
        if not entity_id or not isinstance(entity_id, str):
            raise ValueError("Entity ID must be a non-empty string.")
        self._id = entity_id

    @property
    def id(self) -> str:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._id == other._id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self._id}')>"


class Customer(Entity):
    """Represents a customer entity with segment and country info."""

    VALID_SEGMENTS = {"consumer", "small_business", "enterprise"}

    def __init__(
        self,
        customer_id: str,
        country_code: str,
        acquisition_channel: str,
        customer_segment: str,
        created_at: Optional[datetime] = None,
    ):
        super().__init__(customer_id)
        self.country_code = country_code.upper()
        self.acquisition_channel = acquisition_channel
        self._customer_segment = None
        self.customer_segment = customer_segment
        self.created_at = created_at or datetime.now()

    @property
    def customer_segment(self) -> str:
        return self._customer_segment

    @customer_segment.setter
    def customer_segment(self, segment: str):
        normalized = segment.lower().strip()
        if normalized not in self.VALID_SEGMENTS:
            raise ValueError(f"Invalid segment '{segment}'. Must be one of {self.VALID_SEGMENTS}")
        self._customer_segment = normalized

    def is_enterprise(self) -> bool:
        """Domain logic method."""
        return self.customer_segment == "enterprise"


class Product(Entity):
    """Represents a product item with cost, list price, and margin calculations."""

    def __init__(
        self,
        product_id: str,
        sku: str,
        product_name: str,
        category: str,
        unit_cost: float,
        list_price: float,
    ):
        super().__init__(product_id)
        self.sku = sku
        self.product_name = product_name
        self.category = category
        self._unit_cost = float(unit_cost)
        self._list_price = float(list_price)

    @property
    def unit_cost(self) -> float:
        return self._unit_cost

    @property
    def list_price(self) -> float:
        return self._list_price

    @property
    def profit_margin(self) -> float:
        """Calculates margin in USD."""
        return self._list_price - self._unit_cost

    @property
    def markup_percentage(self) -> float:
        """Calculates markup percentage over cost."""
        if self._unit_cost <= 0:
            return 0.0
        return ((self._list_price - self._unit_cost) / self._unit_cost) * 100.0


class Order(Entity):
    """Represents an order containing subtotal, tax, shipping, and order status."""

    def __init__(
        self,
        order_id: str,
        customer_id: str,
        ordered_at: datetime,
        order_status: str,
        subtotal: float,
        tax_amount: float = 0.0,
        shipping_amount: float = 0.0,
    ):
        super().__init__(order_id)
        self.customer_id = customer_id
        self.ordered_at = ordered_at
        self.order_status = order_status
        self.subtotal = float(subtotal)
        self.tax_amount = float(tax_amount)
        self.shipping_amount = float(shipping_amount)

    @property
    def total_calculated(self) -> float:
        """Total = subtotal + tax + shipping."""
        return round(self.subtotal + self.tax_amount + self.shipping_amount, 2)

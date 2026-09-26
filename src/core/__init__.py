"""Core module package."""
from .config import settings, PlotConfig, ProjectSettings
from .exceptions import (
    EcommerceAnalyticsError,
    DataLoadError,
    DatabaseConnectionError,
    DataValidationError,
    ProcessingError,
    VisualizationError,
)

__all__ = [
    "settings",
    "PlotConfig",
    "ProjectSettings",
    "EcommerceAnalyticsError",
    "DataLoadError",
    "DatabaseConnectionError",
    "DataValidationError",
    "ProcessingError",
    "VisualizationError",
]

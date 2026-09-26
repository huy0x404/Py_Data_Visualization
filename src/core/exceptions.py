"""
Custom exception hierarchy for the Ecommerce Analytics & Visualization project.
Demonstrates OOP Exception handling, custom exception inheritance, and clean error reporting.
"""


class EcommerceAnalyticsError(Exception):
    """Base exception class for all errors in the Ecommerce Analytics application."""
    def __init__(self, message: str = "An error occurred in the analytics pipeline."):
        super().__init__(message)
        self.message = message


class DataLoadError(EcommerceAnalyticsError):
    """Raised when there is an issue loading raw data from disk or network."""
    def __init__(self, source_path: str, reason: str):
        message = f"Failed to load data from '{source_path}'. Reason: {reason}"
        super().__init__(message)
        self.source_path = source_path
        self.reason = reason


class DatabaseConnectionError(DataLoadError):
    """Raised when SQLite database cannot be accessed or queried."""
    def __init__(self, db_path: str, reason: str):
        super().__init__(source_path=db_path, reason=f"Database error: {reason}")


class DataValidationError(EcommerceAnalyticsError):
    """Raised when data fails schema validation or sanity checks."""
    def __init__(self, table_name: str, missing_columns: list):
        message = f"Table '{table_name}' failed validation. Missing required columns: {missing_columns}"
        super().__init__(message)
        self.table_name = table_name
        self.missing_columns = missing_columns


class ProcessingError(EcommerceAnalyticsError):
    """Raised during transformation, cleaning, or feature engineering steps."""
    def __init__(self, step: str, reason: str):
        message = f"Error during data processing step '{step}': {reason}"
        super().__init__(message)
        self.step = step
        self.reason = reason


class VisualizationError(EcommerceAnalyticsError):
    """Raised when rendering or exporting a figure fails."""
    def __init__(self, figure_name: str, reason: str):
        message = f"Failed to render figure '{figure_name}': {reason}"
        super().__init__(message)
        self.figure_name = figure_name
        self.reason = reason

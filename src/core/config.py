"""
Core configuration module for the Ecommerce Analytics & Visualization project.
Defines system paths, color schemes, default figure parameters, and database paths.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any

# Root directories
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SQLITE_DB_PATH = RAW_DATA_DIR / "sqlite" / "ecommerce.sqlite"

REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"


@dataclass(frozen=True)
class PlotConfig:
    """Configuration settings for Matplotlib and Seaborn aesthetics."""
    dpi: int = 300
    figure_format: str = "png"
    style: str = "whitegrid"
    palette_primary: str = "Blues_r"
    palette_categorical: str = "deep"
    font_family: str = "sans-serif"
    default_figsize: tuple = (12, 7)
    title_fontsize: int = 15
    label_fontsize: int = 12
    ticks_fontsize: int = 10
    legend_fontsize: int = 10


@dataclass
class ProjectSettings:
    """Global project settings."""
    project_name: str = "Ecommerce Data Visualization"
    version: str = "1.0.0"
    random_seed: int = 42
    root_dir: Path = ROOT_DIR
    raw_data_dir: Path = RAW_DATA_DIR
    processed_data_dir: Path = PROCESSED_DATA_DIR
    sqlite_db_path: Path = SQLITE_DB_PATH
    reports_dir: Path = REPORTS_DIR
    figures_dir: Path = FIGURES_DIR
    notebooks_dir: Path = NOTEBOOKS_DIR

    # Uppercase aliases for compatibility
    RAW_DATA_DIR: Path = RAW_DATA_DIR
    PROCESSED_DATA_DIR: Path = PROCESSED_DATA_DIR
    SQLITE_DB_PATH: Path = SQLITE_DB_PATH
    REPORTS_DIR: Path = REPORTS_DIR
    FIGURES_DIR: Path = FIGURES_DIR
    NOTEBOOKS_DIR: Path = NOTEBOOKS_DIR

    plot_config: PlotConfig = field(default_factory=PlotConfig)

    def ensure_directories(self) -> None:
        """Create necessary directories if they do not exist."""
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


# Global singleton instance
settings = ProjectSettings()
settings.ensure_directories()

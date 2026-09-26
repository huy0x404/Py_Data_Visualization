"""
Base Visualizer module.
Provides centralized styling, aesthetic configurations, color palettes,
and figure saving capabilities using Matplotlib and Seaborn (Chapter 7).
"""

from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from ..core.config import settings, PlotConfig
from ..core.exceptions import VisualizationError

logger = logging.getLogger("BaseVisualizer")


class BaseVisualizer:
    """Lớp cơ sở quản lý thẩm mỹ và lưu trữ đồ thị cho toàn bộ hệ thống."""

    def __init__(self, config: Optional[PlotConfig] = None):
        self.config = config or settings.plot_config
        self.apply_theme()

    def apply_theme(self) -> None:
        """Thiết lập theme chuẩn: seaborn whitegrid, font hiện đại, tỉ lệ nhãn đồng nhất."""
        sns.set_theme(
            style=self.config.style,
            palette=self.config.palette_categorical,
            font=self.config.font_family,
        )
        plt.rcParams.update(
            {
                "font.size": self.config.label_fontsize,
                "axes.titlesize": self.config.title_fontsize,
                "axes.labelsize": self.config.label_fontsize,
                "xtick.labelsize": self.config.ticks_fontsize,
                "ytick.labelsize": self.config.ticks_fontsize,
                "legend.fontsize": self.config.legend_fontsize,
                "figure.titlesize": self.config.title_fontsize + 2,
                "figure.dpi": 100,  # on-screen preview
                "savefig.dpi": self.config.dpi,  # saved image resolution
                "figure.autolayout": True,
            }
        )

    def create_figure(
        self,
        figsize: Optional[Tuple[int, int]] = None,
        nrows: int = 1,
        ncols: int = 1,
        **kwargs,
    ) -> Tuple[plt.Figure, any]:
        """Tạo Figure và Axes với kích thước chuẩn."""
        size = figsize or self.config.default_figsize
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=size, **kwargs)
        return fig, axes

    def save_figure(
        self,
        fig: plt.Figure,
        filename: str,
        output_dir: Optional[Path] = None,
        close_after: bool = True,
    ) -> Path:
        """
        Lưu đồ thị thành file hình ảnh với độ phân giải cao (300 DPI),
        tự động tạo thư mục và đóng figure để giải phóng bộ nhớ.
        """
        target_dir = Path(output_dir or settings.FIGURES_DIR)
        target_dir.mkdir(parents=True, exist_ok=True)

        if not filename.endswith(f".{self.config.figure_format}"):
            filename = f"{filename}.{self.config.figure_format}"

        file_path = target_dir / filename

        try:
            fig.savefig(
                file_path,
                dpi=self.config.dpi,
                bbox_inches="tight",
                facecolor="white",
                edgecolor="none",
            )
            logger.info(f"Figure exported successfully: {file_path}")
            if close_after:
                plt.close(fig)
            return file_path
        except Exception as e:
            if close_after:
                plt.close(fig)
            raise VisualizationError(figure_name=filename, reason=str(e)) from e

    def format_currency_axis(self, ax, axis: str = "y"):
        """Định dạng trục hiển thị đơn vị tiền tệ $ USD."""
        import matplotlib.ticker as ticker
        formatter = ticker.StrMethodFormatter("${x:,.0f}")
        if axis == "y":
            ax.yaxis.set_major_formatter(formatter)
        elif axis == "x":
            ax.xaxis.set_major_formatter(formatter)

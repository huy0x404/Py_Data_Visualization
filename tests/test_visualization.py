"""
Unit tests for Visualization modules.
Verifies figure creation, file rendering, and export integrity without GUI display.
"""

import pytest
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for testing
import matplotlib.pyplot as plt
from pathlib import Path
from src.core.config import settings
from src.visualization.base_visualizer import BaseVisualizer


def test_base_visualizer_export(tmp_path):
    viz = BaseVisualizer()
    fig, ax = viz.create_figure()
    ax.plot([1, 2, 3], [4, 5, 6], label="Test Line")
    ax.set_title("Test Chart")

    exported_file = viz.save_figure(fig, "test_plot.png", output_dir=tmp_path)
    assert exported_file.exists()
    assert exported_file.stat().st_size > 0

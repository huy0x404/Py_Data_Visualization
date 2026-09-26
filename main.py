"""
Main CLI Application Entrypoint for Ecommerce Data Analytics & Visualization.
Allows executing the entire data pipeline from CSV or SQLite data sources.
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import EcommercePipeline
from src.core.config import settings
from src.core.exceptions import EcommerceAnalyticsError


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python Ecommerce Data Analytics & Visualization Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--source",
        choices=["csv", "sqlite"],
        default="csv",
        help="Data source format to load (csv from data/raw/ or sqlite from data/raw/sqlite/ecommerce.sqlite)",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip figure rendering and export to reports/figures/",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Skip saving processed CSV tables into data/processed/",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print("=" * 80)
    print("      PYTHON DATA VISUALIZATION & ANALYTICS PIPELINE (CLO1 - CLO5)")
    print("=" * 80)
    print(f"Data Source   : {args.source.upper()}")
    print(f"Export Plots  : {not args.no_plots}")
    print(f"Save Processed: {not args.no_save}")
    print(f"Figures Output: {settings.FIGURES_DIR}")
    print(f"Data Output   : {settings.PROCESSED_DATA_DIR}")
    print("-" * 80)

    try:
        pipeline = EcommercePipeline(source_type=args.source)
        summary = pipeline.run_all(
            export_plots=not args.no_plots,
            save_processed=not args.no_save,
        )

        print("\n" + "=" * 80)
        print("                        EXECUTIVE SUMMARY KPI RESULTS")
        print("=" * 80)
        print(f"  • Total Orders Processed : {summary['total_orders']:,}")
        print(f"  • Active Customers       : {summary['total_customers']:,}")
        print(f"  • Gross Revenue (Subtotal): ${summary['gross_sales']:,.2f}")
        print(f"  • Total Succeeded Payments: ${summary['total_paid']:,.2f}")
        print(f"  • Total Refunds Issued   : ${summary['total_refunded']:,.2f}")
        print(f"  • Net Realized Revenue   : ${summary['net_sales']:,.2f}")
        print(f"  • Overall Refund Rate    : {summary['refund_rate_pct']:.2f}%")
        print(f"  • Average Order Value    : ${summary['avg_order_value']:,.2f}")
        print(f"  • Dominant Customer Type : {summary['top_segment'].title()}")
        print(f"  • Top Acquisition Channel: {summary['top_channel'].title()}")
        print(f"  • High-Res Figures Made  : {summary['figures_count']} files")
        print("=" * 80)
        print(" Pipeline finished successfully! Check 'reports/figures/' for output graphs.\n")

    except EcommerceAnalyticsError as e:
        print(f"\n[PIPELINE ERROR] {e.__class__.__name__}: {e.message}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()

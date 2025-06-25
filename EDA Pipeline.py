import os
import sys
import argparse
import pandas as pd
from pathlib import Path


try:
    from ydata_profiling import ProfileReport
except ImportError:
    ProfileReport = None


#Loading Data
def load_data(source: str) -> pd.DataFrame:
    """
    Load a dataset from a local path, URL, or cloud storage URI.
    Supports CSV, Excel, JSON, Parquet from filesystem or HTTP(S)/S3/GCS.
    """
    # Determine if source is a URL or local path
    parsed = urlparse(source)
    is_remote = parsed.scheme in ("http", "https", "s3", "gs")

    # Use pandas to read based on extension
    ext = Path(parsed.path if is_remote else source).suffix.lower()

    # For remote, pandas can usually handle HTTP; for S3/GCS requires proper FS
    read_opts = {}
    if parsed.scheme == "s3":
        if s3fs is None:
            raise ImportError("s3fs is required to read from S3 URIs. Install via `pip install s3fs`.")
        read_opts['storage_options'] = {'anon': False}
    elif parsed.scheme == "gs":
        if gcsfs is None:
            raise ImportError("gcsfs is required to read from GCS URIs. Install via `pip install gcsfs`.")
        read_opts['storage_options'] = {'token': None}


    # Map extensions to pandas read functions
    if ext == ".csv":
        return pd.read_csv(source, **read_opts)
    elif ext in [".xls", ".xlsx"]:
        return pd.read_excel(source, **read_opts)
    elif ext == ".json":
        return pd.read_json(source, **read_opts)
    elif ext == ".parquet":
        return pd.read_parquet(source, **read_opts)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


#Summary statistics
def basic_summary(df: pd.DataFrame) -> None:
    print("\n=== BASIC INFO ===")
    print(df.info())
    print("\n=== HEAD ===")
    print(df.head())
    print("\n=== TAIL ===")
    print(df.tail())
    print(f"\nShape: {df.shape}")


def numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== NUMERIC STATISTICS ===")
    stats = df.describe(include=["number"])
    print(stats)
    return stats


# Missing Values Report
def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== MISSING VALUES ===")
    missing = df.isna().sum().to_frame(name="missing_count")
    missing["missing_pct"] = (missing["missing_count"] / len(df)) * 100
    print(missing.sort_values("missing_count", ascending=False))
    return missing


# Generate HTML profiling report
def generate_profile(df: pd.DataFrame, output: Path) -> None:
    """
    Generate an HTML profiling report if ydata-profiling is installed.
    """
    if ProfileReport is None:
        print("ydata-profiling not installed. Skipping detailed report.")
        return
    profile = ProfileReport(df, title="AutoMate-EDA Report", explorative=True)
    profile.to_file(output)
    print(f"Detailed report saved to {output}")


# Main function to parse arguments abd run the EDA pipeline
def main():
    parser = argparse.ArgumentParser(
        prog="AutoMate-EDA",
        description="Automate comprehensive EDA for any dataset."
    )
    parser.add_argument(
        "file", type=Path,
        help="Path to your dataset file (CSV, Excel, JSON, Parquet)."
    )
    parser.add_argument(
        "--profile", action="store_true",
        help="Generate detailed HTML profiling report (requires ydata-profiling)."
    )
    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: File {args.file} not found.")
        sys.exit(1)

    df = load_data(args.file)
    basic_summary(df)
    numeric_stats(df)
    missing_report(df)

    if args.profile:
        out = args.file.with_suffix('.html')
        generate_profile(df, out)

if __name__ == "__main__":
    main()

import pandas as pd



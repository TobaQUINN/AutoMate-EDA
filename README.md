# AutoMate-EDA

[![PyPI version](https://img.shields.io/pypi/v/automate-eda)]()
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/AutoMate-EDA/ci.yml)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE)

## Overview

**AutoMate-EDA** is a lightweight, smart, and extensible Python CLI tool to automate comprehensive Exploratory Data Analysis (EDA) on any tabular dataset. It seamlessly handles local files, HTTP(S) URLs, AWS S3, and Google Cloud Storage (GCS) URIs, producing quick summaries and optional interactive HTML reports.

Key features:

* 📂 Supports CSV, Excel, JSON, Parquet
* ☁️ Reads from local paths, HTTP/S, `s3://`, `gs://`
* 📊 Prints basic info, head/tail, shape, numeric stats, and missing-value report
* 📝 Optional HTML profiling via `ydata-profiling`
* 🔄 Continuous optimizations and improvements over time
* 🔧 Easily extendable: add plotting, logging, config files, and more

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/AutoMate-EDA.git
   cd AutoMate-EDA
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux/macOS
   .\.venv\Scripts\activate    # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

> **Note:** To enable HTML profiling, also install:
>
> ```bash
> pip install ydata-profiling s3fs gcsfs   # optional
> ```

---

## Usage

Run the CLI with a data source:

```bash
# Local CSV file
python eda_pipeline.py data/my_data.csv

# Generate HTML report
python eda_pipeline.py data/my_data.csv --profile

# From HTTP URL
python eda_pipeline.py https://example.com/data.json

# From S3
python eda_pipeline.py s3://my-bucket/data.parquet --profile

# From GCS
python eda_pipeline.py gs://my-bucket/data.xlsx
```

### Arguments

* `<source>` — Path or URI to dataset (CSV, Excel, JSON, Parquet).
* `--profile` — Generate an interactive HTML profiling report (requires `ydata-profiling`).

---

## Extending AutoMate-EDA

Feel free to enhance:

* **Visualization**: add Matplotlib histograms, boxplots, correlation heatmaps
* **Logging**: integrate `logging` with `--verbose` flag
* **Config**: support a YAML config file for default options
* **CLI**: switch to Click for subcommands (`summary`, `profile`, `plot`)

---

## Testing & CI

* Tests are written with `pytest` in the `tests/` folder.
* Pre-commit hooks enforce linting (Black, isort, flake8).
* GitHub Actions runs tests and linters on each PR.

---

## Contributing

1. Fork the repo and create a branch: `feature/your-feature`
2. Make changes and add tests
3. Commit & push: `git push origin feature/your-feature`
4. Open a Pull Request

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Happy data exploring!*

"""Download and load Stack Overflow Developer Survey data.
Files are saved in data/raw/ (this folder is ignored by Git)."""

import os
import urllib.request
import pandas as pd

# Source: Stack Overflow Developer Survey archive (licence: ODbL 1.0)
BASE_URL = ("https://github.com/StackExchange/Survey/raw/refs/heads/main/"
            "packages/archive/{year}/results.csv")

RAW_DIR = os.path.join("data", "raw")


def download_year(year):
    """Download one year's CSV if we don't already have it."""
    os.makedirs(RAW_DIR, exist_ok=True)
    path = os.path.join(RAW_DIR, f"survey_{year}.csv")
    if os.path.exists(path):
        print(f"{year}: already downloaded")
        return path
    print(f"{year}: downloading... (may take a minute)")
    urllib.request.urlretrieve(BASE_URL.format(year=year), path)
    print(f"{year}: saved to {path}")
    return path


def load_year(year):
    """Load one year into a pandas DataFrame."""
    path = download_year(year)
    return pd.read_csv(path, low_memory=False)
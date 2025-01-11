"""Core configuration for pause.map data pipeline."""

from datetime import datetime, date
from pathlib import Path

# Test month - April 2020 (first full month of UK lockdown)
START_DATE = date(2020, 4, 1)
END_DATE = date(2020, 4, 30)

# Base paths - calculate relative to this file
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "storage"

# Storage structure
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = DATA_DIR / "outputs"

# External data sources
GDELT_URL = "http://data.gdeltproject.org/events/{date}.export.CSV.zip"
OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"
WORLDBANK_URL = "https://search.worldbank.org/api/v3/wds"

# Create directories if they don't exist
for dir in [RAW_DIR, PROCESSED_DIR, OUTPUTS_DIR]:
    dir.mkdir(parents=True, exist_ok=True)
# pause.map data pipeline

Data pipeline that captures the global impact of COVID-19 by combining three key data sources:

- GDELT (Global Database of Events, Language and Tone) for global events and sentiment
- Our World in Data (OWID) for COVID-19 case data and responses
- World Bank for economic indicators and analysis

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[test]"
```

## Commands

Get sample data from any source:
```bash
python -m pausemap.cli sample --source [gdelt|owid|worldbank]
```

Fetch full data for configured date range:
```bash
python -m pausemap.cli fetch --source [gdelt|owid|worldbank]
```

## Data Sources

### GDELT
- Daily event data with sentiment analysis
- Categorized global events (protests, cooperation, conflict etc)
- Data stored in CSV format
- Uses polars for fast processing

### OWID
- COVID-19 statistics (cases, deaths, testing)
- Country-level response tracking
- Data stored in JSON/parquet format

### World Bank
- Economic indicators (GDP, employment, trade)
- Research reports and analysis on COVID impact
- Uses their public APIs:
  - Documents API for reports
  - Indicators API for economic data

## Storage Structure

```
storage/
├── raw/          # Raw data from APIs
│   ├── gdelt/    # Daily GDELT CSVs
│   ├── owid/     # OWID JSON data
│   └── worldbank/# World Bank data and docs
├── processed/    # Cleaned & processed data
└── samples/      # Sample data for development
```

## Development
- Uses pyproject.toml for modern Python packaging
- Type hints throughout
- polars for fast data processing
- Consistent error handling and retries for APIs

## Configuration
Data range is configured in config.py (currently set to April 2020 for initial analysis).

## Notes
- All API access is via public endpoints - no authentication needed
- Raw data is cached locally to avoid unnecessary API calls
- Storage directories are gitignored
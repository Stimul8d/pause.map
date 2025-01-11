# pause.map

Mapping global change through COVID: track how events, sentiment, health and economics shifted during the great pause. Built with GDELT, Our World in Data and World Bank metrics.

## Why this matters
Shows how a global event rippled through media, sentiment and economics. Built to highlight the connections between reporting, public mood and economic reality during an unprecedented pause in normal life.

## Data Sources

Three key datasets tell the story:

1. **GDELT** (Global Database of Events, Language and Tone)
   - Daily global events and sentiment
   - Media coverage patterns
   - Social response tracking

2. **Our World in Data (OWID)**
   - COVID-19 case data
   - Testing and vaccination stats
   - Country response measures

3. **World Bank**
   - Economic indicators (GDP, trade, employment)
   - Research reports and analysis
   - Country-specific impact studies

## Project Structure
```
pause.map/
├── data/              # Python data pipeline
│   ├── src/          # Source code
│   │   └── pausemap/ 
│   │       ├── sources/  # Data source handlers
│   │       └── cli.py    # Command line interface
│   └── storage/      # Data storage
│       ├── raw/      # Raw API data
│       ├── processed/# Cleaned data
│       └── samples/  # Sample data
└── site/             # Next.js frontend (WIP)
```

## Current Status

- ✅ Working data pipeline for all three sources
- ✅ Sample data generation
- ✅ Full data fetch for April 2020 (initial analysis)
- 🚧 Data processing and analysis
- 🚧 Frontend visualization  

## Getting Started

1. Set up Python environment:
```bash
cd data
python -m venv venv
source venv/bin/activate
pip install -e ".[test]"
```

2. Try the data pipeline:
```bash
# Get sample data
python -m pausemap.cli sample --source gdelt
python -m pausemap.cli sample --source owid
python -m pausemap.cli sample --source worldbank

# Fetch full data
python -m pausemap.cli fetch --source gdelt
python -m pausemap.cli fetch --source owid
python -m pausemap.cli fetch --source worldbank
```

## Tech Stack

- **Data Pipeline**: 
  - Python 3.10+
  - polars for fast data processing
  - Public APIs (no auth needed)
  - Type hints throughout

- **Frontend** (Work in Progress):
  - Next.js
  - D3 for visualization

## Local Requirements

- Python 3.10+
- Node 18+ (for frontend)
- ~2GB storage for data
- Git LFS (for any large data files)

## Contributing

PRs welcome for:
- Data pipeline improvements
- New analysis approaches
- Frontend visualization ideas

## Data Limitations

- GDELT provides volume and sentiment, but not fact-checking
- World Bank economic data has natural reporting lag
- Some regions have inconsistent coverage
- API reliability can vary

## Notes

- All API responses are cached locally
- Raw data storage is gitignored
- Date range configured in config.py
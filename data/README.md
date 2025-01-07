# pause.map data pipeline

Grabs and processes data from GDELT, Our World in Data and World Bank APIs. Outputs weekly summaries for the frontend.

## Quick start
```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[test]"
```

## Tests
```bash
pytest
```

## Output format
Weekly JSON summaries containing:
- Event counts and sentiment from GDELT
- COVID metrics from OWID
- Economic indicators from World Bank

## Development
Package is set up with:
- pyproject.toml for modern Python packaging
- pytest for testing
- polars for fast data processing
- type hints throughout

## Notes
- BigQuery credentials needed for GDELT access
- World Bank API can be flaky - built in retries
- OWID data updates daily
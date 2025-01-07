# pause.map

Mapping global change through COVID: track how events, sentiment, health and economics shifted during the great pause. Built with GDELT, Our World in Data and World Bank metrics.

## Why this matters
Shows how a global event rippled through media, sentiment and economics. Built to highlight the connections between reporting, public mood and economic reality during an unprecedented pause in normal life.

## What it shows
- Global media sentiment during lockdown
- Event patterns and social shifts
- Economic ripple effects
- Health metrics

## Tech
Two key bits:
1. Python data pipeline
   - Grabs GDELT, OWID and World Bank data
   - Processes into weekly summaries
   - Outputs clean JSON for frontend
2. Next.js frontend
   - D3 for visualisations
   - Shows how events rippled globally
   - Links health, economic and social impact

## Quick start
```bash
make setup   # First time setup
make dev     # Run development environment
```

## Structure
```
pause.map/
  /data           # Python data pipeline
    /src          # Source code
    /tests        # Test suite
    /output       # Generated JSONs
  /site          # Next.js frontend
```

## Contributing
PR for data improvements welcome. Insight suggestions even better.

## Data limitations
- GDELT gives us volume and sentiment, not accuracy
- World Bank economic data lags by ~3 months
- Some regions have patchy coverage

## Local setup needs
- Python 3.10+
- Node 18+
- ~2GB storage for data
# pause.map

Mapping global change through COVID: track how events, sentiment, health and economics shifted during the great pause. Built with GDELT, Our World in Data and World Bank metrics.

## What it shows
- Global media sentiment during lockdown
- Event patterns and social shifts
- Economic ripple effects
- Health metrics

## Tech
- Python data grabber (GDELT + OWID + World Bank)
- Next.js + D3 vis
- Weekly data summaries
- Static site deploy

## Quick start
```bash
make setup   # First time setup
make dev     # Run development environment
```

## Structure
```
pause.map/
  /data           # Python data pipeline
    /scripts      # Data grabbing/processing
    /output      # Generated JSONs
  /site          # Next.js frontend
```

## Data sources
- GDELT: Global events and media sentiment
- Our World in Data: COVID metrics
- World Bank: Economic indicators
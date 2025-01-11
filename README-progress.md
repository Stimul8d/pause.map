# Pause.map Progress Report

## Project Goal
Track how global events, sentiment, and reactions shifted during COVID using GDELT event data. Focus on showing how events rippled through media, sentiment and economics during this unprecedented pause in normal life.

## Current Progress

### Data Structure 
Created clean module structure separating concerns:
```
data/
  storage/
    raw/        # Raw GDELT daily files
    processed/  # Cleaned parquet files
    outputs/    # Weekly summaries for viz
  src/
    pausemap/
      references/
        actors.py      # CAMEO actor type codes
        countries.py   # CAMEO country codes
        events.py      # CAMEO event codes
        locations.py   # FIPS location codes
      config.py        # Project settings
      parse_gdelt.py   # Data processing
```

### Key Files Built

1. Reference Data
- Split all lookup tables into separate modules
- Built proper functions for code translation
- Handle both CAMEO (actors) and FIPS (locations) codes
- Full event category taxonomy

2. Parser (parse_gdelt.py)
- Handles GDELT's tab-separated format
- Fixes date issues (wrong years)
- Translates all codes to human-readable names
- Outputs clean parquet files

### Current Capabilities
- Can download daily GDELT files
- Clean and standardize raw data
- Map codes to readable names
- Track key metrics:
  - Event types and categories
  - Actor involvement 
  - Geographic spread
  - Sentiment (tone scores)

### Gotchas & Fixes
1. Data Formats
- Event codes come as integers, need string padding
- Country codes need different handling for CAMEO vs FIPS
- Dates sometimes have wrong years

2. Polars Issues
- Deprecated dtypes -> schema_overrides
- Return type specification needed for maps
- Column naming conventions in CSV reading

3. Code Lookups
- Need to try different lengths (2-4 digits)
- Fallback for unknown codes
- Careful null handling

### Next Steps
1. Fix display formatting for event descriptions
2. Build weekly summarizer
3. Add data visualizations
4. Test with full COVID timeline

### Key Dates
- Start: Dec 2019 (pre-COVID baseline)
- Focus: March 2020 (lockdowns)
- End: Dec 2021 (post-vaccine rollout)

### Example Data Point (March 23, 2020)
136,674 events showing:
- High diplomatic activity (CONSULT, STATEMENT)
- Many appeals and declarations of intent
- Some mass violence events
- Global geographic spread

## Notes for Continuation
- Keep modular design pattern
- Focus on COVID timeline analysis
- Consider storage/performance for full timeline
- Think about meaningful visualizations
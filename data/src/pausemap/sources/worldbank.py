"""World Bank data handler for economic impacts."""

from typing import Dict, List, Optional
import polars as pl
from pathlib import Path
import requests
import logging
import json
from datetime import datetime

from ..config import RAW_DIR, DATA_DIR, WORLDBANK_URL, START_DATE, END_DATE

logger = logging.getLogger(__name__)

class WorldBankSource:
    """Handles World Bank data related to COVID impact."""
    
    def __init__(self):
        self.raw_dir = RAW_DIR / "worldbank"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Key metrics to track
        self.indicators = {
            "gdp": ["NY.GDP.MKTP.KD.ZG"],  # GDP growth
            "employment": ["SL.UEM.TOTL.ZS"], # Unemployment rate
            "trade": ["NE.TRD.GNFS.ZS"]  # Trade (% of GDP)
        }
        
        # Base URL for indicators API
        self.indicators_url = "https://api.worldbank.org/v2/country/all/indicator"
            
    def fetch_documents(self, target_date: str) -> Path:
        """Get relevant World Bank reports for date."""
        target = self.raw_dir / f"wb_docs_{target_date}.json"
        
        if target.exists():
            logger.info(f"Using cached WB docs for {target_date}")
            return target
            
        # Parameters for document search
        params = {
            "format": "json",
            "qterm": "COVID-19 OR coronavirus OR pandemic",
            "docty": "Report",
            "strdate": target_date,
            "enddate": target_date,
            "fl": ",".join([
                "docdt",
                "display_title", 
                "abstracts"
            ]),
            "rows": 1000
        }
        
        logger.info(f"Fetching WB docs for {target_date}")
        response = requests.get(WORLDBANK_URL, params=params)
        response.raise_for_status()
        
        with open(target, "wb") as f:
            f.write(response.content)
            
        return target

    def _fetch_indicator(self, indicator: str) -> List[Dict]:
        """Fetch data for a single indicator."""
        url = f"{self.indicators_url}/{indicator}"
        
        results = []
        page = 1
        per_page = 1000  # Max out the page size
        
        while True:
            params = {
                "format": "json",
                "date": f"{START_DATE.year}:{END_DATE.year}",
                "per_page": per_page,
                "page": page
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # First element is metadata, second is data
                if len(data) < 2:
                    break
                    
                results.extend(data[1])
                
                # Check if we've got all pages
                if page >= data[0]['pages']:
                    break
                    
                page += 1
                
            except Exception as e:
                logger.error(f"Error fetching {indicator}: {e}")
                break
                
        return results

    def fetch_indicators(self) -> Path:
        """Get World Bank indicators."""
        
        logger.info("Fetching World Bank indicators")
        
        # Fetch each category of indicators
        for category, codes in self.indicators.items():
            target = self.raw_dir / f"wb_{category}_{START_DATE.isoformat()}.json"
            
            if target.exists():
                logger.info(f"Using cached WB {category} data")
                continue
                
            # Get data for each indicator in category
            results = []
            for code in codes:
                data = self._fetch_indicator(code)
                results.extend(data)
                
            with open(target, "w") as f:
                json.dump(results, f)
                
        return self.raw_dir
        
    def get_sample(self) -> None:
        """Get sample of World Bank data structure."""
        # Get sample docs and indicators
        docs_file = self.fetch_documents(START_DATE.isoformat())
        indicators_dir = self.fetch_indicators()
        
        # Build sample from first few results
        with open(docs_file) as f:
            docs = json.load(f)
            
        sample = {
            "metadata": {
                "date": START_DATE.isoformat(),
                "total_documents": len(docs.get("documents", [])),
                "total_indicators": len(self.indicators)
            },
            "document_example": next(iter(docs.get("documents", {}).values()), {}),
            "indicator_categories": list(self.indicators.keys())
        }
        
        # Save sample
        samples_dir = DATA_DIR / "samples"
        samples_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = samples_dir / "worldbank_sample.json"
        with open(output_path, "w") as f:
            json.dump(sample, f, indent=2)
            
        logger.info(f"World Bank sample saved to {output_path}")
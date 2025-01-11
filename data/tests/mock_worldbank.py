from typing import Dict, List
import polars as pl
import requests

class WorldBankSource:
    BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/"
    
    def get_indicators(self, indicator: str, start_year: int, end_year: int) -> pl.DataFrame:
        params = {
            "format": "json",
            "per_page": 1000,
            "date": f"{start_year}:{end_year}"
        }
        
        response = requests.get(f"{self.BASE_URL}{indicator}", params=params)
        data = response.json()
        
        return pl.DataFrame(data[1])
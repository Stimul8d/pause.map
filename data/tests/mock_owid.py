from typing import Dict, List
import polars as pl
import requests

class OWIDSource:
    BASE_URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"
    
    def get_weekly_data(self, start_date: str, end_date: str) -> pl.DataFrame:
        response = requests.get(self.BASE_URL)
        data = response.json()
        
        # Convert to weekly aggregates
        # TODO: Implement proper weekly rollup
        return pl.DataFrame(data)
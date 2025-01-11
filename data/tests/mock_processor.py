from typing import Dict, List
import polars as pl
from datetime import datetime

class DataProcessor:
    def merge_weekly_data(self, gdelt: pl.DataFrame, owid: pl.DataFrame) -> pl.DataFrame:
        """Basic merge for now"""
        return gdelt
    
    def add_economic_data(self, worldbank: pl.DataFrame) -> pl.DataFrame:
        """Just pass through for now"""
        return worldbank
    
    def generate_weekly_summary(self, date: datetime, metrics: Dict) -> Dict:
        """Simple summary"""
        return {
            'date': date.strftime('%Y-%m-%d'),
            'metrics': metrics
        }
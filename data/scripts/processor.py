from typing import Dict, List
import polars as pl
from datetime import datetime

class DataProcessor:
    def merge_weekly_data(self, gdelt: pl.DataFrame, owid: pl.DataFrame) -> pl.DataFrame:
        """Merge GDELT and OWID data on weekly timestamps"""
        return gdelt.join(owid, on='week', how='left')
    
    def add_economic_data(self, worldbank: pl.DataFrame) -> pl.DataFrame:
        """Convert quarterly economic data to weekly, interpolating between points"""
        # TODO: Implement proper interpolation
        return worldbank
    
    def generate_weekly_summary(self, date: datetime, metrics: Dict) -> Dict:
        """Generate a weekly summary for the frontend"""
        return {
            'date': date.strftime('%Y-%m-%d'),
            'metrics': metrics
        }
    
    def process_all(self, gdelt: pl.DataFrame, owid: pl.DataFrame, worldbank: pl.DataFrame) -> List[Dict]:
        """Process all data sources into weekly summaries"""
        weekly_data = self.merge_weekly_data(gdelt, owid)
        weekly_data = self.add_economic_data(worldbank)
        
        summaries = []
        for row in weekly_data.iter_rows(named=True):
            summary = self.generate_weekly_summary(
                row['week'],
                {k: v for k, v in row.items() if k != 'week'}
            )
            summaries.append(summary)
            
        return summaries
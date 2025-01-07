from typing import Dict, List
import polars as pl
from datetime import datetime, timedelta

class GDELTSource:
    def get_mock_data(self, start_date: str, end_date: str) -> pl.DataFrame:
        """Mock data for testing"""
        dates = [
            datetime.strptime(start_date, '%Y-%m-%d') + timedelta(weeks=i) 
            for i in range(52)
        ]
        return pl.DataFrame({
            'week': dates,
            'event_count': [1000 + i * 10 for i in range(52)],
            'tone': [-0.2 + i/100 for i in range(52)]
        })
    
    def get_weekly_data(self, start_date: str, end_date: str) -> pl.DataFrame:
        """Real implementation will use BigQuery"""
        return self.get_mock_data(start_date, end_date)
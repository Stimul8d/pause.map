from typing import Dict, List
import polars as pl
from google.cloud import bigquery

class GDELTSource:
    def __init__(self):
        self.client = bigquery.Client()
    
    def get_weekly_data(self, start_date: str, end_date: str) -> pl.DataFrame:
        query = """
        SELECT 
            DATE_TRUNC(DATE(_PARTITIONTIME), WEEK) as week,
            COUNT(*) as event_count,
            AVG(GoldsteinScale) as impact,
            AVG(AvgTone) as tone
        FROM `gdelt-bq.gdeltv2.events`
        WHERE DATE(_PARTITIONTIME) BETWEEN @start AND @end
        GROUP BY week
        ORDER BY week
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start", "STRING", start_date),
                bigquery.ScalarQueryParameter("end", "STRING", end_date),
            ]
        )
        
        return pl.from_pandas(self.client.query(query, job_config=job_config).to_dataframe())
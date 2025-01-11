"""GDELT data handler with event codes and parsing."""

import requests
import zipfile
import io
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, List
import logging
from tqdm import tqdm

from ..config import RAW_DIR, DATA_DIR, GDELT_URL, START_DATE, END_DATE

logger = logging.getLogger(__name__)

class GDELTSource:
    def __init__(self):
        self.raw_dir = RAW_DIR / "gdelt"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
            
    def fetch_day(self, target_date=None) -> Optional[Path]:
        """Fetch a single day's GDELT export"""
        if target_date is None:
            target_date = START_DATE
            
        date_str = target_date.strftime("%Y%m%d")
        url = GDELT_URL.format(date=date_str)
        zip_path = self.raw_dir / f"{date_str}.export.CSV.zip"
        csv_path = self.raw_dir / f"{date_str}.export.CSV"
        
        if csv_path.exists():
            return csv_path
            
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(zip_path, "wb") as f:
                f.write(response.content)
                
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(self.raw_dir)
                
            zip_path.unlink()
            return csv_path
            
        except Exception as e:
            logger.error(f"Failed to fetch {date_str}: {e}")
            return None
    
    def fetch_range(self) -> List[Path]:
        """Fetch all GDELT exports between START_DATE and END_DATE."""
        current = START_DATE
        days = (END_DATE - START_DATE).days + 1
        
        csvs = []
        with tqdm(total=days, desc="Fetching GDELT data") as pbar:
            while current <= END_DATE:
                csv = self.fetch_day(current)
                if csv:
                    csvs.append(csv)
                current += timedelta(days=1)
                pbar.update(1)
                
        return csvs

    def get_sample(self) -> None:
        """Get sample of GDELT data structure."""
        raw_file = self.fetch_day()
        if not raw_file:
            logger.error("Failed to get sample data")
            return
        
        df = pl.read_csv(
            raw_file,
            separator="\t",
            has_header=False,
            n_rows=1000
        )
        
        event_counts = df["column_26"].value_counts()
        event_codes = {
            str(row['column_26']): int(row['count']) 
            for row in event_counts.to_dicts()
        }
        
        country_counts = df["column_7"].value_counts()
        countries = {
            str(row['column_7']): int(row['count']) 
            for row in country_counts.to_dicts()
        }
        
        sample = {
            "metadata": {
                "date": raw_file.stem[:8],
                "total_columns": len(df.columns),
                "sample_size": 1000
            },
            "columns": {},
            "stats": {
                "event_codes": event_codes,
                "countries": countries,
                "tone": {
                    "count": int(len(df)),
                    "mean": float(df["column_34"].mean()),
                    "std": float(df["column_34"].std())
                }
            }
        }
        
        for i, col in enumerate(df.columns):
            values = df[col].drop_nulls().head(3).to_list()
            if values:
                sample["columns"][f"col_{i}"] = [str(v) for v in values]
        
        samples_dir = DATA_DIR / "samples"
        samples_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = samples_dir / "gdelt_sample.json"
        with open(output_path, "w") as f:
            json.dump(sample, f, indent=2)
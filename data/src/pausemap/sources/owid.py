"""OWID Covid data handler."""

from typing import Dict
import polars as pl
from pathlib import Path
import requests
import logging
import json

from ..config import RAW_DIR, DATA_DIR, OWID_URL, START_DATE, END_DATE

logger = logging.getLogger(__name__)

# All possible fields from metadata
METADATA_FIELDS = {
    "aged_65_older": pl.Float64,
    "aged_70_older": pl.Float64,
    "cardiovasc_death_rate": pl.Float64,
    "continent": pl.Utf8,
    "diabetes_prevalence": pl.Float64,
    "extreme_poverty": pl.Float64,
    "female_smokers": pl.Float64,
    "gdp_per_capita": pl.Float64,
    "handwashing_facilities": pl.Float64,
    "hospital_beds_per_thousand": pl.Float64,
    "human_development_index": pl.Float64,
    "life_expectancy": pl.Float64,
    "location": pl.Utf8,
    "male_smokers": pl.Float64,
    "median_age": pl.Float64,
    "population": pl.Float64,
    "population_density": pl.Float64
}

# All possible metrics from daily data
METRIC_FIELDS = {
    "date": pl.Date,
    "excess_mortality": pl.Float64,
    "excess_mortality_cumulative": pl.Float64,
    "excess_mortality_cumulative_absolute": pl.Float64,
    "excess_mortality_cumulative_per_million": pl.Float64,
    "hosp_patients": pl.Float64,
    "hosp_patients_per_million": pl.Float64,
    "icu_patients": pl.Float64,
    "icu_patients_per_million": pl.Float64,
    "new_cases": pl.Float64,
    "new_cases_per_million": pl.Float64,
    "new_cases_smoothed": pl.Float64,
    "new_cases_smoothed_per_million": pl.Float64,
    "new_deaths": pl.Float64,
    "new_deaths_per_million": pl.Float64,
    "new_deaths_smoothed": pl.Float64,
    "new_deaths_smoothed_per_million": pl.Float64,
    "new_people_vaccinated_smoothed": pl.Float64,
    "new_people_vaccinated_smoothed_per_hundred": pl.Float64,
    "new_tests": pl.Float64,
    "new_tests_per_thousand": pl.Float64,
    "new_tests_smoothed": pl.Float64,
    "new_tests_smoothed_per_thousand": pl.Float64,
    "new_vaccinations": pl.Float64,
    "new_vaccinations_smoothed": pl.Float64,
    "new_vaccinations_smoothed_per_million": pl.Float64,
    "people_fully_vaccinated": pl.Float64,
    "people_fully_vaccinated_per_hundred": pl.Float64,
    "people_vaccinated": pl.Float64,
    "people_vaccinated_per_hundred": pl.Float64,
    "positive_rate": pl.Float64,
    "reproduction_rate": pl.Float64,
    "stringency_index": pl.Float64,
    "tests_per_case": pl.Float64,
    "tests_units": pl.Utf8,
    "total_boosters": pl.Float64,
    "total_boosters_per_hundred": pl.Float64,
    "total_cases": pl.Float64,
    "total_cases_per_million": pl.Float64,
    "total_deaths": pl.Float64,
    "total_deaths_per_million": pl.Float64,
    "total_tests": pl.Float64,
    "total_tests_per_thousand": pl.Float64,
    "total_vaccinations": pl.Float64,
    "total_vaccinations_per_hundred": pl.Float64,
    "weekly_hosp_admissions": pl.Float64,
    "weekly_hosp_admissions_per_million": pl.Float64,
    "weekly_icu_admissions": pl.Float64,
    "weekly_icu_admissions_per_million": pl.Float64
}

class OWIDSource:
    def __init__(self):
        self.raw_dir = RAW_DIR / "owid"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
            
    def fetch_data(self) -> Path:
        """Get OWID dataset."""
        target = self.raw_dir / "owid_covid.json"
        
        if target.exists():
            logger.info("Using cached OWID data")
            return target
            
        logger.info("Fetching fresh OWID data")
        response = requests.get(OWID_URL)
        response.raise_for_status()
        
        with open(target, "wb") as f:
            f.write(response.content)
            
        return target
        
    def process_data(self, input_path: Path) -> Dict[str, pl.DataFrame]:
        """Convert JSON to DataFrames with consistent schema."""
        with open(input_path) as f:
            data = json.load(f)
            
        # Extract country metadata
        metadata_records = []
        for country, details in data.items():
            record = {"country_code": country}
            for field in METADATA_FIELDS:
                record[field] = details.get(field)
            metadata_records.append(record)
            
        metadata_df = pl.DataFrame(
            metadata_records,
            schema={
                "country_code": pl.Utf8,
                **METADATA_FIELDS
            }
        )
        
        # Process daily metrics
        metric_records = []
        for country, details in data.items():
            if details.get("data"):
                for day in details["data"]:
                    record = {"country_code": country}
                    # Keep date as string for now
                    record["date"] = day["date"]
                    # Add all other metrics (will be null if not present)
                    for field in METRIC_FIELDS:
                        if field != "date":  # Skip date as we handled it
                            record[field] = day.get(field)
                    metric_records.append(record)
        
        # Create DataFrame and convert date after
        metrics_df = pl.DataFrame(
            metric_records,
            schema={
                "country_code": pl.Utf8,
                "date": pl.Utf8,
                **{k:v for k,v in METRIC_FIELDS.items() if k != "date"}
            }
        ).with_columns([
            pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")
        ])
        
        # Filter to our date range
        metrics_df = metrics_df.filter(
            (pl.col("date") >= START_DATE) &
            (pl.col("date") <= END_DATE)
        )
        
        # Save both dataframes
        metadata_df.write_parquet(self.raw_dir / "metadata.parquet")
        metrics_df.write_parquet(self.raw_dir / "metrics.parquet")
        
        return {
            "metadata": metadata_df,
            "metrics": metrics_df
        }
        
    def get_sample(self) -> None:
        """Get sample of OWID data structure."""
        raw_file = self.fetch_data()
        with open(raw_file) as f:
            data = json.load(f)
            
        # Get first proper country (not OWID_* aggregate)
        sample_country = next(k for k, v in data.items() 
                            if not k.startswith("OWID_"))
        country_data = data[sample_country]
        
        # Build sample
        sample = {
            "metadata": {
                "date_range": [START_DATE.isoformat(), END_DATE.isoformat()],
                "total_countries": len([k for k in data.keys() 
                                     if not k.startswith("OWID_")]),
                "total_regions": len([k for k in data.keys() 
                                   if k.startswith("OWID_")])
            },
            "country_metadata": {
                field: type(country_data.get(field)).__name__
                for field in METADATA_FIELDS
                if country_data.get(field) is not None
            },
            "metrics": {
                field: METRIC_FIELDS[field].name
                for field in METRIC_FIELDS
            }
        }
        
        # Save sample
        samples_dir = DATA_DIR / "samples"
        samples_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = samples_dir / "owid_sample.json"
        with open(output_path, "w") as f:
            json.dump(sample, f, indent=2)
            
        logger.info(f"OWID sample saved to {output_path}")

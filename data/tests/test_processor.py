import pytest
import polars as pl
from datetime import datetime
from pausemap.processor import DataProcessor

def test_merge_weekly_data(sample_gdelt_data, sample_owid_data):
    processor = DataProcessor()
    merged = processor.merge_weekly_data(sample_gdelt_data, sample_owid_data)
    assert len(merged) > 0  # Basic smoke test

def test_add_economic_indicators(sample_worldbank_data):
    processor = DataProcessor()
    weekly = processor.add_economic_data(sample_worldbank_data)
    assert len(weekly) > 0  # Just check we get something back

def test_generate_summary():
    processor = DataProcessor()
    summary = processor.generate_weekly_summary(
        datetime(2020, 3, 1),
        {'event_count': 1000, 'tone': -0.2}
    )
    assert isinstance(summary, dict)
    assert 'date' in summary
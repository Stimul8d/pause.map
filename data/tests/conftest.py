import pytest
import polars as pl
from datetime import datetime, timedelta

@pytest.fixture
def sample_gdelt_data():
    dates = [datetime(2020, 1, 1) + timedelta(weeks=i) for i in range(52)]
    return pl.DataFrame({
        'week': dates,
        'event_count': [1000 + i * 10 for i in range(52)],
        'impact': [0.5 + i/100 for i in range(52)],
        'tone': [-0.2 + i/100 for i in range(52)]
    })

@pytest.fixture
def sample_owid_data():
    dates = [datetime(2020, 1, 1) + timedelta(weeks=i) for i in range(52)]
    return pl.DataFrame({
        'week': dates,
        'cases': [100 * i for i in range(52)],
        'deaths': [10 * i for i in range(52)],
        'stringency_index': [50 + i/2 for i in range(52)]
    })

@pytest.fixture
def sample_worldbank_data():
    return pl.DataFrame({
        'date': ['2020', '2020', '2021', '2021'],
        'country': ['GB', 'US', 'GB', 'US'],
        'value': [-9.3, -3.4, 7.5, 5.9]
    })
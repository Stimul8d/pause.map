import pytest
from pausemap.sources.gdelt import GDELTSource

def test_gdelt_weekly_processing():
    gdelt = GDELTSource()
    # Using mock data for tests
    df = gdelt.get_weekly_data('2020-01-01', '2020-12-31') 
    
    assert len(df) > 0
    assert 'week' in df.columns
    assert 'event_count' in df.columns
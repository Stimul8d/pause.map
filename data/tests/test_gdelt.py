import pytest
from pausemap.sources.gdelt import GDELTSource

def test_gdelt_weekly_processing(mocker):
    # We'll just assert we can get data without BigQuery for now
    gdelt = GDELTSource()
    result = gdelt.get_mock_data('2020-01-01', '2020-12-31')
    
    assert len(result) > 0
    assert 'week' in result.columns
    assert 'event_count' in result.columns
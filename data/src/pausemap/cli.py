"""Command line interface for pause.map data pipeline."""

import click
import logging

from pausemap.sources.gdelt import GDELTSource
from pausemap.sources.owid import OWIDSource
from pausemap.sources.worldbank import WorldBankSource 
from pausemap.config import DATA_DIR, START_DATE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """Data pipeline for pause.map"""
    pass

@cli.command()
@click.option("--source", type=click.Choice(["gdelt", "owid", "worldbank"]), default="gdelt", 
              help="Data source to sample")
def sample(source: str):
    """Get sample data from a source."""
    if source == "gdelt":
        gdelt = GDELTSource()
        gdelt.get_sample()
    elif source == "owid":
        owid = OWIDSource()
        owid.get_sample()
    elif source == "worldbank":
        wb = WorldBankSource()
        wb.get_sample()

@cli.command()
@click.option("--source", type=click.Choice(["gdelt", "owid", "worldbank"]), default="gdelt",
              help="Data source to fetch")
def fetch(source: str):
    """Fetch full dataset for date range in config."""
    if source == "gdelt":
        gdelt = GDELTSource()
        csvs = gdelt.fetch_range()
        logger.info(f"Downloaded {len(csvs)} GDELT files")
    elif source == "owid":
        owid = OWIDSource()
        data_file = owid.fetch_data()
        owid.process_data(data_file)
        logger.info("Processed OWID data")
    elif source == "worldbank":
        wb = WorldBankSource()
        docs = wb.fetch_documents(START_DATE.isoformat())
        wb.fetch_indicators()
        logger.info("Downloaded World Bank data")
        
if __name__ == "__main__":
    cli()
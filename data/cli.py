#!/usr/bin/env python3
"""Command line interface for pause.map data pipeline."""

import click
from pathlib import Path
from pausemap.sources.gdelt import GDELTSource
from pausemap.sources.owid import OWIDSource
from pausemap.sources.worldbank import WorldBankSource

@click.group()
def cli():
    """Manage pause.map data pipeline."""
    pass

@cli.command()
@click.option('--storage', type=click.Path(), default='storage',
              help='Storage directory for data files')
def fetch_all(storage):
    """Fetch data from all sources."""
    storage_path = Path(storage)
    
    # GDELT
    gdelt = GDELTSource(storage_path)
    gdelt.fetch_data()
    
    # OWID
    owid = OWIDSource(storage_path)
    owid.fetch_data()
    
    # World Bank
    wb = WorldBankSource(storage_path)
    wb.fetch_reports('2020-01-01', '2024-12-31')

@cli.command()
@click.option('--storage', type=click.Path(), default='storage',
              help='Storage directory for data files')
def process_all(storage):
    """Process raw data from all sources."""
    storage_path = Path(storage)
    
    # Process each source
    # TODO: Implement processing logic for each source
    pass

if __name__ == '__main__':
    cli()
from datetime import datetime
import polars as pl
from sources.gdelt import GDELTSource
from sources.owid import OWIDSource
from sources.worldbank import WorldBankSource

START_DATE = "2019-01-01"
END_DATE = "2023-12-31"

def main():
    gdelt = GDELTSource()
    owid = OWIDSource()
    wb = WorldBankSource()
    
    # Grab all data
    gdelt_data = gdelt.get_weekly_data(START_DATE, END_DATE)
    covid_data = owid.get_weekly_data(START_DATE, END_DATE)
    economic_data = wb.get_indicators("NY.GDP.MKTP.KD.ZG", 2019, 2023)
    
    # TODO: Merge and process
    # TODO: Save to output/

if __name__ == "__main__":
    main()
"""
ETF Scraper - Core Engine

This module contains the main scraping pipeline for ETF data extraction.

It orchestrates the full workflow:
- Input parsing (ISIN list + column schema)
- Web page loading via Selenium
- HTML parsing via BeautifulSoup
- Structured extraction using SiteConfig rules
- Normalization and enrichment
- DataFrame creation and export

This is the central entry point used by run_scraper.py.

WARNING:
This module is not intended to be called directly by end users.
Use run_scraper.py instead.
"""

import logging
import pandas as pd
from etf_scraper.io import FileReader, FileWriter
from etf_scraper.engine.soup_extractor import SoupDataExtractor
from etf_scraper.engine.soup_factory import WebDriverSoupFactory

logger = logging.getLogger( __name__ )

def scrape_etfs( input_path: str, output_path: str, use_input_format = False, override_input = False ):
    """
    Executes the full ETF scraping pipeline.

    Reads ISINs from input file, scrapes ETF data from the configured website,
    and exports the results into a structured DataFrame.

    Args:
        input_path (str): Path to the input file containing ISINs and columns.
        output_path (str): Path where the output file will be written.
        use_input_format (bool): If True, reuses Excel formatting from input file.
        override_input (bool): If True and input == output, overwrites file instead of copying.

    Returns:
        pandas.DataFrame: Final dataset containing all scraped ETF data.
    """
    input_info = FileReader.read( input_path )
    isins = input_info[ "isins" ]
    columns = input_info[ "columns" ]
    data = []

    with WebDriverSoupFactory( columns = columns ) as factory:
        for n_isin, isin in enumerate(isins, 1):
            logger.info( "Scraping ISIN %s / %s: %s", n_isin, len( isins ), isin )

            # Initialise isin_data
            isin_data = { column: None for column in columns }
            isin_data[ "ISIN" ] = isin

            # Charge the website
            soup = factory.get_soup( isin )

            # Fill the row
            page_scraper = SoupDataExtractor( isin_data, soup )
            page_scraper.fill_info()

            # Add to data
            data.append( page_scraper.isin_data )

    df = pd.DataFrame( data, columns = columns )
    FileWriter.write( df, output_path, use_input_format, input_path, override_input )
    
    return df
"""
ETF Scraper - Execution Script

This is the main entry point of the application.

The only purpose of this script is to launch the ETF scraping pipeline
using the configuration defined in `user_config.py`.

All scraping behavior (input files, output files, browser settings,
target website, etc.) is controlled exclusively via `user_config.py`.

This script should NOT be modified in normal usage.


Usage
-----
Simply run:

    python run_scraper.py

or:

    python3 run_scraper.py

    
Dependencies
-----------
- etf_scraper (core package)
- user_config.py (user-defined settings)


Notes
-----
- This is the only executable script intended for end users.
- All customization must be done in `user_config.py`.
- No scraping logic is implemented here; this file only orchestrates execution.
"""

from etf_scraper import scrape_etfs
from user_config import path, input_file, output_file, use_input_format, override_input
import logging

logging.basicConfig( level = logging.INFO, format = "%(message)s" )

scrape_etfs( path + input_file, path + output_file, use_input_format, override_input )
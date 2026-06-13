"""
ETF Scraper package.

This package provides a configurable framework to scrape ETF data
from financial websites using ISIN identifiers.

Main entry point:
    scrape_etfs (engine.scraper)
"""


from etf_scraper.engine import scrape_etfs

__all__ = [ "scrape_etfs" ]
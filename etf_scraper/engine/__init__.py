"""
Engine module for ETF Scraper.

This module contains the core scraping pipeline responsible for:
- loading input data
- orchestrating web scraping
- extracting structured information
- exporting results

It exposes the main scraping function used by the package.
"""

from etf_scraper.engine.scraper import scrape_etfs

__all__ = [ "scrape_etfs" ]
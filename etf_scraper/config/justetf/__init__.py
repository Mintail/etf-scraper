"""
JustETF configuration module.

This module defines the complete scraping configuration for JustETF,
including:
- DOM paths
- section definitions
- converters
- normalizers
- special enrichment rules

It is registered in the global configuration registry.
"""

from etf_scraper.config.justetf.registry import config

__all__ = [ "config" ]
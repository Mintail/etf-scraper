"""
Configuration registry for ETF Scraper.

This module provides access to all supported website configurations.

It acts as a central registry used to retrieve:
- site-specific DOM paths
- extractors
- converters
- normalizers
- special processing rules

Main entry point:
    get_config(site: str)
"""

from etf_scraper.config.justetf import config as config_justetf
from etf_scraper.config.site_config import SiteConfig, Section

_CONFIGS = {
    "justetf": config_justetf,
}

def get_config(site: str) -> SiteConfig:
    try:
        return _CONFIGS[ site.lower() ]
    except KeyError:
        raise ValueError(
            f"Unknown site: {site}. "
            f"Available Sites: {', '.join(_CONFIGS.keys())}."
        )

__all__ = [
    "Section",
    "get_config"
]
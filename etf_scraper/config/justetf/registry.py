"""
JustETF site registry configuration.

This module acts as the composition layer of the scraping pipeline.

It wires together all independent components:
- DOM navigation (paths)
- HTML extraction (extractors)
- label mapping (converters)
- data normalization (normalizers)
- post-processing rules (special_adds)

The scraping logic is section-driven.

Each Section represents a logical block of the website
(e.g. Basics, Performance, Risk) and defines:
- where to find the section in the DOM
- how to extract data from it
- how to map labels to internal fields

The resulting SiteConfig is consumed by the scraping engine.

columns_to_fill defines a reference set of possible output columns.

The configuration supports dual-language initialization (EN/FR):
init_fr triggers a preliminary load of the French version
to enable region-specific features (e.g. PEA eligibility).
"""

from itertools import chain

from etf_scraper.config.site_config import Section, SiteConfig

from etf_scraper.config.justetf.converters import (
    header_converter,
    overview_converter,
    basics_converter,
    performance_converter,
    risk_converter,
    stock_exchange_converter
)

from etf_scraper.config.justetf.paths import (
    isin_path_css_selector,
    isin_path,
    loading_check_paths,
    header_path,
    overview_path,
    basics_path,
    performance_path,
    risk_path,
    stock_exchange_path
)

from etf_scraper.config.justetf.extractors import (
    header_extractor,
    overview_extractor,
    stock_exchange_extractor,
    table_extractor
)

from etf_scraper.config.justetf.normalizers import (
    normalize_price,
    normalize_percentage,
    normalize_fund_size,
    normalize_replication,
    normalize_date_of_price,
    normalize_investment_focus
)

from etf_scraper.config.justetf.special_adds import add_region_asset_type


sections = (
    Section( "Basics", basics_path, table_extractor, basics_converter ),
    Section( "Overview", overview_path, overview_extractor, overview_converter ),
    Section( "Header", header_path, header_extractor, header_converter ),
    Section( "Stock exchange", stock_exchange_path, stock_exchange_extractor, stock_exchange_converter ),
    Section( "Performance", performance_path, table_extractor, performance_converter ),
    Section( "Risk", risk_path, table_extractor, risk_converter ),
)

normalizers = {
    "Date of Price"     : normalize_date_of_price,
    "Fund size"         : normalize_fund_size,
    "Investment focus"  : normalize_investment_focus,
    "Perf Current Year" : normalize_percentage,
    "Perf 1 month"      : normalize_percentage,
    "Perf 3 months"     : normalize_percentage,
    "Perf 6 months"     : normalize_percentage,
    "Perf 1 year"       : normalize_percentage,
    "Perf 3 years"      : normalize_percentage,
    "Perf 5 years"      : normalize_percentage,
    "Price"             : normalize_price,
    "Replication"       : normalize_replication,
    "TER"               : normalize_percentage,
    "Vol 1 year"        : normalize_percentage,
    "Vol 3 years"       : normalize_percentage,
    "Vol 5 years"       : normalize_percentage,
}

special_adds = {
    "Investment focus": add_region_asset_type,
}

website = "https://www.justetf.com/en/etf-profile.html?isin="

columns_to_fill = tuple( dict.fromkeys( # to avoid duplication of Index + keep the order
    [ "ISIN", "Index", "Region", "Asset Type" ]
    + list( chain.from_iterable( section.converter.values() for section in sections ) )
) )

def init_fr( columns: list ) -> bool:
    return "PEA eligible" in columns

config = SiteConfig(
    website = website,
    columns_to_fill = columns_to_fill,
    sections = sections,
    normalizers = normalizers,
    special_adds = special_adds,
    isin_path = isin_path,
    isin_path_css_selector = isin_path_css_selector,
    loading_check_paths = loading_check_paths,
    init_fr = init_fr,
    website_fr = website.split( "en" )[ 0 ] + "fr",
)
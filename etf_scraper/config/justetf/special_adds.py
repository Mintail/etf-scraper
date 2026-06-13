"""
Special post-processing rules for ETF data.

This module applies cross-field transformations that cannot
be handled by simple normalization, such as:
- deriving region classification
- extracting asset type categories
- enriching structured fields from raw text
"""

import logging

logger = logging.getLogger( __name__ )

valid_regions = {
    "Asia Pacifique",
    "Broad Market",
    "China",
    "Emerging Markets",
    "Europe",
    "France",
    "Japan",
    "United Kingdom",
    "United States",
    "World",
}

valid_asset_types = {
    "Bonds",
    "Commodities",
    "Cryptocurrencies",
    "Equity",
    "Precious Metals"
}

def add_region_asset_type( value: str, isin_data: dict ):
    """
    Enriches ISIN data by extracting region and asset type from a raw comma-separated string.
    """

    areas = [ v.strip() for v in value.split( "," ) ]
    
    # Intersect parsed values with known valid region / asset type sets
    regions     = set( areas ).intersection( valid_regions )
    asset_types = set( areas ).intersection( valid_asset_types )
    
    # Intersect parsed values with known valid region / asset type sets
    if "Region" in isin_data:
        regions = "\n".join( regions )
        isin_data[ "Region" ] = regions
        logger.debug( "Set %s = %s", "Region", regions )
    
    # Update Region field if present in output schema
    if "Asset Type" in isin_data:
        asset_types = "\n".join( asset_types )
        isin_data[ "Asset Type" ] = asset_types
        logger.debug( "Set %s = %s", "Asset Type", asset_types )

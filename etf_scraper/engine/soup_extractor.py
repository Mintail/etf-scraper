"""
SoupDataExtractor module.

This module provides a class to extract structured data from BeautifulSoup objects
representing financial instrument pages. It fills a dictionary with ISIN-related
information based on pre-defined sections and labels, supporting both English and French.

Classes:
    SoupDataExtractor: Extracts and normalizes ISIN data from parsed HTML pages.

Usage:
    extractor = SoupDataExtractor( soup, isin_data = None )
    extractor.fill_info()
    data = extractor.isin_data
"""

import logging
from bs4 import BeautifulSoup
from etf_scraper.config import get_config, Section
from user_config import WEBSITE

logger = logging.getLogger( __name__ )


class SoupDataExtractor:
    """
    Extract and normalize financial instrument data from a BeautifulSoup object.

    Attributes:
        soup (BeautifulSoup): Parsed HTML page.
        isin_data (dict): Dictionary of ISIN-related fields to fill.
    """

    def __init__( self, isin_data: dict, soup: BeautifulSoup ):
        """
        Initialize the extractor with a BeautifulSoup object, ISIN info dictionary.

        Args:
            soup (BeautifulSoup): Parsed HTML page.
            isin_data (dict): Dictionary of fields to populate.
        """
        self.soup      = soup
        self.isin_data = isin_data

    def fill_info( self ) -> None:
        """
        Populate the ISIN info dictionary by processing all configured sections.
        """
        if not self.soup:
            logger.warning( "No soup provided for extraction." )
            return

        sections = get_config( WEBSITE ).sections
        for section in sections:
            self._fill_info_section( section )

    def _fill_info_section( self, section: Section ) -> None:
        """
        Process a single section and update the ISIN info dictionary.
        """
        subsection = section.path( self.soup )
        if not subsection:
            logger.debug( "Section '%s' not found", section.name )
            return
        extract_map = section.final_extractor( subsection )
        for label, value in extract_map.items():
            self._set_field_value( section.converter.get( label ), value )


    def _set_field_value( self, entry: str | None, value: str ):
        """
        Update the entry isin_data with value.
        """
        if not entry:
            return
        
        value = value.replace( "®" , "" )
        config = get_config( WEBSITE )

        normalizer = config.normalizers.get( entry )
        normalized = normalizer( value ) if normalizer else value
        self.isin_data[ entry ] = normalized
        logger.debug( "Set %s = %s", entry, normalized )
        
        special_add = config.special_adds.get( entry )
        if special_add:
            special_add( value, self.isin_data )
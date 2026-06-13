"""
HTML extraction layer for JustETF.

Defines section-specific parsing functions that convert
BeautifulSoup nodes into structured key-value dictionaries.

Each extractor is responsible for one logical section of the page.
"""

from bs4 import BeautifulSoup
from etf_scraper.config.site_config import FinalExtractor

def parse_header( subsoup: BeautifulSoup ) -> dict[str,str]:
    """
    Extracts PEA eligibility flag from the header section
    """
    line = subsoup.find( "span", string = lambda t: t and t.strip() == "PEA eligible" )
    return { "PEA eligible": "Yes" if line else "No" }


def parse_overview( subsection: BeautifulSoup ) -> dict[str,str]:
    """
    Extracts currency, price, and price date from the overview quote section.
    """
    extract_map = {}
    val_div = subsection.find_next( "div", class_ = "val" )
    if not val_div:
        return {}

    spans = val_div.find_all( "span" )
    if len( spans ) >= 2:
        extract_map[ "Currency" ] = spans[0].get_text( strip = True )
        extract_map[ "Price" ] = spans[1].get_text( strip = True )

    date_label = subsection.find_next( "div", class_ = "vallabel" )
    if date_label:
        extract_map[ "Date of Price" ] = date_label.get_text( strip = True )

    return extract_map


def parse_stock_exchange( table: BeautifulSoup ) -> dict[str,str]:
    """
    Extracts all stock exchange listings into a newline-separated string.
    """
    rows = table.find_all( "tr" )[ 1: ]
    values = [ r.find( "td" ).get_text( strip = True ) for r in rows if r.find( "td" ) ]
    return { "Stock exchange": "\n".join( values ) }


def parse_table( table: BeautifulSoup ) -> dict[str,str]:
    """
    Generic key-value table extractor for structured ETF data sections.
    """
    extract_map = {}
    rows = table.find_all( "tr" )
    for row in rows:
        label_td = row.find( "td", class_= "vallabel" )
        if not label_td:
            continue
        label    = label_td.get_text( strip = True )
        value_td = label_td.find_next_sibling( "td" )
        value    = value_td.get_text( strip = True ) if value_td else ""
        extract_map[ label ] = value
    
    return extract_map

header_extractor         = FinalExtractor( "Header Extractor", parse_header )
overview_extractor       = FinalExtractor( "Overview Extractor", parse_overview )
stock_exchange_extractor = FinalExtractor( "Stock exchange Extractor", parse_stock_exchange )
table_extractor          = FinalExtractor( "Table Extractor", parse_table )
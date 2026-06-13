"""
DOM path definitions for JustETF scraping.

This module defines all navigation rules used to locate
relevant sections within the HTML structure.

Paths are built using DOMPath to ensure readable and
maintainable DOM traversal logic.

Each path represents an anchor point in the DOM used to
locate a logical section of the ETF page.

These paths are tightly coupled to the current DOM structure
of the JustETF website and may break if the HTML layout changes.

Both DOMPath and CSS selectors are used:
- DOMPath: preferred structured navigation approach
- CSS selector: fallback / alternative lookup method

loading_check_paths defines DOM markers used to determine
whether the page has fully loaded before extraction.
"""

from etf_scraper.config.dompath import DOMPath

isin_path_css_selector = "div.e_head div.identfier span:contains('ISIN') + span"

isin_path = (
    DOMPath()
        .find( "div", class_ = "e_head" )
        .find( "div", class_ = "identfier" )
        .find( "span", string = lambda t: t and t.strip() == "ISIN" )
        .find_next_sibling( "span" )
)

loading_check_paths = [
    DOMPath()
        .find( "div", id = "shadow-nav" )
]

header_path = (
    DOMPath()
        .find( "div", class_ = "e_head" )
        .find_next_sibling( "div" )
)

overview_path = (
    DOMPath()
        .find( "h2", string = lambda t: t and t.strip() == "Overview" )
        .find_next( "h3", string = lambda t: t and t.strip() == "Quote" )
)

basics_path = (
    DOMPath()
        .find( "h2", string = lambda t: t and t.strip() == "Basics" )
        .find_next( "h3", string = lambda t: t and t.strip() == "Data" )
        .find_next( "table" )
)

performance_path = (
    DOMPath()
        .find( "h2", string = lambda t: t and t.strip() == "Performance" )
        .find_next( "h3", class_ = "clearfix" )
        .validate( lambda element: element.find( "span" ).get_text( strip = True ) == "Returns overview" )
        #.validate( lambda element: element.find( text = True, recursive = False ).strip() == "Returns overview" ) # Old version of the website
        .find_next( "table" )
)

risk_path = (
    DOMPath()
        .find( "h2", string = lambda t: t and t.strip() == "Risk" )
        .find_next( "h3", string = lambda t: t and t.strip() == "Risk overview" )
        .find_next( "table" )
)

stock_exchange_path = (
    DOMPath()
        .find( "h2", string = lambda t: t and t.strip() == "Stock exchange" )
        .find_next( "h3", string = lambda t: t and t.strip() == "Listings" )
        .find_next( "table" )
)
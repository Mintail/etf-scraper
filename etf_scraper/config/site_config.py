"""
Site configuration module.

This module defines the data model used to configure scraping behavior
for a given website.

It provides a declarative structure describing:
- page sections to extract
- DOM navigation rules
- field mappings (converters)
- normalization logic
- special post-processing rules

This allows the scraping engine to remain fully generic while supporting
multiple websites with different HTML structures.
"""

from bs4 import BeautifulSoup
from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, TypeAlias

from etf_scraper.config.dompath import DOMPath

ExtractorFn: TypeAlias = Callable[ [BeautifulSoup], dict[str, str] ]


@dataclass( frozen = True )
class FinalExtractor:
    """
    Wrapper around a section-specific extraction function.

    Executes a BeautifulSoup parsing function and returns structured data.

    Attributes:
        name (str): Name of the extractor (debugging / logging purpose).
        extractor (Callable): Function converting BeautifulSoup to dict.
    """
    name: str
    extractor: ExtractorFn
       
    def __call__( self, soup: BeautifulSoup ) -> dict[str, str]:
        return self.extractor( soup )


@dataclass( frozen = True )
class Section:
    """
    Defines a logical extraction unit within a webpage.

    A section describes:
    - where to find data in the DOM
    - how to extract it
    - how to map raw labels to canonical fields

    Attributes:
        name (str): Section identifier.
        path (DOMPath): DOM navigation rule to locate the section.
        final_extractor (FinalExtractor): HTML → structured data extractor.
        converter (MappingProxyType): Mapping from raw labels to field names.
    """
    name: str
    path: DOMPath
    final_extractor: FinalExtractor
    converter: MappingProxyType


def default_init_fr( columns: list | None = None ) -> bool:
    """
    Default initialization hook for French version detection.
    False by default.
    """
    return False

@dataclass( frozen = True )
class SiteConfig:
    """
    Defines the full scraping configuration for a website.

    This object centralizes all rules required to extract structured data
    from a specific site, making the scraper fully modular.

    Attributes:
        website (str): Base URL of the website.
        sections (tuple[Section]): Ordered list of page sections to extract.
        normalizers (dict[str, Callable]): Field-level data cleaning functions.
        special_adds (dict[str, Callable]): Cross-field enrichment logic.
        columns_to_fill (list[str]): Final output schema (DataFrame columns).
        isin_path (DOMPath): DOM path used to verify ISIN presence.
        isin_path_css_selector (str): Alternative CSS selector for ISIN check.
        loading_check_paths (DOMPath): Paths used to validate page load.
        init_fr (Callable): Optional French initialization hook.
        website_fr (str): French version of the base URL.
    """
    website: str
    columns_to_fill: list[str]
    sections: tuple[Section]
    normalizers: dict[str,Callable]
    special_adds: dict[str,Callable]
    isin_path: DOMPath
    isin_path_css_selector: str
    loading_check_paths: DOMPath
    init_fr: Callable = default_init_fr
    website_fr: str = ""
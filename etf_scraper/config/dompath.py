"""
DOMPath module.

This module provides a declarative and chainable system to navigate
and filter BeautifulSoup elements in a structured and reusable way.

It acts as a lightweight DSL over BeautifulSoup to:
- locate elements step by step
- apply validation rules at each step
- safely fail on missing or invalid nodes

Main classes:
    DOMPath: Chainable path builder and executor
    DOMPathStep: Single navigation + validation step
    ExtractorStep: Executes BeautifulSoup search methods
    ValidatorStep: Applies optional validation logic
"""

import logging
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Callable, Tuple


logger = logging.getLogger( __name__ )

@dataclass( frozen = True )
class ExtractorStep:
    """
    Executes a BeautifulSoup search method on a given element.

    Attributes:
        method (str): BeautifulSoup method name (e.g. 'find', 'find_next').
        attributes (dict): Arguments passed to the BeautifulSoup method.
    """
    method: str
    attributes: dict

    def __call__( self, soup: BeautifulSoup ) -> BeautifulSoup | None:
        return getattr( soup, self.method )( **self.attributes )


@dataclass( frozen = True )
class ValidatorStep:
    """
    Applies an optional validation function on a BeautifulSoup element.

    Attributes:
        validator (Callable | None): Function returning True if element is valid.
    """
    validator: Callable | None = None

    def __call__( self, soup: BeautifulSoup ) -> bool:
        if not self.validator:
            return True
        return self.validator( soup )


@dataclass( frozen = True )
class DOMPathStep:
    """
    Combines extraction and validation for a single navigation step.

    Executes a BeautifulSoup lookup and validates the result before returning it.

    Attributes:
        extractor (ExtractorStep): Element extraction logic.
        validator (ValidatorStep): Validation logic applied to extracted element.
    """
    extractor: ExtractorStep
    validator: ValidatorStep
    
    def __call__( self, soup: BeautifulSoup ) -> BeautifulSoup | None:
        element = self.extractor( soup )
        return element if element and self.validator( element ) else None


@dataclass( frozen = True )
class DOMPath:
    """
    Chainable path builder for BeautifulSoup navigation.

    Each step defines:
    - how to locate an element
    - optional validation of the result

    The path is executed sequentially until:
    - the target element is found, or
    - a step fails (returns None)

    Attributes:
        steps (Tuple[DOMPathStep, ...]): Ordered navigation steps.
    """
    steps: Tuple[DOMPathStep, ...] = ()

    def _add_step( self, method: str, attributes: dict, validator: Callable | None = None ):
        """
        Adds a new navigation step to the DOM path.
        """
        return DOMPath( self.steps + ( DOMPathStep( ExtractorStep( method, attributes ), ValidatorStep( validator ) ), ) )

    def __getattr__( self, method: str ):
        """
        Dynamically maps BeautifulSoup methods into chainable DOMPath calls.
        """
        def wrapper( *args, **kwargs ):
            attributes = {}
            if args:
                attributes[ "name" ] = args[ 0 ]
            attributes.update( kwargs )
            return self._add_step( method, attributes )
        return wrapper

    def validate( self, validator: Callable ):
        """
        Adds a validation function to the last step of the path.
        """
        if not self.steps:
            raise ValueError( "Cannot add validator to empty path." )
        new_steps = self.steps[:-1] + (
            DOMPathStep( self.steps[ -1 ].extractor, ValidatorStep( validator ) ),
        )
        return DOMPath( new_steps )

    def __call__( self, soup: BeautifulSoup ):
        """
        Executes the full DOM path on a BeautifulSoup object.
        """
        element = soup
        for i, step in enumerate( self.steps, 1 ):
            element = step( element )
            if not element:
                logger.debug( f"Step {i} failed: {step.extractor.method} {step.extractor.attributes}" )
                return None
        return element


"""
WebDriverSoupFactory module.

This module provides a factory class to load web pages for financial instruments
identified by ISINs using Selenium WebDriver and parse them into BeautifulSoup objects.

Classes:
    WebDriverSoupFactory: Handles browser setup, page loading with retries, and ISIN verification.

Usage:
    with WebDriverSoupFactory( browser = "chrome", headless = True) as factory:
        soup = factory.get_soup( "IE00BD8KRH84" )
"""

import os
import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

from etf_scraper.config import get_config
from user_config import WEBSITE, BROWSER, HEADLESS, LOAD_TIMEOUT, LOAD_WAIT, RETRY_DELAYS


logger = logging.getLogger( __name__ )
os.environ[ "SE_AVOID_BROWSER_DOWNLOAD" ] = "true" # avoid downloading browser in cache if browser not installed by user
os.environ[ "SE_SKIP_DRIVER_IN_PATH" ] = "true" # force creating a new browser driver instead of using the driver in cache

class WebDriverSoupFactory:
    """
    Factory to create BeautifulSoup objects from web pages using Selenium WebDriver.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance.
        browser (str): Browser name.
        headless (bool): Whether to run the browser in headless mode (not available for Safari).
        load_timeout (int): Maximum page load time in seconds.
        load_wait (int): Time to wait after page load in seconds.
        retry_delays (tuple[int]): Wait times between retry attempts.
    """

    def __init__(
        self,
        browser: str = BROWSER,
        columns: list = [],
        headless: bool = HEADLESS,
        load_timeout: int = LOAD_TIMEOUT,
        load_wait: int = LOAD_WAIT,
        retry_delays: tuple = RETRY_DELAYS,
    ):
        """
        Initialize the factory and start a Selenium WebDriver session.

        Args:
            browser (str): Browser to use ("Chrome", "Firefox", "Safari").
            headless (bool): Run browser in headless mode.
            load_timeout (int): Page load timeout in seconds.
            load_wait (int): Delay to wait after loading page.
            retry_delays (tuple[int]): Delays between retry attempts.
        
        Raises:
            ValueError: If the specified browser is unsupported.
        """
        self.browser      = browser
        self.load_timeout = load_timeout
        self.headless     = headless
        self.load_wait    = load_wait
        self.retry_delays = retry_delays
        self.init_fr      = get_config( WEBSITE ).init_fr( columns )

        self.driver = self._create_driver()
        self.driver.set_page_load_timeout( self.load_timeout )

    def __enter__( self ):
        if self.init_fr:
            self._load_webpage( init_fr = True )
        return self

    def __exit__( self, exc_type, exc_value, traceback ):
        self.close()

    def _create_driver( self ) -> webdriver:
        """
        Create a Selenium WebDriver instance based on the selected browser.
        Options are adjusted depending on headless mode and environment.
        """
        def _build_driver( browser_name: str, headless: bool ) -> webdriver:
            """Internal helper to create a driver with proper options and flags."""
            browser_name = browser_name.lower().strip()
            if browser_name == "chrome":
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument( "--headless=new" )
                    options.add_argument( "--disable-gpu" )
                    options.add_argument( "--no-sandbox" )
                    options.add_argument( "--disable-dev-shm-usage" )
                return webdriver.Chrome( options = options )

            elif browser_name == "firefox":
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument( "--headless" )
                return webdriver.Firefox( options = options )

            elif browser_name == "safari":
                if headless:
                    logger.warning( "Safari does not support headless mode: ignoring 'headless=True'." )
                return webdriver.Safari()

            else:
                raise ValueError(
                    f"Browser '{browser_name}' is not supported. "
                    "Please use 'Safari', 'Firefox', or 'Chrome'."
                )

        # Try to build the driver and log errors
        try:
            driver = _build_driver(self.browser, self.headless)
            logger.info( "%s WebDriver successfully created.", self.browser.capitalize() )
            return driver
        except WebDriverException as e:
            logger.error( "Failed to start %s WebDriver: %s", self.browser.capitalize(), e )
            raise WebDriverException( f"Impossible to find {self.browser.capitalize()}." )

    def close( self ):
        """
        Close the WebDriver session and release resources.
        """
        if self.driver:
            self.driver.quit()
            logger.info( "WebDriver closed." )

    def get_soup( self, isin: str ) -> BeautifulSoup | None:
        """
        Load web page from WEBSITE and return the parsed HTML.

        Args:
            isin (str): ISIN identifier of the financial instrument.

        Returns:
            BeautifulSoup: Parsed HTML soup.
                           Returns empty soup and "en" if not found.
        """
        soup = self._load_webpage( isin )
        if soup and WebDriverSoupFactory._has_isin( soup, isin ):
            return soup
        logger.warning( "The website does not have ISIN %s.", isin )

        return None

    def _load_webpage( self, isin: str = "", init_fr: bool = False ) -> BeautifulSoup | None:
        """
        Load and parse a web page for a given ISIN with retries.
        """
        if init_fr:
            url = get_config( WEBSITE ).website_fr
            website_str = "fr website"
            logger.warning( "Loading French version of the website to ensure PEA box appears in future loads." )
        else:
            url = get_config( WEBSITE ).website + isin
            website_str = f"website for ISIN {isin}"
        website_str_cap = website_str[0].upper() + website_str[1:]
        
        n_tries = len( self.retry_delays )
        for attempt in range( n_tries ):
            if attempt > 0:
                wait = self.retry_delays[ attempt - 1 ]
                logger.warning( "%s not loaded. Try %s/%s. Waiting %s seconds.", website_str_cap, attempt, n_tries, wait )
                time.sleep( wait )
            try:
                self.driver.get( url )
                time.sleep( self.load_wait )
            except TimeoutException:
                logger.warning( "Timeout loading %s.", website_str )

            soup = BeautifulSoup( self.driver.page_source, "html.parser" )
            if self._is_loaded( soup ):
                if attempt > 0:
                    logger.info( "%s successfully loaded after %s attempts.", website_str_cap, attempt + 1 )
                return soup

        logger.warning( "Failed to fully load %s.", website_str )
        return None

    @staticmethod
    def _is_loaded( soup: BeautifulSoup ) -> bool:
        """
        Return True if the page contains content and is considered loaded.
        """
        is_loaded = True
        loading_check_paths = get_config( WEBSITE ).loading_check_paths
        for path in loading_check_paths:
            is_loaded = is_loaded and ( path( soup ) is not None )
        return is_loaded

    @staticmethod
    def _has_isin( soup: BeautifulSoup, isin: str ) -> bool:
        """
        Return True if the ISIN is found in the parsed HTML.
        """
        value_span = get_config( WEBSITE ).isin_path( soup )
        return value_span and value_span.get_text( strip = True ) == isin

    @staticmethod
    def _has_isin_css_selector( soup: BeautifulSoup, isin: str ) -> bool:
        """
        Return True if the ISIN is found in the parsed HTML.
        Same as _has_isin but using a more elegant but less robust way.
        Not in use.
        """
        selector   = get_config( WEBSITE ).isin_path_css_selector
        value_span = soup.select_one( selector )
        return value_span and value_span.get_text( strip = True ) == isin
    
    

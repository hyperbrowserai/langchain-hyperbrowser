from typing import Optional, Union, Dict, Any
from langchain_core.tools import BaseTool
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser
from hyperbrowser.models.crawl import StartCrawlJobParams
from hyperbrowser.models.scrape import ScrapeOptions
from hyperbrowser.models.session import CreateSessionParams
from pydantic import BaseModel, Field, SecretStr, model_validator

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

from langchain_hyperbrowser.common import SimpleSessionParams, SimpleScrapeOptions

from ._utilities import initialize_client


class CrawlArgs(BaseModel):
    url: str = Field(description="The URL to scrape data from")
    max_pages: Optional[int] = Field(default=None)
    scrape_options: Optional[SimpleScrapeOptions] = Field(
        default=None, description="Optional parameters for scraping configuration"
    )
    session_options: Optional[SimpleSessionParams] = Field(
        default=None, description="Optional parameters for the browser session"
    )


class HyperbrowserCrawlTool(BaseTool):
    name: str = "hyperbrowser_crawl_data"
    description: str = (
        """Crawl a website starting from a given URL.
    Provide a URL and optionally configure crawling options like max pages and scraping settings.
    Returns the crawled content from all pages in markdown or HTML format along with metadata."""
    )
    client: Hyperbrowser = Field(default=None)  # type: ignore
    async_client: AsyncHyperbrowser = Field(default=None)  # type: ignore
    api_key: SecretStr = Field(default=None)  # type: ignore
    args_schema: type[CrawlArgs] = CrawlArgs

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate the environment."""
        values = initialize_client(values)
        return values

    def _run(
        self,
        url: str,
        max_pages: Optional[int] = None,
        scrape_options: Optional[SimpleScrapeOptions] = None,
        session_options: Optional[SimpleSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Crawl a website starting from a given URL.

        Args:
            url: The URL to start crawling from
            max_pages: Optional maximum number of pages to crawl
            scrape_options: Optional parameters for scraping configuration
            session_options: Optional parameters for the browser session
            run_manager: Optional callback manager for the tool run

        Returns:
            Dict containing the crawled content and metadata from all pages
        """
        # Create crawl job parameters
        crawl_params = StartCrawlJobParams(
            url=url,
            max_pages=max_pages,
            scrape_options=(
                ScrapeOptions(formats=scrape_options.formats)
                if scrape_options
                else None
            ),
            session_options=(
                CreateSessionParams(
                    use_proxy=session_options.use_proxy,
                    proxy_country=session_options.proxy_country,
                    solve_captchas=session_options.solve_captchas,
                    adblock=session_options.adblock,
                )
                if session_options is not None
                else None
            ),
        )

        # Start and wait for crawl job
        response = self.client.crawl.start_and_wait(crawl_params)

        return {"data": response.data, "error": response.error}

    async def _arun(
        self,
        url: str,
        max_pages: Optional[int] = None,
        scrape_options: Optional[SimpleScrapeOptions] = None,
        session_options: Optional[SimpleSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Asynchronously crawl a website starting from a given URL.

        Args:
            url: The URL to start crawling from
            max_pages: Optional maximum number of pages to crawl
            scrape_options: Optional parameters for scraping configuration
            session_options: Optional parameters for the browser session
            run_manager: Optional callback manager for the tool run

        Returns:
            Dict containing the crawled content and metadata from all pages
        """
        # Create crawl job parameters
        crawl_params = StartCrawlJobParams(
            url=url,
            max_pages=max_pages,
            scrape_options=(
                ScrapeOptions(formats=scrape_options.formats)
                if scrape_options
                else None
            ),
            session_options=(
                CreateSessionParams(
                    use_proxy=session_options.use_proxy,
                    proxy_country=session_options.proxy_country,
                    solve_captchas=session_options.solve_captchas,
                    adblock=session_options.adblock,
                )
                if session_options is not None
                else None
            ),
        )

        # Start and wait for crawl job
        response = await self.async_client.crawl.start_and_wait(crawl_params)

        return {"data": response.data, "error": response.error}

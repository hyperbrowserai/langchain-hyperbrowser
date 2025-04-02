from typing import Optional, Union, Dict, Any
from langchain_core.tools import BaseTool
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser
from hyperbrowser.models.scrape import StartScrapeJobParams, ScrapeOptions
from hyperbrowser.models.session import CreateSessionParams
from pydantic import BaseModel, Field, SecretStr, model_validator

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

from langchain_hyperbrowser.common import SimpleSessionParams, SimpleScrapeOptions

from ._utilities import initialize_client


class ScrapeArgs(BaseModel):
    url: str = Field(description="The URL to scrape data from")
    scrape_options: Optional[SimpleScrapeOptions] = Field(
        default=None, description="Optional parameters for scraping configuration"
    )
    session_options: Optional[SimpleSessionParams] = Field(
        default=None, description="Optional parameters for the browser session"
    )


class HyperbrowserScrapeTool(BaseTool):
    name: str = "hyperbrowser_scrape_data"
    description: str = (
        """Scrape content from a webpage.
    Provide a URL and optionally configure scraping options.
    Returns the scraped content in markdown or HTML format along with metadata."""
    )
    client: Hyperbrowser = Field(default=None)  # type: ignore
    async_client: AsyncHyperbrowser = Field(default=None)  # type: ignore
    api_key: SecretStr = Field(default=None)  # type: ignore
    args_schema: type[ScrapeArgs] = ScrapeArgs

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate the environment."""
        values = initialize_client(values)
        return values

    def _run(
        self,
        url: str,
        scrape_options: Optional[SimpleScrapeOptions] = None,
        session_options: Optional[SimpleSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Scrape content from a webpage.

        Args:
            url: The URL to scrape data from
            scrape_options: Optional parameters for scraping configuration
            session_options: Optional parameters for the browser session
            run_manager: Optional callback manager for the tool run

        Returns:
            Dict containing the scraped content and metadata
        """
        # Create scrape job parameters
        scrape_params = StartScrapeJobParams(
            url=url,
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
                if session_options
                else None
            ),
        )

        # Start and wait for scrape job
        response = self.client.scrape.start_and_wait(scrape_params)

        return {"data": response.data, "error": response.error}

    async def _arun(
        self,
        url: str,
        scrape_options: Optional[SimpleScrapeOptions] = None,
        session_options: Optional[SimpleSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Asynchronously scrape content from a webpage.

        Args:
            url: The URL to scrape data from
            scrape_options: Optional parameters for scraping configuration
            session_options: Optional parameters for the browser session
            run_manager: Optional callback manager for the tool run

        Returns:
            Dict containing the scraped content and metadata
        """
        # Create scrape job parameters
        scrape_params = StartScrapeJobParams(
            url=url,
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
                if session_options
                else None
            ),
        )

        # Start and wait for scrape job
        response = await self.async_client.scrape.start_and_wait(scrape_params)

        return {"data": response.data, "error": response.error}

"""Hyperbrowser document loader."""

from typing import AsyncIterator, Iterator, Literal, Optional, Sequence, Union

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_core.utils import get_from_env
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser
from hyperbrowser.models.scrape import (
    StartScrapeJobParams,
    ScrapeOptions,
    ScrapeJobData,
)
from hyperbrowser.models.crawl import StartCrawlJobParams
from hyperbrowser.models.session import CreateSessionParams


class HyperbrowserLoader(BaseLoader):
    """
    Hyperbrowser document loader integration

    Setup:
        Get your API Key from https://app.hyperbrowser.ai/
        Install ``langchain-hyperbrowser`` and set environment variable ``HYPERBROWSER_API_KEY``.

        .. code-block:: bash

            pip install -U langchain-hyperbrowser
            export HYPERBROWSER_API_KEY="your-api-key"

    Instantiate:
        .. code-block:: python

            from langchain_hyperbrowser import HyperbrowserLoader

            loader = HyperbrowserLoader(
                urls="https://example.com",
                operation="scrape",
                # other params = ...
            )

    Lazy load:
        .. code-block:: python

            docs = []
            docs_lazy = loader.lazy_load()

            # async variant:
            # docs_lazy = await loader.alazy_load()

            for doc in docs_lazy:
                docs.append(doc)
            print(docs[0].page_content[:100])
            print(docs[0].metadata)

        .. code-block:: python

            page_content='Example Domain

            # Example Domain

            This domain is for use in illustrative examples in documents. You may use this
            domain in literature without prior coordination or asking for permission.

            [More information...](https://www.iana.org/domains/example)' metadata={'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}

    Async load:
        .. code-block:: python

            docs = await loader.aload()
            print(docs[0].page_content[:100])
            print(docs[0].metadata)

        .. code-block:: python

            page_content='Example Domain

            # Example Domain

            This domain is for use in illustrative examples in documents. You may use this
            domain in literature without prior coordination or asking for permission.

            [More information...](https://www.iana.org/domains/example)' metadata={'title': 'Example Domain', 'viewport': 'width=device-width, initial-scale=1', 'sourceURL': 'https://example.com'}
    """  # noqa: E501

    def __init__(
        self,
        urls: Union[str, Sequence[str]],
        api_key: Optional[str] = None,
        operation: Literal["scrape", "crawl"] = "scrape",
        params: Optional[dict] = None,
    ):
        """Initialize with API Key, operation, urls to scrape, and optional params.
        For full documentation, visit https://docs.hyperbrowser.ai

        Args:
            urls: URL(s) to scrape or crawl.
            api_key: Hyperbrowser API key.
            operation: Operation to perform, either "scrape" or "crawl".
            params: Optional params for scrape or crawl. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait
        """
        self.api_key = api_key or get_from_env(
            "HYPERBROWSER_API_KEY", env_key="HYPERBROWSER_API_KEY"
        )
        if not self.api_key:
            raise ValueError(
                "HYPERBROWSER_API_KEY environment variable not set and no API key provided"
            )

        self.operation = operation
        self.params = params or {}

        if operation == "crawl":
            if isinstance(urls, str):
                self.urls = [urls]
            else:
                if len(urls) > 1:
                    raise ValueError("Crawl operation can only accept a single URL")
                self.urls = [urls[0]]
        else:
            if isinstance(urls, str):
                self.urls = [urls]
            else:
                self.urls = urls

        if "scrape_options" in self.params:
            if "formats" in self.params["scrape_options"]:
                formats = self.params["scrape_options"]["formats"]
                if not all(fmt in ["markdown", "html"] for fmt in formats):
                    raise ValueError("formats can only contain 'markdown' or 'html'")

        self.hyperbrowser = Hyperbrowser(api_key=api_key)
        self.async_hyperbrowser = AsyncHyperbrowser(api_key=api_key)

    def _prepare_params(self):
        """Prepare session and scrape options parameters."""
        if "session_options" in self.params:
            self.params["session_options"] = CreateSessionParams(
                **self.params["session_options"]
            )
        if "scrape_options" in self.params:
            self.params["scrape_options"] = ScrapeOptions(
                **self.params["scrape_options"]
            )

    def _create_document(self, content: str, metadata: dict) -> Document:
        """Create a Document with content and metadata."""
        return Document(page_content=content, metadata=metadata)

    def _extract_content_metadata(self, data: Union[ScrapeJobData, None]):
        """Extract content and metadata from response data."""
        content = ""
        metadata = {}
        if data:
            content = data.markdown or data.html or ""
            if data.metadata:
                metadata = data.metadata
        return content, metadata

    def lazy_load(self) -> Iterator[Document]:
        self._prepare_params()

        if self.operation == "scrape":
            for url in self.urls:
                scrape_params = StartScrapeJobParams(url=url, **self.params)
                scrape_resp = self.hyperbrowser.scrape.start_and_wait(scrape_params)
                content, metadata = self._extract_content_metadata(scrape_resp.data)
                yield self._create_document(content, metadata)
        else:
            crawl_params = StartCrawlJobParams(url=self.urls[0], **self.params)
            crawl_resp = self.hyperbrowser.crawl.start_and_wait(crawl_params)
            for page in crawl_resp.data:
                content = page.markdown or page.html or ""
                yield self._create_document(content, page.metadata or {})

    async def alazy_load(self) -> AsyncIterator[Document]:
        self._prepare_params()

        if self.operation == "scrape":
            for url in self.urls:
                scrape_params = StartScrapeJobParams(url=url, **self.params)
                scrape_resp = await self.async_hyperbrowser.scrape.start_and_wait(
                    scrape_params
                )
                content, metadata = self._extract_content_metadata(scrape_resp.data)
                yield self._create_document(content, metadata)
        else:
            crawl_params = StartCrawlJobParams(url=self.urls[0], **self.params)
            crawl_resp = await self.async_hyperbrowser.crawl.start_and_wait(
                crawl_params
            )
            for page in crawl_resp.data:
                content = page.markdown or page.html or ""
                yield self._create_document(content, page.metadata or {})

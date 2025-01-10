"""Integration tests for HyperbrowserLoader."""

import os
import pytest
from langchain_hyperbrowser.hyperbrowser import HyperbrowserLoader


@pytest.mark.skipif(
    not os.getenv("HYPERBROWSER_API_KEY"),
    reason="HYPERBROWSER_API_KEY environment variable not set",
)
class TestHyperbrowserLoaderIntegration:
    """Integration tests for HyperbrowserLoader."""

    def test_scrape_single_url(self):
        """Test scraping a single URL."""
        loader = HyperbrowserLoader(urls="https://example.com", operation="scrape")
        docs = list(loader.lazy_load())

        assert len(docs) > 0
        assert docs[0].page_content
        assert docs[0].metadata
        assert "sourceURL" in docs[0].metadata

    def test_scrape_multiple_urls(self):
        """Test scraping multiple URLs."""
        urls = ["https://example.com", "https://example.org"]
        loader = HyperbrowserLoader(urls=urls, operation="scrape")
        docs = list(loader.lazy_load())

        assert len(docs) == 2
        for doc in docs:
            assert doc.page_content
            assert doc.metadata
            assert "sourceURL" in doc.metadata

    @pytest.mark.asyncio
    async def test_async_scrape(self):
        """Test async scraping."""
        loader = HyperbrowserLoader(urls="https://example.com", operation="scrape")
        docs = []
        async for doc in loader.alazy_load():
            docs.append(doc)

        assert len(docs) > 0
        assert docs[0].page_content
        assert docs[0].metadata

    def test_crawl_operation(self):
        """Test crawl operation."""
        loader = HyperbrowserLoader(
            urls="https://example.com",
            operation="crawl",
            params={"max_pages": 2, "scrape_options": {"formats": ["markdown"]}},
        )
        docs = list(loader.lazy_load())

        assert len(docs) > 0
        for doc in docs:
            assert doc.page_content
            assert doc.metadata

    @pytest.mark.asyncio
    async def test_async_crawl(self):
        """Test async crawling."""
        loader = HyperbrowserLoader(
            urls="https://example.com",
            operation="crawl",
            params={"max_pages": 2, "scrape_options": {"formats": ["markdown"]}},
        )
        docs = []
        async for doc in loader.alazy_load():
            docs.append(doc)

        assert len(docs) > 0
        for doc in docs:
            assert doc.page_content
            assert doc.metadata

    def test_custom_scrape_options(self):
        """Test scraping with custom options."""
        loader = HyperbrowserLoader(
            urls="https://example.com",
            operation="scrape",
            params={"scrape_options": {"include_tags": ["a"]}},
        )
        docs = list(loader.lazy_load())

        assert len(docs) > 0
        assert docs[0].page_content
        assert docs[0].metadata

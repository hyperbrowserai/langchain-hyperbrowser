"""Unit tests for HyperbrowserLoader."""

import pytest
from unittest.mock import Mock, patch
from langchain_hyperbrowser.hyperbrowser_loader import HyperbrowserLoader
from hyperbrowser.models.scrape import ScrapeJobData


@pytest.fixture
def mock_hyperbrowser():
    with patch("langchain_hyperbrowser.hyperbrowser.Hyperbrowser") as mock:
        yield mock


@pytest.fixture
def mock_async_hyperbrowser():
    with patch("langchain_hyperbrowser.hyperbrowser.AsyncHyperbrowser") as mock:
        yield mock


def test_init_with_single_url():
    """Test initialization with a single URL."""
    loader = HyperbrowserLoader(
        urls="https://example.com", api_key="test-key", operation="scrape"
    )
    assert loader.urls == ["https://example.com"]
    assert loader.api_key == "test-key"
    assert loader.operation == "scrape"


def test_init_with_multiple_urls():
    """Test initialization with multiple URLs."""
    urls = ["https://example1.com", "https://example2.com"]
    loader = HyperbrowserLoader(urls=urls, api_key="test-key", operation="scrape")
    assert loader.urls == urls


def test_init_crawl_multiple_urls():
    """Test that crawl operation with multiple URLs raises ValueError."""
    urls = ["https://example1.com", "https://example2.com"]
    with pytest.raises(
        ValueError, match="Crawl operation can only accept a single URL"
    ):
        HyperbrowserLoader(urls=urls, api_key="test-key", operation="crawl")


def test_invalid_format_option():
    """Test that invalid format option raises ValueError."""
    with pytest.raises(
        ValueError, match="formats can only contain 'markdown' or 'html'"
    ):
        HyperbrowserLoader(
            urls="https://example.com",
            api_key="test-key",
            params={"scrape_options": {"formats": ["invalid"]}},
        )


def test_lazy_load_scrape(mock_hyperbrowser):
    """Test sync lazy loading with scrape operation."""
    mock_response = Mock()
    mock_response.data = ScrapeJobData(
        markdown="# Test Content", metadata={"title": "Test"}
    )
    mock_instance = mock_hyperbrowser.return_value
    mock_instance.scrape.start_and_wait.return_value = mock_response

    loader = HyperbrowserLoader(urls="https://example.com", api_key="test-key")

    docs = list(loader.lazy_load())

    assert len(docs) == 1
    assert docs[0].page_content == "# Test Content"
    assert docs[0].metadata == {"title": "Test"}


def test_prepare_params():
    """Test parameter preparation."""
    loader = HyperbrowserLoader(
        urls="https://example.com",
        api_key="test-key",
        params={
            "session_options": {"timeout": 30},
            "scrape_options": {"formats": ["markdown"]},
        },
    )

    loader._prepare_params()
    assert "session_options" in loader.params
    assert "scrape_options" in loader.params

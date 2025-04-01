"""Unit tests for extract tool."""

import pytest
from unittest.mock import Mock, patch
from langchain_hyperbrowser.extract_tool import HyperbrowserExtractTool


@pytest.fixture
def mock_hyperbrowser():
    with patch("langchain_hyperbrowser.extract_tool.Hyperbrowser") as mock:
        yield mock


@pytest.fixture
def mock_async_hyperbrowser():
    with patch("langchain_hyperbrowser.extract_tool.AsyncHyperbrowser") as mock:
        yield mock


def test_extract_tool_creation():
    """Test the extract tool creation."""
    tool = HyperbrowserExtractTool()
    assert tool.name == "hyperbrowser_extract_data"
    assert "Extract structured data from a webpage using AI" in tool.description


def test_extract_tool_run(mock_hyperbrowser):
    """Test synchronous run of the extract tool."""
    mock_response = Mock()
    mock_response.data = {"name": "Test Product", "price": "$10"}
    mock_response.error = None

    mock_instance = mock_hyperbrowser.return_value
    mock_instance.extract.start_and_wait.return_value = mock_response

    tool = HyperbrowserExtractTool()
    result = tool._run(
        url="https://dummyjson.com/products?limit=10",
        extraction_prompt="Extract product info",
        json_schema=None,
    )

    assert result["data"] == {"name": "Test Product", "price": "$10"}
    assert result["error"] is None


@pytest.mark.asyncio
async def test_extract_tool_arun(mock_async_hyperbrowser):
    """Test asynchronous run of the extract tool."""
    mock_response = Mock()
    mock_response.data = {"name": "Test Product", "price": "$10"}
    mock_response.error = None

    mock_instance = mock_async_hyperbrowser.return_value
    mock_instance.extract.start_and_wait.return_value = mock_response

    tool = HyperbrowserExtractTool()
    result = await tool._arun(
        url="https://dummyjson.com/products?limit=10",
        extraction_prompt="Extract product info",
        json_schema=None,
    )

    assert result["data"] == {"name": "Test Product", "price": "$10"}
    assert result["error"] is None


def test_extract_tool_with_schema():
    """Test the extract tool with a Pydantic schema."""
    from pydantic import BaseModel
    from typing import List

    class ProductSchema(BaseModel):
        title: str
        price: float

    class ProductsSchema(BaseModel):
        products: List[ProductSchema]

    tool = HyperbrowserExtractTool()
    result = tool.run(
        {
            "url": "https://dummyjson.com/products?limit=10",
            "extraction_prompt": "Extract product info",
            "json_schema": ProductsSchema,
            "session_options": {"use_proxy": True},
        }
    )

    assert isinstance(result, dict)
    assert "data" in result
    assert result["data"] is not None
    assert "error" in result
    assert result["error"] is None

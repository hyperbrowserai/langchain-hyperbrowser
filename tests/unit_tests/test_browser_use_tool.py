"""Unit tests for browser use tool."""

import pytest
from unittest.mock import Mock, patch
from langchain_hyperbrowser.browser_use_tool import HyperbrowserBrowserUseTool


@pytest.fixture
def mock_hyperbrowser():
    with patch("langchain_hyperbrowser.browser_use_tool.Hyperbrowser") as mock:
        yield mock


@pytest.fixture
def mock_async_hyperbrowser():
    with patch("langchain_hyperbrowser.browser_use_tool.AsyncHyperbrowser") as mock:
        yield mock


def test_browser_use_tool_creation():
    """Test the browser use tool creation."""
    tool = HyperbrowserBrowserUseTool()
    assert tool.name == "hyperbrowser_browser_use"
    assert "Execute a task using a browser agent" in tool.description


def test_browser_use_tool_sync(mock_hyperbrowser):
    """Test synchronous browser use tool execution."""
    mock_response = Mock()
    mock_response.data = Mock(final_result="Here are the top 5 posts...")
    mock_response.error = None

    mock_instance = mock_hyperbrowser.return_value
    mock_instance.agents.browser_use.start_and_wait.return_value = mock_response

    tool = HyperbrowserBrowserUseTool()
    result = tool._run(
        task="go to Hacker News and summarize the top 5 posts",
        validate_output=True,
        use_vision=True,
        max_actions_per_step=5,
    )

    assert result["data"] == "Here are the top 5 posts..."
    assert result["error"] is None


@pytest.mark.asyncio
async def test_browser_use_tool_async(mock_async_hyperbrowser):
    """Test asynchronous browser use tool execution."""
    mock_response = Mock()
    mock_response.data = Mock(final_result="Here are the top 5 posts...")
    mock_response.error = None

    mock_instance = mock_async_hyperbrowser.return_value
    mock_instance.agents.browser_use.start_and_wait.return_value = mock_response

    tool = HyperbrowserBrowserUseTool()
    result = await tool._arun(
        task="go to Hacker News and summarize the top 5 posts",
        validate_output=True,
        use_vision=True,
        max_actions_per_step=5,
    )

    assert result["data"] == "Here are the top 5 posts..."
    assert result["error"] is None


def test_browser_use_tool_with_all_params():
    """Test the browser use tool with all available parameters."""
    tool = HyperbrowserBrowserUseTool()
    result = tool._run(
        task="go to Hacker News and summarize the top 5 posts right now",
        validate_output=True,
        use_vision=True,
        use_vision_for_planner=True,
        max_actions_per_step=5,
        max_input_tokens=1000,
        planner_interval=1000,
        max_steps=10,
        keep_browser_open=True,
    )

    assert isinstance(result, dict)
    assert "data" in result
    assert "error" in result
    assert result["error"] is None

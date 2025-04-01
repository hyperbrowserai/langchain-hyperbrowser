from importlib import metadata

from langchain_hyperbrowser.hyperbrowser_loader import HyperbrowserLoader
from langchain_hyperbrowser.extract_tool import HyperbrowserExtractTool
from langchain_hyperbrowser.browser_use_tool import HyperbrowserBrowserUseTool
from langchain_hyperbrowser.claude_computer_use_tool import (
    HyperbrowserClaudeComputerUseTool,
)
from langchain_hyperbrowser.openai_cua_tool import HyperbrowserOpenAICUATool

try:
    __version__ = metadata.version(__package__ or "langchain_hyperbrowser")
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "HyperbrowserLoader",
    "HyperbrowserExtractTool",
    "HyperbrowserBrowserUseTool",
    "HyperbrowserClaudeComputerUseTool",
    "HyperbrowserOpenAICUATool",
    "__version__",
]

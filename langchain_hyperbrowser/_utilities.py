import os
from typing import Dict

from hyperbrowser import ClientConfig, Hyperbrowser, AsyncHyperbrowser  # type: ignore
from langchain_core.utils import convert_to_secret_str


def initialize_client(values: Dict) -> Dict:
    """Initialize the client."""
    api_key = values.get("api_key") or os.environ.get("HYPERBROWSER_API_KEY") or ""
    values["api_key"] = convert_to_secret_str(api_key)
    args = {
        "api_key": values["api_key"].get_secret_value(),
    }
    values["client"] = Hyperbrowser(ClientConfig(**args))
    values["async_client"] = AsyncHyperbrowser(ClientConfig(**args))

    return values

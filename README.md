# langchain-hyperbrowser

This package contains the LangChain integration with Hyperbrowser

## Installation

```bash
pip install -U langchain-hyperbrowser
```

And you should configure credentials by setting the following environment variables:

`HYPERBROWSER_API_KEY=<your-api-key>`

Make sure to get your API Key from https://app.hyperbrowser.ai/

## Document Loaders

`HyperbrowserLoader` class exposes document loaders from Hyperbrowser.

```python
from langchain_hyperbrowser import HyperbrowserLoader

loader = HyperbrowserLoader(urls="https://www.google.com")
docs = loader.load()
```

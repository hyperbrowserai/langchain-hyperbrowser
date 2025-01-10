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

## Usage

```python
from langchain_hyperbrowser import HyperbrowserLoader

loader = HyperbrowserLoader(urls="https://example.com")
docs = loader.load()

print(docs[0])
```

## Advanced Usage

You can specify the operation to be performed by the loader. The default operation is `scrape`. For `scrape`, you can provide a single URL or a list of URLs to be scraped. For `crawl`, you can only provide a single URL. The `crawl` operation will crawl the provided page and subpages and return a document for each page.

```python
loader = HyperbrowserLoader(
  urls="https://hyperbrowser.ai", api_key="YOUR_API_KEY", operation="crawl"
)
```

Optional params for the loader can also be provided in the `params` argument. For more information on the supported params, visit https://docs.hyperbrowser.ai/reference/sdks/python/scrape#start-scrape-job-and-wait or https://docs.hyperbrowser.ai/reference/sdks/python/crawl#start-crawl-job-and-wait.

```python
loader = HyperbrowserLoader(
  urls="https://example.com",
  api_key="YOUR_API_KEY",
  operation="scrape",
  params={"scrape_options": {"include_tags": ["h1", "h2", "p"]}}
)
```
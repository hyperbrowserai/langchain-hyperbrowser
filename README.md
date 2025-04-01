# langchain-hyperbrowser

This package contains the LangChain integration with Hyperbrowser

## Overview

[Hyperbrowser](https://hyperbrowser.ai) is a platform for running and scaling headless browsers. It lets you launch and manage browser sessions at scale and provides easy to use solutions for any webscraping needs, such as scraping a single page or crawling an entire site.

Key Features:
- Instant Scalability - Spin up hundreds of browser sessions in seconds without infrastructure headaches
- Simple Integration - Works seamlessly with popular tools like Puppeteer and Playwright
- Powerful APIs - Easy to use APIs for scraping/crawling any site, and much more
- Bypass Anti-Bot Measures - Built-in stealth mode, ad blocking, automatic CAPTCHA solving, and rotating proxies

For more information about Hyperbrowser, please visit the [Hyperbrowser website](https://hyperbrowser.ai) or if you want to check out the docs, you can visit the [Hyperbrowser docs](https://docs.hyperbrowser.ai).

## Installation and Setup

To get started with `langchain-hyperbrowser`, you can install the package using pip:

```bash
pip install langchain-hyperbrowser
```

And you should configure credentials by setting the following environment variables:

`HYPERBROWSER_API_KEY=<your-api-key>`

Make sure to get your API Key from https://app.hyperbrowser.ai/

## Document Loaders

The package provides two main document loaders:

### HyperbrowserLoader

The `HyperbrowserLoader` class can be used to load content from any single page or multiple pages. The content can be loaded as markdown or html.

```python
from langchain_hyperbrowser import HyperbrowserLoader

loader = HyperbrowserLoader(urls="https://example.com")
docs = loader.load()

print(docs[0])
```

## Tools

### Extract Tool

The `HyperbrowserExtractTool` can be used to extract structured data from web pages using AI. You can provide a prompt describing what data to extract or a Pydantic model/JSON schema for structured extraction.

```python
from langchain_hyperbrowser import HyperbrowserExtractTool
from pydantic import BaseModel
from typing import List

class ProductSchema(BaseModel):
    name: str
    price: str
    features: List[str]

# Use the tool directly
tool = HyperbrowserExtractTool()
result = tool.run({
    "url": "https://example.com/product",
    "prompt": "Extract the product name, price, and key features",
    "schema": ProductSchema,  # Optional
    "session_options": {
        "solve_captchas": True
    }
})

# Or use it in an agent
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, [tool], verbose=True)
agent_executor = AgentExecutor(agent=agent, tools=[tool], verbose=True)

result = agent_executor.invoke({
    "input": "Extract product information from https://example.com/product"
})
```

### Browser Use Tool

The `HyperbrowserBrowserUseTool` allows you to execute tasks using a browser agent that can navigate websites, interact with elements, and extract information. This is perfect for complex web automation tasks.

```python
from langchain_hyperbrowser import HyperbrowserBrowserUseTool

# Use the tool directly
tool = HyperbrowserBrowserUseTool()
result = tool.run(
    task="go to Hacker News and summarize the top 5 posts of the day",
    session_options={
        "accept_cookies": True
    }
)

# Or use it in an agent
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, [tool], verbose=True)
agent_executor = AgentExecutor(agent=agent, tools=[tool], verbose=True)

result = agent_executor.invoke({
    "input": "Go to example.com, click the login button, and tell me what fields are required"
})
```

The browser use tool supports various configuration options:
- `task`: The task to execute using the browser agent
- `llm`: The language model to use for generating actions
- `session_id`: Optional session ID to reuse an existing browser session
- `validate_output`: Whether to validate the agent's output format
- `use_vision`: Whether to use visual analysis for better context
- `use_vision_for_planner`: Whether to use vision for the planner component
- `max_actions_per_step`: Maximum actions per step
- `max_input_tokens`: Maximum token limit for inputs
- `planner_llm`: Language model for planning future actions
- `page_extraction_llm`: Language model for extracting structured data
- `planner_interval`: How often the planner runs
- `max_steps`: Maximum number of steps
- `keep_browser_open`: Whether to keep the browser session open
- `session_options`: Browser session configuration

### Claude Computer Use Tool

The `HyperbrowserClaudeComputerUseTool` leverages Claude's computer use capabilities through Hyperbrowser. It allows Claude to interact with web pages and perform complex tasks using natural language instructions.

```python
from langchain_hyperbrowser import HyperbrowserClaudeComputerUseTool

# Use the tool directly
tool = HyperbrowserClaudeComputerUseTool()
result = tool.run(
    task="Go to example.com and extract the contact information",
    max_failures=3,
    max_steps=20
)

# Or use it in an agent
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, [tool], verbose=True)
agent_executor = AgentExecutor(agent=agent, tools=[tool], verbose=True)

result = agent_executor.invoke({
    "input": "Go to example.com and find the contact information"
})
```

### OpenAI CUA Tool

The `HyperbrowserOpenAICUATool` leverages OpenAI's Computer Use Agent (CUA) capabilities through Hyperbrowser. It allows the agent to interact with web pages and perform complex tasks using natural language instructions.

```python
from langchain_hyperbrowser import HyperbrowserOpenAICUATool

# Use the tool directly
tool = HyperbrowserOpenAICUATool()
result = tool.run(
    task="Go to example.com and extract the contact information",
    max_failures=3,
    max_steps=20
)

# Or use it in an agent
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
agent = create_openai_functions_agent(llm, [tool], verbose=True)
agent_executor = AgentExecutor(agent=agent, tools=[tool], verbose=True)

result = agent_executor.invoke({
    "input": "Go to example.com and find the contact information"
})
```

## Advanced Usage

All tools support both synchronous and asynchronous usage:

```python
# Synchronous usage
result = tool.run(task="your task")

# Asynchronous usage
result = await tool.arun(task="your task")
```

You can also provide various options for the tools through their respective parameters. For more information on the supported parameters, visit:
- [Browser Use API Reference](https://docs.hyperbrowser.ai/reference/api-reference/agents/browser-use)
- [Claude Computer Use API Reference](https://docs.hyperbrowser.ai/reference/api-reference/agents/claude-computer-use)
- [OpenAI CUA API Reference](https://docs.hyperbrowser.ai/reference/api-reference/agents/openai-cua)
- [Extract API Reference](https://docs.hyperbrowser.ai/reference/api-reference/extract)

## Additional Resources

- [Hyperbrowser](https://hyperbrowser.ai)
- [Hyperbrowser Python SDK](https://github.com/hyperbrowserai/python-sdk)
- [Hyperbrowser Docs](https://docs.hyperbrowser.ai/)

"""Hyperbrowser browser use tool."""

from typing import Optional, Dict, Any
from langchain_core.tools import BaseTool
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser
from hyperbrowser.models import (
    StartBrowserUseTaskParams,
    BrowserUseLlm,
    CreateSessionParams,
)
from pydantic import BaseModel, Field, SecretStr, model_validator

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

from langchain_hyperbrowser.common import SimpleSessionParams

from ._utilities import initialize_client


class BrowserUseArgs(BaseModel):
    task: str = Field()
    max_input_tokens: Optional[int] = Field(default=None)
    max_steps: Optional[int] = Field(default=None)
    session_options: Optional[SimpleSessionParams] = Field(default=None)


class HyperbrowserBrowserUseTool(BaseTool):
    """Tool for executing tasks using a browser agent."""

    name: str = "hyperbrowser_browser_use"
    description: str = (
        """Execute a task using a browser agent. This specific tool uses browser-use.
    The agent can navigate websites, interact with elements, and extract information.
    Provide a task description and optionally configure the agent's behavior.
    Returns the task result and metadata."""
    )
    client: Hyperbrowser = Field(default=None)  # type: ignore
    async_client: AsyncHyperbrowser = Field(default=None)  # type: ignore
    api_key: SecretStr = Field(default=None)  # type: ignore
    args_schema: type[BrowserUseArgs] = BrowserUseArgs

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate the environment."""
        values = initialize_client(values)
        return values

    def _run(
        self,
        task: str,
        max_steps: Optional[int] = None,
        session_options: Optional[SimpleSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Execute a task using a browser agent.

        Args:
            task: The task to execute (e.g. "go to Hacker News and summarize the top 5 posts")
            use_vision: Optional flag to enable vision capabilities for the agent
            max_input_tokens: Optional limit on the number of input tokens
            max_steps: Optional maximum number of steps to execute
            session_options: Optional parameters for browser session configuration

        Returns:
            Dict containing the task result and metadata with keys 'data' and 'error'
        """

        # Create browser use task parameters
        task_params = StartBrowserUseTaskParams(
            task=task,
            use_vision=True,
            max_steps=max_steps,
            session_options=(
                CreateSessionParams(
                    use_proxy=session_options.use_proxy,
                    proxy_country=session_options.proxy_country,
                    solve_captchas=session_options.solve_captchas,
                    adblock=session_options.adblock,
                )
                if session_options is not None
                else None
            ),
        )

        # Start and wait for browser use task
        response = self.client.agents.browser_use.start_and_wait(task_params)
        return {
            "data": response.data.final_result if response.data is not None else None,
            "error": response.error,
        }

    async def _arun(
        self,
        task: str,
        max_steps: Optional[int] = None,
        session_options: Optional[SimpleSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Async version of _run."""
        # Initialize async Hyperbrowser client

        task_params = StartBrowserUseTaskParams(
            task=task,
            use_vision=True,
            max_steps=max_steps,
            session_options=(
                CreateSessionParams(
                    use_proxy=session_options.use_proxy,
                    proxy_country=session_options.proxy_country,
                    solve_captchas=session_options.solve_captchas,
                    adblock=session_options.adblock,
                )
                if session_options is not None
                else None
            ),
        )

        # Start and wait for browser use task
        response = await self.async_client.agents.browser_use.start_and_wait(
            task_params
        )

        return {
            "data": response.data.final_result if response.data is not None else None,
            "error": response.error,
        }

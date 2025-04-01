"""Hyperbrowser browser use tool."""

from typing import Optional, Dict, Any
from langchain_core.tools import BaseTool
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser
from hyperbrowser.models import (
    StartClaudeComputerUseTaskParams,
    CreateSessionParams,
)
from pydantic import Field, SecretStr, model_validator

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

from ._utilities import initialize_client


class HyperbrowserClaudeComputerUseTool(BaseTool):
    """Tool for executing tasks using a browser agent."""

    name: str = "hyperbrowser_browser_use"
    description: str = (
        """Execute a task using a browser agent. This specific tool uses Claude Computer Use.
    The agent can navigate websites, interact with elements, and extract information.
    Provide a task description and optionally configure the agent's behavior.
    Returns the task result and metadata."""
    )
    client: Hyperbrowser = Field(default=None)  # type: ignore
    async_client: AsyncHyperbrowser = Field(default=None)  # type: ignore
    api_key: SecretStr = Field(default=None)  # type: ignore

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate the environment."""
        values = initialize_client(values)
        return values

    def _run(
        self,
        task: str,
        max_failures: Optional[int] = None,
        max_steps: Optional[int] = None,
        session_options: Optional[Dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Execute a task using Claude Computer Use agent.

        Args:
            task: The task to execute (e.g. "go to Hacker News and summarize the top 5 posts")
            max_failures: Optional maximum number of consecutive failures allowed before aborting
            max_steps: Optional maximum number of steps the agent can take to complete the task
            session_options: Optional parameters for browser session configuration

        Returns:
            Dict containing the task result and metadata with keys 'data' and 'error'
        """

        # Create browser use task parameters
        task_params = StartClaudeComputerUseTaskParams(
            task=task,
            max_failures=max_failures,
            max_steps=max_steps,
            session_options=(
                CreateSessionParams(**session_options)
                if session_options is not None
                else None
            ),
        )

        # Start and wait for browser use task
        response = self.client.agents.claude_computer_use.start_and_wait(task_params)
        return {
            "data": response.data.final_result if response.data is not None else None,
            "error": response.error,
        }

    async def _arun(
        self,
        task: str,
        max_failures: Optional[int] = None,
        max_steps: Optional[int] = None,
        session_options: Optional[Dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Execute a task using Claude Computer Use agent.

        Args:
            task: The task to execute (e.g. "go to Hacker News and summarize the top 5 posts")
            max_failures: Optional maximum number of consecutive failures allowed before aborting
            max_steps: Optional maximum number of steps the agent can take to complete the task
            session_options: Optional parameters for browser session configuration

        Returns:
            Dict containing the task result and metadata with keys 'data' and 'error'
        """

        # Create browser use task parameters
        task_params = StartClaudeComputerUseTaskParams(
            task=task,
            max_failures=max_failures,
            max_steps=max_steps,
            session_options=(
                CreateSessionParams(**session_options)
                if session_options is not None
                else None
            ),
        )

        # Start and wait for browser use task
        response = await self.async_client.agents.claude_computer_use.start_and_wait(
            task_params
        )

        return {
            "data": response.data.final_result if response.data is not None else None,
            "error": response.error,
        }

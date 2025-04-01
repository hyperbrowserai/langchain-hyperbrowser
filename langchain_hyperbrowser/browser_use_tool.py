"""Hyperbrowser browser use tool."""

from typing import Optional, Dict, Any
from langchain_core.tools import BaseTool
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser
from hyperbrowser.models import (
    StartBrowserUseTaskParams,
    BrowserUseLlm,
    CreateSessionParams,
)
from pydantic import Field, SecretStr, model_validator

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

from ._utilities import initialize_client


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

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate the environment."""
        values = initialize_client(values)
        return values

    def _run(
        self,
        task: str,
        llm: Optional[BrowserUseLlm] = None,
        session_id: Optional[str] = None,
        validate_output: Optional[bool] = None,
        use_vision: Optional[bool] = None,
        use_vision_for_planner: Optional[bool] = None,
        max_actions_per_step: Optional[int] = None,
        max_input_tokens: Optional[int] = None,
        planner_llm: Optional[BrowserUseLlm] = None,
        page_extraction_llm: Optional[BrowserUseLlm] = None,
        planner_interval: Optional[int] = None,
        max_steps: Optional[int] = None,
        keep_browser_open: Optional[bool] = None,
        session_options: Optional[CreateSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Execute a task using a browser agent.

        Args:
            task: The task to execute (e.g. "go to Hacker News and summarize the top 5 posts")
            llm: Optional LLM configuration for the browser agent
            session_id: Optional session ID to reuse an existing browser session
            validate_output: Optional flag to validate the output of the task
            use_vision: Optional flag to enable vision capabilities for the agent
            use_vision_for_planner: Optional flag to enable vision for the planner component
            max_actions_per_step: Optional limit on the number of actions per step
            max_input_tokens: Optional limit on the number of input tokens
            planner_llm: Optional LLM configuration for the planner component
            page_extraction_llm: Optional LLM configuration for page extraction
            planner_interval: Optional interval for planner execution in milliseconds
            max_steps: Optional maximum number of steps to execute
            keep_browser_open: Optional flag to keep the browser open after task completion
            session_options: Optional parameters for browser session configuration

        Returns:
            Dict containing the task result and metadata with keys 'data' and 'error'
        """

        # Create browser use task parameters
        task_params = StartBrowserUseTaskParams(
            task=task,
            llm=llm,
            session_id=session_id,
            validate_output=validate_output,
            use_vision=use_vision,
            use_vision_for_planner=use_vision_for_planner,
            max_actions_per_step=max_actions_per_step,
            max_input_tokens=max_input_tokens,
            planner_llm=planner_llm,
            page_extraction_llm=page_extraction_llm,
            planner_interval=planner_interval,
            max_steps=max_steps,
            keep_browser_open=keep_browser_open,
            session_options=session_options,
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
        llm: Optional[BrowserUseLlm] = None,
        session_id: Optional[str] = None,
        validate_output: Optional[bool] = None,
        use_vision: Optional[bool] = None,
        use_vision_for_planner: Optional[bool] = None,
        max_actions_per_step: Optional[int] = None,
        max_input_tokens: Optional[int] = None,
        planner_llm: Optional[BrowserUseLlm] = None,
        page_extraction_llm: Optional[BrowserUseLlm] = None,
        planner_interval: Optional[int] = None,
        max_steps: Optional[int] = None,
        keep_browser_open: Optional[bool] = None,
        session_options: Optional[CreateSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        """Async version of _run."""
        # Initialize async Hyperbrowser client

        task_params = StartBrowserUseTaskParams(
            task=task,
            llm=llm,
            session_id=session_id,
            validate_output=validate_output,
            use_vision=use_vision,
            use_vision_for_planner=use_vision_for_planner,
            max_actions_per_step=max_actions_per_step,
            max_input_tokens=max_input_tokens,
            planner_llm=planner_llm,
            page_extraction_llm=page_extraction_llm,
            planner_interval=planner_interval,
            max_steps=max_steps,
            keep_browser_open=keep_browser_open,
            session_options=session_options,
        )

        # Start and wait for browser use task
        response = await self.async_client.agents.browser_use.start_and_wait(
            task_params
        )

        return {
            "data": response.data.final_result if response.data is not None else None,
            "error": response.error,
        }

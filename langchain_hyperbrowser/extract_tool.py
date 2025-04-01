from typing import Optional, Union, Dict, Any
from langchain_core.tools import BaseTool
from hyperbrowser import Hyperbrowser, AsyncHyperbrowser  # type: ignore[untyped-import]
from hyperbrowser.models.extract import StartExtractJobParams
from hyperbrowser.models.session import CreateSessionParams
from pydantic import Field, SecretStr, model_validator


from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)

from ._utilities import initialize_client


class HyperbrowserExtractTool(BaseTool):

    name: str = "hyperbrowser_extract_data"
    description: str = (
        """Extract structured data from a webpage using AI.
    Provide a URL and optionally a prompt describing what data to extract.
    Provide a schema (Pydantic model or JSON schema) for structured extraction.
    Either the schema or extraction prompt **MUST** be provided.
    Prefer the schema since that is more concrete.
    Returns the extracted data and metadata."""
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
        url: str,
        extraction_prompt: Optional[str],
        json_schema: Optional[Union[object, Dict[str, Any]]],
        session_options: Optional[CreateSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Extract structured data from a webpage using AI.

        Args:
            url: The URL to extract data from
            extraction_prompt: A prompt describing what data to extract
            schema: Optional Pydantic model or JSON schema for structured extraction
            session_options: Optional parameters for the browser session
            run_manager: Optional callback manager for the tool run

        Note:
            Either prompt or schema must be provided for extraction to work properly.

        Returns:
            Dict containing the extracted data and any error information
        """
        # Create extract job parameters
        extract_params = StartExtractJobParams(
            urls=[url],
            prompt=extraction_prompt,
            schema=json_schema,
            session_options=session_options,
        )

        # Start and wait for extract job
        response = self.client.extract.start_and_wait(extract_params)

        return {"data": response.data, "error": response.error}

    async def _arun(
        self,
        url: str,
        extraction_prompt: Optional[str],
        json_schema: Optional[Union[object, Dict[str, Any]]],
        session_options: Optional[CreateSessionParams] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Asynchronously extract structured data from a webpage using AI.

        Args:
            url: The URL to extract data from
            extraction_prompt: A prompt describing what data to extract
            schema: Optional Pydantic model or JSON schema for structured extraction
            session_options: Optional parameters for the browser session
            run_manager: Optional callback manager for the tool run

        Note:
            Either prompt or schema must be provided for extraction to work properly.

        Returns:
            Dict containing the extracted data and any error information
        """
        # Create extract job parameters
        extract_params = StartExtractJobParams(
            urls=[url],
            prompt=extraction_prompt,
            schema=json_schema,
            session_options=session_options,
        )

        # Start and wait for extract job
        response = await self.async_client.extract.start_and_wait(extract_params)

        return {"data": response.data, "error": response.error}

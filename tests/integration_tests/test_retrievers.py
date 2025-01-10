from typing import Type

from langchain_hyperbrowser.retrievers import HyperbrowserRetriever
from langchain_tests.integration_tests import (
    RetrieversIntegrationTests,
)


class TestHyperbrowserRetriever(RetrieversIntegrationTests):
    @property
    def retriever_constructor(self) -> Type[HyperbrowserRetriever]:
        """Get an empty vectorstore for unit tests."""
        return HyperbrowserRetriever

    @property
    def retriever_constructor_params(self) -> dict:
        return {"k": 2}

    @property
    def retriever_query_example(self) -> str:
        """
        Returns a dictionary representing the "args" of an example retriever call.
        """
        return "example query"

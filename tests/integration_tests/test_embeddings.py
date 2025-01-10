"""Test Hyperbrowser embeddings."""

from typing import Type

from langchain_hyperbrowser.embeddings import HyperbrowserEmbeddings
from langchain_tests.integration_tests import EmbeddingsIntegrationTests


class TestParrotLinkEmbeddingsIntegration(EmbeddingsIntegrationTests):
    @property
    def embeddings_class(self) -> Type[HyperbrowserEmbeddings]:
        return HyperbrowserEmbeddings

    @property
    def embedding_model_params(self) -> dict:
        return {"model": "nest-embed-001"}

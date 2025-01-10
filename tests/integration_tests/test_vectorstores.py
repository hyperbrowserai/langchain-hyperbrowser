from typing import AsyncGenerator, Generator

import pytest
from langchain_hyperbrowser.vectorstores import HyperbrowserVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_tests.integration_tests import (
    AsyncReadWriteTestSuite,
    ReadWriteTestSuite,
)


class TestHyperbrowserVectorStoreSync(ReadWriteTestSuite):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        """Get an empty vectorstore for unit tests."""
        store = HyperbrowserVectorStore()
        # note: store should be EMPTY at this point
        # if you need to delete data, you may do so here
        try:
            yield store
        finally:
            # cleanup operations, or deleting data
            pass


class TestHyperbrowserVectorStoreAsync(AsyncReadWriteTestSuite):
    @pytest.fixture()
    async def vectorstore(self) -> AsyncGenerator[VectorStore, None]:  # type: ignore
        """Get an empty vectorstore for unit tests."""
        store = HyperbrowserVectorStore()
        # note: store should be EMPTY at this point
        # if you need to delete data, you may do so here
        try:
            yield store
        finally:
            # cleanup operations, or deleting data
            pass

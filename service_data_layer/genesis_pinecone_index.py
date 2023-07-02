import atexit

import pinecone
from pinecone import Index

from genesis.service_infra.genesis_context import GenesisRuntimeContext
from genesis.service_data_layer.genesis_pinecone_store import GenesisPineconeVectorStore
from genesis.service_infra.genesis_synchronization import CriticalSection, Locker


class GenesisPineconeIndex:

    def __init__(self, genesis_context: GenesisRuntimeContext, genesis_store: GenesisPineconeVectorStore) -> None:
        self._genesis_context = genesis_context
        self._genesis_store = genesis_store
        self._index_lock = CriticalSection()
        atexit.register(self._delete_index())
        self._create_index()
        self._validate_index()
        self._index = self._fetch_index()

    def __str__(self) -> str:
        return str(self._index.describe_index_stats())

    def _create_index(self) -> None:
        with Locker.acquire(self._index_lock):
            pinecone.create_index(
                name=self._genesis_context.client_id,
                metric=self._genesis_context.model_metric,
                dimension=self._genesis_context.model_dimension)

    def _validate_index(self) -> None:
        with Locker.acquire(self._index_lock):
            return self._genesis_context.client_id in GenesisPineconeIndex.list_indexes()

    def _fetch_index(self) -> Index:
        with Locker.acquire(self._index_lock):
            return pinecone.Index(index_name=self._genesis_context.client_id)

    def _delete_index(self) -> None:
        with Locker.acquire(self._index_lock):
            pinecone.delete_index(name=self._genesis_context.client_id)

    @staticmethod
    def list_indexes() -> str:
        return pinecone.list_indexes()




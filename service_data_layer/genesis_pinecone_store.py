import pinecone

from genesis.service_infra.genesis_context import GenesisRuntimeContext
from genesis.service_infra.genesis_synchronization import OneTimeLock, Locker, CriticalSection


class GenesisPineconeVectorStore:

    def __init__(self, genesis_context: GenesisRuntimeContext) -> None:
        self._genesis_context = genesis_context
        self._initialize_lock = OneTimeLock()

    def initialize(self) -> None:
        with Locker.acquire(self._initialize_lock) as lock_acquired:
            if lock_acquired:
                pinecone.init(
                    api_key=self._genesis_context.pinecone_api_key,
                    pinecone_environment=self._genesis_context.pinecone_environment)

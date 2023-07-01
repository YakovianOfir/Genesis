import atexit

import pinecone

from chatty.service_infra.chatty_context import ChattyRuntimeContext


class ChattyPineconeIndex:

    def __init__(self, chatty_context: ChattyRuntimeContext) -> None:
        self._chatty_context = chatty_context
        atexit.register(self._delete_index())
        self._create_index()

    def _create_index(self) -> None:
        pinecone.create_index(
            name=self._chatty_context.client_id,
            metric=self._chatty_context.model_metric,
            dimension=self._chatty_context.model_dimension)

    def _delete_index(self) -> None:
        pinecone.delete_index(name=self._chatty_context.client_id)


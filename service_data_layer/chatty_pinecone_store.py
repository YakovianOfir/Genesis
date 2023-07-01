import pinecone

from chatty.service_infra.chatty_context import ChattyRuntimeContext


class ChattyPineconeVectorStore:

    def __init__(self, chatty_context: ChattyRuntimeContext) -> None:
        pass

    @staticmethod
    def initialize_pinecone_engine(chatty_context: ChattyRuntimeContext) -> None:
        pinecone.init(
            api_key=chatty_context.pinecone_api_key,
            pinecone_environment=chatty_context.pinecone_environment)

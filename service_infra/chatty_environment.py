from __future__ import annotations

import os


class ChattyEnvironment:

    @staticmethod
    def read_environment_variable(environment_variable_name: str) -> str:
        return os.environ[environment_variable_name]

    @staticmethod
    def pinecone_environment() -> str:
        return ChattyEnvironment.read_environment_variable("PINECONE_ENVIRONMENT")

    @staticmethod
    def pinecone_api_key() -> str:
        return ChattyEnvironment.read_environment_variable("PINECONE_API_KEY")

    @staticmethod
    def openai_api_key() -> str:
        return ChattyEnvironment.read_environment_variable("OPENAI_API_KEY")



